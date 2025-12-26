from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل."),
                code='password_no_upper',
            )
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("كلمة المرور يجب أن تحتوي على حرف صغير واحد على الأقل."),
                code='password_no_lower',
            )
        if not re.findall('[0-9]', password):
            raise ValidationError(
                _("كلمة المرور يجب أن تحتوي على رقم واحد على الأقل."),
                code='password_no_number',
            )
        if not re.findall('[^A-Za-z0-9]', password):
            raise ValidationError(
                _("كلمة المرور يجب أن تحتوي على رمز واحد على الأقل."),
                code='password_no_symbol',
            )
        if len(password) > 16:
             raise ValidationError(
                _("كلمة المرور يجب ألا تزيد عن 16 خانة."),
                code='password_too_long',
            )

    def get_help_text(self):
        return _(
            "يجب أن تكون كلمة المرور بين 8 و 16 خانة، وتحتوي على حرف كبير، حرف صغير، رقم، ورمز."
        )
