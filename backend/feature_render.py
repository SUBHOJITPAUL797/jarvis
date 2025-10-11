import os
import eel
from backend.command_render import speak

@eel.expose
def play_assistant_sound():
    """Placeholder for sound - not used in web deployment"""
    print("Sound play skipped for web deployment")

def chatBot(query):
    """AI chatbot using Google Gemini API"""
    user_input = query.lower()
    try:
        import google.generativeai as genai
        
        # Get API key from environment variable
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            speak("Please set the GEMINI_API_KEY environment variable")
            return "API key not configured"
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Create the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate response
        response = model.generate_content(user_input)
        response_text = response.text
        
        print(f"AI Response: {response_text}")
        speak(response_text)
        return response_text
    except Exception as e:
        error_msg = f"Error with AI service: {e}"
        print(error_msg)
        speak("Sorry, I'm having trouble connecting to the AI service. Please check your API key.")
        return "Error occurred"