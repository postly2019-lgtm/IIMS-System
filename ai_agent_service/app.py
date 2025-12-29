# app_advanced.py - إصدار متقدم مع ميزات إضافية 
import os 
import time 
import logging 
from flask import Flask, request, jsonify, Response 
from groq import Groq 
from dotenv import load_dotenv 
import json 
from functools import wraps 

# إعداد التسجيل 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 

load_dotenv() 

app = Flask(__name__) 

# Middleware للتحقق من المفتاح (اختياري) 
def require_api_key(f): 
    @wraps(f) 
    def decorated(*args, **kwargs): 
        # api_key = request.headers.get('X-API-Key') 
        # if api_key != os.environ.get('API_SECRET_KEY'): 
        #     return jsonify({"error": "Unauthorized"}), 401 
        return f(*args, **kwargs) 
    return decorated 

class GroqAgent:
    def __init__(self):
        try:
            self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            self.model = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")
            logger.info(f"Groq Agent initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            self.client = None
            self.model = "unknown"

    def chat(self, messages, stream=False, **kwargs):
        """الدردشة مع النموذج"""
        if not self.client:
            raise RuntimeError("Groq client is not initialized")
            
        try: 
            start_time = time.time() 
            
            completion = self.client.chat.completions.create( 
                model=self.model, 
                messages=messages, 
                temperature=kwargs.get('temperature', 0.7), 
                max_completion_tokens=kwargs.get('max_tokens', 2048), 
                top_p=kwargs.get('top_p', 1), 
                stream=stream, 
                stop=kwargs.get('stop', None) 
            ) 
            
            if stream: 
                return self._handle_stream(completion) 
            else: 
                response_time = time.time() - start_time 
                logger.info(f"Chat completed in {response_time:.2f}s") 
                
                return { 
                    "response": completion.choices[0].message.content, 
                    "model": self.model, 
                    "usage": completion.usage.dict() if completion.usage else None, 
                    "response_time": response_time 
                } 
                
        except Exception as e: 
            logger.error(f"Chat error: {str(e)}") 
            raise 
    
    def _handle_stream(self, completion): 
        """معالجة الردود المتدفقة""" 
        for chunk in completion: 
            if chunk.choices[0].delta.content: 
                yield chunk.choices[0].delta.content 

# تهيئة الوكيل 
agent = GroqAgent() 

@app.route('/api/v1/chat', methods=['POST']) 
# @require_api_key  # قم بتفعيله إذا أردت التحقق من الهوية 
def chat(): 
    """نقطة نهاية رئيسية للدردشة""" 
    data = request.json 
    
    required_fields = ['messages'] 
    for field in required_fields: 
        if field not in data: 
            return jsonify({"error": f"Missing required field: {field}"}), 400 
    
    try: 
        stream = data.get('stream', False) 
        
        if stream: 
            def generate(): 
                for chunk in agent.chat( 
                    messages=data['messages'], 
                    stream=True, 
                    temperature=data.get('temperature', 0.7), 
                    max_tokens=data.get('max_tokens', 2048) 
                ): 
                    yield f"data: {json.dumps({'content': chunk})}\n\n" 
                yield "data: [DONE]\n\n" 
            
            return Response(generate(), mimetype='text/event-stream') 
        else: 
            result = agent.chat( 
                messages=data['messages'], 
                stream=False, 
                temperature=data.get('temperature', 0.7), 
                max_tokens=data.get('max_tokens', 2048) 
            ) 
            
            return jsonify(result) 
            
    except Exception as e: 
        logger.error(f"API error: {str(e)}") 
        return jsonify({"error": str(e)}), 500 

@app.route('/api/v1/models', methods=['GET']) 
def list_models(): 
    """الحصول على قائمة النماذج المتاحة""" 
    return jsonify({ 
        "models": [agent.model], 
        "current_model": agent.model, 
        "provider": "Groq" 
    }) 

@app.route('/') 
def index(): 
    """الصفحة الرئيسية""" 
    return jsonify({ 
        "service": "Groq AI Agent API", 
        "status": "running", 
        "model": agent.model, 
        "endpoints": { 
            "chat": "/api/v1/chat (POST)", 
            "models": "/api/v1/models (GET)", 
            "health": "/health (GET)" 
        } 
    }) 

@app.route('/health', methods=['GET']) 
def health(): 
    """فحص الصحة""" 
    try: 
        # اختبار اتصال بسيط 
        test_response = agent.client.models.list() 
        return jsonify({ 
            "status": "healthy", 
            "model": agent.model, 
            "provider": "Groq", 
            "timestamp": time.time() 
        }) 
    except Exception as e: 
        return jsonify({"status": "unhealthy", "error": str(e)}), 500 

if __name__ == '__main__': 
    port = int(os.environ.get('PORT', 8000)) 
    app.run(host='0.0.0.0', port=port, debug=False)
