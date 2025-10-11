import os
import eel
from backend.auth import recoganize
from backend.auth.recoganize import AuthenticateFace
from backend.feature import *
from backend.command import *

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Using system environment variables only.")

def start():
    # Get port from environment variable (for deployment)
    port = int(os.environ.get('PORT', 8000))
    
    eel.init("frontend") 
    
    play_assistant_sound()
    
    @eel.expose
    def init():
        eel.hideLoader()
        speak("Welcome to Jarvis")
        speak("Ready for Face Authentication")
        try:
            flag = recoganize.AuthenticateFace()
            if flag == 1:
                speak("Face recognized successfully")
                eel.hideFaceAuth()
                eel.hideFaceAuthSuccess()
                speak("Welcome to Your Assistant")
                eel.hideStart()
                play_assistant_sound()
            else:
                speak("Face not recognized. Please try again")
        except Exception as e:
            print(f"Face recognition error: {e}")
            speak("Camera not available. Skipping face authentication.")
            eel.hideFaceAuth()
            eel.hideFaceAuthSuccess()
            speak("Welcome to Your Assistant")
            eel.hideStart()
            play_assistant_sound()
    
    # For deployment, don't open browser automatically
    if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RENDER'):
        print(f"Jarvis is running on port {port}")
        print("Access your Jarvis at the provided URL")
    else:
        # Local development - open browser
        # Cross-platform browser opening
        import platform
        import webbrowser
        if platform.system() == 'Windows':
            os.system('start msedge.exe --app="http://127.0.0.1:8000/index.html"')
        else:
            webbrowser.open(f"http://127.0.0.1:{port}/index.html")
    
    eel.start("index.html", mode=None, host="0.0.0.0", port=port, block=True)

if __name__ == "__main__":
    start()
