import re
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class SmartDictionaryTranslator:
    """
    A sovereign, offline translation engine optimized for military and political intelligence.
    Now loads terms from the database (SovereignTerm).
    """

    def __init__(self):
        # Fallback/Bootstrap terms if DB is empty or fails
        self.common_terms = {
            r'\bsays\b': 'يقول',
            r'\bsaid\b': 'قال',
            r'\breports\b': 'تقارير',
            r'\bwarns\b': 'يحذر',
            r'\bannounces\b': 'يعلن',
            r'\bclaims\b': 'يزعم',
            r'\bdenies\b': 'ينفي',
            r'\bconfirms\b': 'يؤكد',
            r'\bin\b': 'في',
            r'\bon\b': 'على',
            r'\bto\b': 'إلى',
            r'\bfrom\b': 'من',
            r'\bwith\b': 'مع',
            r'\bagainst\b': 'ضد',
            r'\band\b': 'و',
            r'\bnew\b': 'جديد',
            r'\burgent\b': 'عاجل',
            r'\bbreaking\b': 'عاجل',
        }
        self._cache = None

    def _load_terms(self):
        """Loads terms from the database into a sorted list of (pattern, replacement)."""
        try:
            # Avoid import errors at module level
            from intelligence.models import SovereignTerm
            
            terms = []
            
            # Add common terms
            for p, t in self.common_terms.items():
                terms.append((p, t))

            # Add DB terms
            db_terms = SovereignTerm.objects.all()
            for term in db_terms:
                pattern = term.english_term
                
                # If not a regex, enforce word boundaries and escape special chars
                if not term.is_regex:
                    escaped_term = re.escape(term.english_term)
                    pattern = fr'\b{escaped_term}\b'
                    
                terms.append((pattern, term.arabic_translation))
            
            # Sort by length of pattern string to prioritize longer matches
            # e.g., "Prime Minister" (14 chars) should be replaced before "Minister" (8 chars)
            terms.sort(key=lambda x: len(x[0]), reverse=True)
            
            return terms
        except Exception as e:
            logger.error(f"Failed to load SovereignTerms from DB: {e}")
            # Return just common terms as fallback
            return list(self.common_terms.items())

    def refresh_cache(self):
        """Forces a reload of terms from the database."""
        self._cache = self._load_terms()

    def translate_text(self, text):
        """
        Translates text using regex-based dictionary substitution.
        """
        if not text:
            return ""

        # Lazy Load
        if self._cache is None:
            self._cache = self._load_terms()

        translated_text = text
        
        for pattern, replacement in self._cache:
            try:
                # Case insensitive replacement
                translated_text = re.sub(pattern, replacement, translated_text, flags=re.IGNORECASE)
            except re.error:
                # Fallback if pattern is invalid regex
                continue
            
        return translated_text

# Singleton Instance
translator = SmartDictionaryTranslator()
