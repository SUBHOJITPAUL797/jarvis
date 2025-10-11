"""
Jarvis AI Assistant - Complete Web Application
A fully functional AI assistant with multiple capabilities
"""

import os
import json
import datetime
import re
import base64
from flask import Flask, render_template, request, jsonify, session, send_file
from flask_cors import CORS
import google.generativeai as genai
from werkzeug.utils import secure_filename
import secrets
import markdown
from io import BytesIO

# Initialize Flask app
app = Flask(__name__, 
            template_folder='frontend', 
            static_folder='frontend/static',
            static_url_path='/static')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=24)

# Enable CORS
CORS(app)

# Configure Gemini API
api_key = os.environ.get('GEMINI_API_KEY', 'AIzaSyBIT39QDL7bEQqpOPYXLXxa5ueA8z3SpBU')
genai.configure(api_key=api_key)

# Initialize models
chat_model = genai.GenerativeModel('gemini-2.5-flash')
vision_model = genai.GenerativeModel('gemini-2.5-flash')

# Store conversation history in memory (in production, use database)
conversations = {}

# AI Capabilities Configuration
AI_CAPABILITIES = {
    'chat': 'General conversation and questions',
    'code': 'Generate, debug, and explain code',
    'translate': 'Translate between languages',
    'summarize': 'Summarize long texts',
    'creative': 'Write stories, poems, and creative content',
    'analyze': 'Analyze data and provide insights',
    'learn': 'Educational explanations and tutoring',
    'professional': 'Business emails, reports, and documents',
    'math': 'Solve mathematical problems',
    'research': 'Research assistance and fact-checking'
}

# Helper Functions
def get_or_create_session_id():
    """Get or create a unique session ID for the user"""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)
        session['created_at'] = datetime.datetime.now().isoformat()
    return session['session_id']

def get_conversation_history(session_id):
    """Get conversation history for a session"""
    if session_id not in conversations:
        conversations[session_id] = {
            'messages': [],
            'context': '',
            'created_at': datetime.datetime.now().isoformat(),
            'last_activity': datetime.datetime.now().isoformat()
        }
    return conversations[session_id]

def format_ai_response(text):
    """Format AI response with markdown support"""
    # Convert markdown to HTML for better formatting
    html = markdown.markdown(text, extensions=['extra', 'codehilite'])
    return html

def generate_prompt_with_context(message, mode, context=''):
    """Generate appropriate prompt based on mode and context"""
    prompts = {
        'chat': f"{context}\nUser: {message}\nAssistant:",
        'code': f"You are an expert programmer. {context}\nUser request: {message}\nProvide clean, commented code with explanations:",
        'translate': f"Translate the following text accurately. Detect the source language automatically:\n{message}",
        'summarize': f"Provide a clear, concise summary of the following text:\n{message}",
        'creative': f"You are a creative writer. {context}\n{message}",
        'analyze': f"Analyze the following and provide detailed insights:\n{message}",
        'learn': f"You are an educational tutor. Explain clearly and provide examples.\n{context}\nTopic: {message}",
        'professional': f"Write in a professional business tone.\n{message}",
        'math': f"Solve the following mathematical problem step by step:\n{message}",
        'research': f"Provide researched, factual information about:\n{message}"
    }
    return prompts.get(mode, prompts['chat'])

# Routes
@app.route('/')
def index():
    """Main page"""
    session_id = get_or_create_session_id()
    return render_template('jarvis_premium.html', session_id=session_id)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.now().isoformat()})

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint with multiple capabilities"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        mode = data.get('mode', 'chat')
        include_history = data.get('include_history', True)
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get session and history
        session_id = get_or_create_session_id()
        conversation = get_conversation_history(session_id)
        
        # Build context from history if requested
        context = ''
        if include_history and conversation['messages']:
            recent_messages = conversation['messages'][-10:]  # Last 10 messages
            context = "Previous conversation:\n"
            for msg in recent_messages:
                context += f"{msg['role']}: {msg['content'][:200]}...\n"
        
        # Generate appropriate prompt
        prompt = generate_prompt_with_context(message, mode, context)
        
        # Generate AI response
        response = chat_model.generate_content(prompt)
        response_text = response.text
        
        # Format response
        formatted_response = format_ai_response(response_text)
        
        # Store in conversation history
        conversation['messages'].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.datetime.now().isoformat(),
            'mode': mode
        })
        conversation['messages'].append({
            'role': 'assistant',
            'content': response_text,
            'formatted': formatted_response,
            'timestamp': datetime.datetime.now().isoformat()
        })
        conversation['last_activity'] = datetime.datetime.now().isoformat()
        
        # Limit history to last 100 messages to prevent memory issues
        if len(conversation['messages']) > 100:
            conversation['messages'] = conversation['messages'][-100:]
        
        return jsonify({
            'response': response_text,
            'formatted': formatted_response,
            'mode': mode,
            'session_id': session_id,
            'message_count': len(conversation['messages'])
        })
        
    except Exception as e:
        app.logger.error(f"Chat error: {str(e)}")
        return jsonify({
            'error': 'An error occurred processing your request',
            'details': str(e) if app.debug else None
        }), 500

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    """Analyze uploaded images using Gemini Vision"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image = request.files['image']
        prompt = request.form.get('prompt', 'Describe this image in detail')
        
        if image.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Read image data
        image_data = image.read()
        
        # Prepare image for Gemini
        import PIL.Image
        from io import BytesIO
        img = PIL.Image.open(BytesIO(image_data))
        
        # Generate response
        response = vision_model.generate_content([prompt, img])
        response_text = response.text
        
        # Store in history
        session_id = get_or_create_session_id()
        conversation = get_conversation_history(session_id)
        conversation['messages'].append({
            'role': 'user',
            'content': f"[Image Analysis] {prompt}",
            'timestamp': datetime.datetime.now().isoformat(),
            'mode': 'vision'
        })
        conversation['messages'].append({
            'role': 'assistant',
            'content': response_text,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        return jsonify({
            'response': response_text,
            'formatted': format_ai_response(response_text)
        })
        
    except Exception as e:
        app.logger.error(f"Image analysis error: {str(e)}")
        return jsonify({'error': 'Failed to analyze image', 'details': str(e)}), 500

@app.route('/get_history', methods=['GET'])
def get_history():
    """Get conversation history for current session"""
    try:
        session_id = get_or_create_session_id()
        conversation = get_conversation_history(session_id)
        
        return jsonify({
            'history': conversation['messages'][-50:],  # Last 50 messages
            'session_id': session_id,
            'created_at': conversation['created_at'],
            'message_count': len(conversation['messages'])
        })
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve history'}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        session_id = get_or_create_session_id()
        if session_id in conversations:
            conversations[session_id]['messages'] = []
            conversations[session_id]['context'] = ''
        return jsonify({'success': True, 'message': 'History cleared'})
    except Exception as e:
        return jsonify({'error': 'Failed to clear history'}), 500

@app.route('/export_conversation', methods=['GET'])
def export_conversation():
    """Export conversation as text file"""
    try:
        session_id = get_or_create_session_id()
        conversation = get_conversation_history(session_id)
        
        # Format conversation for export
        export_text = f"Jarvis AI Conversation Export\n"
        export_text += f"Session: {session_id}\n"
        export_text += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        export_text += "="*50 + "\n\n"
        
        for msg in conversation['messages']:
            timestamp = msg.get('timestamp', '')
            role = "You" if msg['role'] == 'user' else "Jarvis"
            export_text += f"[{timestamp}] {role}:\n{msg['content']}\n\n"
        
        # Create file in memory
        output = BytesIO()
        output.write(export_text.encode('utf-8'))
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/plain',
            as_attachment=True,
            download_name=f'jarvis_conversation_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        )
    except Exception as e:
        return jsonify({'error': 'Failed to export conversation'}), 500

@app.route('/get_capabilities', methods=['GET'])
def get_capabilities():
    """Get list of AI capabilities"""
    return jsonify({'capabilities': AI_CAPABILITIES})

@app.route('/suggest_prompts', methods=['GET'])
def suggest_prompts():
    """Get suggested prompts based on mode"""
    mode = request.args.get('mode', 'chat')
    
    suggestions = {
        'chat': [
            "What's the weather like today?",
            "Tell me an interesting fact",
            "How can I be more productive?",
            "Explain quantum computing simply"
        ],
        'code': [
            "Write a Python function to sort a list",
            "Debug this JavaScript code: [paste code]",
            "Explain how async/await works",
            "Create a REST API endpoint"
        ],
        'translate': [
            "Translate 'Hello World' to Spanish",
            "How do you say 'Thank you' in Japanese?",
            "Translate this paragraph to French: [text]"
        ],
        'creative': [
            "Write a short story about time travel",
            "Create a haiku about technology",
            "Generate character names for a fantasy novel"
        ],
        'math': [
            "Solve: 2x + 5 = 15",
            "Calculate the derivative of x^3 + 2x",
            "Explain the Pythagorean theorem"
        ]
    }
    
    return jsonify({'suggestions': suggestions.get(mode, suggestions['chat'])})

@app.route('/feedback', methods=['POST'])
def feedback():
    """Collect user feedback"""
    try:
        data = request.json
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        # In production, store this in a database
        app.logger.info(f"Feedback received - Rating: {rating}, Comment: {comment}")
        
        return jsonify({'success': True, 'message': 'Thank you for your feedback!'})
    except Exception as e:
        return jsonify({'error': 'Failed to submit feedback'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# Run the application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)