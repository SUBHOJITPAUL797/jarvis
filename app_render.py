import os
import eel
from backend.feature_render import *
from backend.command_render import *

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Using system environment variables only.")

def start():
    # Get port from environment variable (required for Render)
    port = int(os.environ.get('PORT', 10000))
    
    eel.init("frontend") 
    
    @eel.expose
    def init():
        eel.hideLoader()
        # Skip face authentication for web deployment
        eel.hideFaceAuth()
        eel.hideFaceAuthSuccess()
        speak("Welcome to Jarvis Assistant")
        eel.hideStart()
    
    # For Render deployment
    print(f"Jarvis is running on port {port}")
    print("Access your Jarvis at the provided URL")
    
    # Start with all IPs accessible for Render
    eel.start("index_render.html", mode=None, host="0.0.0.0", port=port, block=True)

if __name__ == "__main__":
    start()