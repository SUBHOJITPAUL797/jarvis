import eel

# Simplified speak function for web deployment
def speak(text):
    text = str(text)
    print(f"Assistant: {text}")
    eel.DisplayMessage(text)
    eel.receiverText(text)

@eel.expose
def takeAllCommands(message):
    """Handle text-based commands only for web deployment"""
    if not message:
        return
    
    query = message.lower()
    print(f"User: {query}")
    eel.senderText(query)
    
    try:
        # For web deployment, only use chatbot functionality
        from backend.feature_render import chatBot
        response = chatBot(query)
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, something went wrong. Please try again.")
    
    eel.ShowHood()