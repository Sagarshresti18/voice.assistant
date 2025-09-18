import speech_recognition as sr

def test_microphone():
    recognizer = sr.Recognizer()
    
    # List all available microphones
    print("\nAvailable microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone {index}: {name}")
    
    try:
        # Try to use the Microphone Array
        microphone_index = None
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if "Microphone Array" in name:
                microphone_index = index
                break
        
        if microphone_index is None:
            print("\nNo Microphone Array found, using default microphone...")
            mic = sr.Microphone()
        else:
            print(f"\nUsing Microphone Array (index {microphone_index})...")
            mic = sr.Microphone(device_index=microphone_index)
        
        with mic as source:
            print("Adjusting for ambient noise... Please be quiet.")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("\nMicrophone is ready! Please say something...")
            try:
                audio = recognizer.listen(source, timeout=5)
                print("\nRecognizing your speech...")
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"\nYou said: {text}")
                except sr.UnknownValueError:
                    print("\nCould not understand the audio")
                except sr.RequestError as e:
                    print(f"\nCould not request results; {e}")
            except sr.WaitTimeoutError:
                print("\nNo speech detected within timeout period")
    except Exception as e:
        print(f"\nError accessing microphone: {e}")
        print("Please check if your microphone is properly connected and allowed in Windows permissions.")
        print("To check Windows permissions:")
        print("1. Open Windows Settings")
        print("2. Go to Privacy & Security > Microphone")
        print("3. Ensure 'Microphone access' is turned on")
        print("4. Make sure Python/VS Code has permission to use the microphone")

if __name__ == "__main__":
    test_microphone()