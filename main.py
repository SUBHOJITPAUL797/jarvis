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
        
    # Cross-platform browser opening
    import platform
    import webbrowser
    if platform.system() == 'Windows':
        os.system('start msedge.exe --app="http://127.0.0.1:8000/index.html"')
    else:
        webbrowser.open("http://127.0.0.1:8000/index.html")
    
    
    
    eel.start("index.html", mode=None, host="localhost", block=True) 

