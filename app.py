import speech_recognition as sr
import pyttsx3
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import json
import subprocess
import os
import sys
import platform
from datetime import datetime
import wikipedia
import re
from googlesearch import search
import threading
import time
import logging
from config import Config

class AdvancedVoiceAssistant:
    def __init__(self):
        """Initialize the Advanced Voice Assistant"""
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Print configuration status
        Config.print_config_status()
        Config.validate_config()
        
        # Initialize components
        self.setup_speech_recognition()
        self.setup_text_to_speech()
        self.setup_spotify()
        
        # State management
        self.is_listening = False
        self.last_command_time = time.time()
        
        # Initialize assistant
        self.logger.info("Voice Assistant initialized successfully!")
        self.speak(Config.GREETING_MESSAGE)
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_level = getattr(logging, Config.LOG_LEVEL.upper())
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def setup_speech_recognition(self):
        """Initialize speech recognition"""
        self.recognizer = sr.Recognizer()
        
        # Try to find the Microphone Array
        microphone_index = None
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if "Microphone Array" in name:
                microphone_index = index
                break
        
        # Use Microphone Array if found, otherwise use default
        if microphone_index is not None:
            print(f"🎤 Using Microphone Array (index {microphone_index})...")
            self.microphone = sr.Microphone(device_index=microphone_index)
        else:
            print("🎤 Using default microphone...")
            self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            print("🎤 Calibrating microphone for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=Config.AMBIENT_NOISE_DURATION)
        print("✅ Microphone calibrated!")
    
    def setup_text_to_speech(self):
        """Configure text-to-speech engine"""
        self.tts_engine = pyttsx3.init()
        
        # Configure voice properties
        self.tts_engine.setProperty('rate', Config.TTS_RATE)
        self.tts_engine.setProperty('volume', Config.TTS_VOLUME)
        
        # Set preferred voice
        voices = self.tts_engine.getProperty('voices')
        if Config.TTS_VOICE_PREFERENCE and voices:
            for voice in voices:
                if Config.TTS_VOICE_PREFERENCE.lower() in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    self.logger.info(f"Selected voice: {voice.name}")
                    break
    
    def setup_spotify(self):
        """Initialize Spotify client"""
        try:
            if Config.SPOTIFY_CLIENT_ID != 'your_spotify_client_id':
                auth_manager = SpotifyOAuth(
                    client_id=Config.SPOTIFY_CLIENT_ID,
                    client_secret=Config.SPOTIFY_CLIENT_SECRET,
                    redirect_uri=Config.SPOTIFY_REDIRECT_URI,
                    scope=Config.SPOTIFY_SCOPE,
                    cache_path=".cache"
                )
                self.spotify = spotipy.Spotify(auth_manager=auth_manager)
                self.logger.info("✅ Spotify connected successfully!")
            else:
                self.spotify = None
                self.logger.warning("⚠️ Spotify credentials not configured")
        except Exception as e:
            self.logger.error(f"❌ Spotify setup failed: {e}")
            self.spotify = None
    
    def speak(self, text):
        """Convert text to speech with improved error handling"""
        try:
            print(f"🤖 {Config.ASSISTANT_NAME}: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            self.logger.error(f"TTS Error: {e}")
            print(f"🤖 {Config.ASSISTANT_NAME}: {text}")  # Fallback to text only
    
    def listen(self, timeout=None):
        """Enhanced listening with better error handling"""
        try:
            with self.microphone as source:
                print("🎧 Listening...")
                # Adjust the microphone for ambient noise before each listen
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout or Config.SPEECH_TIMEOUT,
                    phrase_time_limit=Config.PHRASE_TIME_LIMIT
                )
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio).lower()
            print(f"👤 You said: {text}")
            self.logger.info(f"Speech recognized: {text}")
            return text
        
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout...")
            return "timeout"
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            return "unknown"
        except sr.RequestError as e:
            print(f"🌐 Network error: {e}")
            self.logger.error(f"Speech recognition error: {e}")
            return "network_error"
        except Exception as e:
            print(f"❌ Error: {e}")
            self.logger.error(f"Listening error: {e}")
            return "error"
    
    def extract_intent_and_entity(self, text):
        """Enhanced NLP for command recognition"""
        text = text.lower().strip()
        print(f"🔍 Analyzing command: '{text}'")
        
        for intent, patterns in Config.COMMAND_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    entities = match.groups() if match.groups() else []
                    entity = entities[0] if entities else None
                    print(f"✅ Found intent: '{intent}', entity: '{entity}'")
                    self.logger.info(f"Intent: {intent}, Entities: {entities}")
                    return intent, entity
        
        # Special handling for YouTube commands
        if "youtube" in text:
            if "search" in text or "find" in text:
                # Extract everything after "youtube" or "for"
                search_query = text.split("youtube")[-1]
                if "for" in search_query:
                    search_query = search_query.split("for")[-1]
                search_query = search_query.strip()
                print(f"✅ Found YouTube search query: '{search_query}'")
                return "search_youtube", search_query
            
        print("❌ No intent found")
        return "unknown", None
    
    def play_spotify_music(self, query):
        """Enhanced Spotify music control"""
        if not self.spotify:
            self.speak("Spotify is not connected. Please check your credentials.")
            return
        
        try:
            # Search for tracks, albums, or artists
            results = self.spotify.search(q=query, type='track,album,artist', limit=5)
            
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                track_uri = track['uri']
                
                # Get available devices
                devices = self.spotify.devices()
                active_device = None
                
                for device in devices['devices']:
                    if device['is_active']:
                        active_device = device
                        break
                
                if not active_device and devices['devices']:
                    active_device = devices['devices'][0]
                
                if active_device:
                    self.spotify.start_playback(device_id=active_device['id'], uris=[track_uri])
                    response = Config.RESPONSES['spotify_playing'].format(
                        song=track_name, artist=artist_name
                    )
                    self.speak(response)
                else:
                    self.speak(Config.RESPONSES['spotify_no_device'])
            else:
                response = Config.RESPONSES['spotify_not_found'].format(query=query)
                self.speak(response)
                
        except Exception as e:
            self.logger.error(f"Spotify error: {e}")
            self.speak("Sorry, there was an error with Spotify playback.")
    
    def control_spotify_playback(self, action):
        """Control Spotify playback (pause, resume, next, previous)"""
        if not self.spotify:
            self.speak("Spotify is not connected.")
            return
        
        try:
            if action == 'pause':
                self.spotify.pause_playback()
                self.speak(Config.RESPONSES['spotify_paused'])
            elif action == 'resume':
                self.spotify.start_playback()
                self.speak(Config.RESPONSES['spotify_resumed'])
            elif action == 'next':
                self.spotify.next_track()
                self.speak(Config.RESPONSES['spotify_next'])
            elif action == 'previous':
                self.spotify.previous_track()
                self.speak(Config.RESPONSES['spotify_previous'])
        except Exception as e:
            self.logger.error(f"Spotify control error: {e}")
            self.speak("Sorry, there was an error controlling Spotify.")
    
    def search_youtube(self, query):
        """Enhanced YouTube search"""
        try:
            print(f"🎥 Searching YouTube for: {query}")
            # Clean up the query
            search_query = query.strip().replace(' ', '+')
            search_url = f"https://www.youtube.com/results?search_query={search_query}"
            
            # Open the search URL
            webbrowser.open(search_url)
            
            # Speak the response
            response = Config.RESPONSES['youtube_search'].format(query=query)
            self.speak(response)
        except Exception as e:
            self.logger.error(f"YouTube search error: {e}")
            self.speak("Sorry, there was an error searching YouTube")
    
    def search_google(self, query):
        """Enhanced Google search with results preview"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            response = Config.RESPONSES['google_search'].format(query=query)
            self.speak(response)
            
            # Try to get quick answer
            try:
                search_results = list(search(query, num_results=1, stop=1))
                if search_results:
                    self.logger.info(f"Top result: {search_results[0]}")
            except:
                pass  # Ignore if search API fails
                
        except Exception as e:
            self.logger.error(f"Google search error: {e}")
            self.speak("Sorry, there was an error searching Google")
    
    def get_weather(self, location=None):
        """Enhanced weather information"""
        if not location:
            location = Config.DEFAULT_CITY
        
        try:
            if Config.OPENWEATHER_API_KEY != 'your_openweather_api_key':
                url = f"http://api.openweathermap.org/data/2.5/weather"
                params = {
                    'q': location,
                    'appid': Config.OPENWEATHER_API_KEY,
                    'units': Config.WEATHER_UNITS
                }
                
                response = requests.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
                data = response.json()
                
                if data["cod"] == 200:
                    weather_desc = data["weather"][0]["description"]
                    temp = round(data["main"]["temp"])
                    feels_like = round(data["main"]["feels_like"])
                    
                    response_text = Config.RESPONSES['weather_info'].format(
                        location=location,
                        description=weather_desc,
                        temp=temp,
                        feels_like=feels_like
                    )
                    self.speak(response_text)
                else:
                    response_text = Config.RESPONSES['weather_not_found'].format(location=location)
                    self.speak(response_text)
            else:
                # Fallback to web search
                search_url = f"https://www.google.com/search?q=weather+in+{location.replace(' ', '+')}"
                webbrowser.open(search_url)
                self.speak(f"Opening weather search for {location}")
                
        except Exception as e:
            self.logger.error(f"Weather API error: {e}")
            self.speak(f"I couldn't get weather data. Let me search the web for you.")
            search_url = f"https://www.google.com/search?q=weather+in+{location.replace(' ', '+')}"
            webbrowser.open(search_url)
    
    def get_current_time(self):
        """Get and speak current time"""
        current_time = datetime.now().strftime("%I:%M %p")
        response = Config.RESPONSES['time_response'].format(time=current_time)
        self.speak(response)
    
    def get_current_date(self):
        """Get and speak current date"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        response = Config.RESPONSES['date_response'].format(date=current_date)
        self.speak(response)
    
    def search_wikipedia(self, query):
        """Enhanced Wikipedia search"""
        try:
            summary = wikipedia.summary(query, sentences=2)
            response = Config.RESPONSES['wikipedia_info'].format(summary=summary)
            self.speak(response)
        except wikipedia.exceptions.DisambiguationError as e:
            try:
                summary = wikipedia.summary(e.options[0], sentences=2)
                response = Config.RESPONSES['wikipedia_info'].format(summary=summary)
                self.speak(response)
            except:
                self.speak(f"I found multiple results for {query}. Please be more specific.")
        except wikipedia.exceptions.PageError:
            response = Config.RESPONSES['wikipedia_not_found'].format(query=query)
            self.speak(response)
        except Exception as e:
            self.logger.error(f"Wikipedia error: {e}")
            self.speak("Sorry, there was an error searching Wikipedia")
    
    def open_application(self, app_name):
        """Open applications with cross-platform support"""
        try:
            app_name_lower = app_name.lower()
            
            # Check if it's a web application
            if app_name_lower in Config.WEB_APPLICATIONS:
                url = Config.WEB_APPLICATIONS[app_name_lower]
                webbrowser.open(url)
                response = f"Opening {app_name} in your browser"
                self.speak(response)
                return
            
            # Check if it's a desktop application
            if app_name_lower in Config.APPLICATIONS:
                app_path = Config.APPLICATIONS[app_name_lower]
            else:
                app_path = app_name
            
            system = platform.system()
            
            if system == "Windows":
                subprocess.run(['start', app_path], shell=True, check=True)
            elif system == "Darwin":  # macOS
                subprocess.run(['open', '-a', app_path], check=True)
            else:  # Linux
                subprocess.run([app_path], check=True)
            
            response = Config.RESPONSES['app_opened'].format(app=app_name)
            self.speak(response)
            
        except subprocess.CalledProcessError:
            response = Config.RESPONSES['app_not_found'].format(app=app_name)
            self.speak(response)
        except Exception as e:
            self.logger.error(f"Application launch error: {e}")
            self.speak(f"Sorry, I couldn't open {app_name}")
    
    def open_news(self):
        """Open news websites"""
        news_sites = [
            "https://news.google.com",
            "https://www.bbc.com/news",
            "https://www.cnn.com",
            "https://www.reuters.com"
        ]
        webbrowser.open(news_sites[0])  # Default to Google News
        self.speak(Config.RESPONSES['news_opening'])
    
    def process_command(self, text):
        """Enhanced command processing with better intent recognition"""
        print(f"🔍 Processing command: '{text}'")
        intent, entity = self.extract_intent_and_entity(text)
        print(f"🎯 Detected intent: '{intent}', entity: '{entity}'")
        
        try:
            if intent == "play_spotify":
                print("🎵 Attempting to play music on Spotify...")
                self.play_spotify_music(entity)
            
            elif intent == "pause_spotify":
                print("⏸️ Attempting to pause Spotify...")
                self.control_spotify_playback('pause')
            
            elif intent == "next_song":
                print("⏭️ Skipping to next song...")
                self.control_spotify_playback('next')
            
            elif intent == "previous_song":
                print("⏮️ Going to previous song...")
                self.control_spotify_playback('previous')
            
            elif intent == "search_youtube":
                print("🎥 Searching YouTube...")
                self.search_youtube(entity)
            
            elif intent == "search_google":
                print("🔍 Searching Google...")
                self.search_google(entity)
            
            elif intent == "weather":
                print("🌤️ Getting weather information...")
                self.get_weather(entity)
            
            elif intent == "time":
                print("⏰ Getting current time...")
                self.get_current_time()
            
            elif intent == "date":
                print("📅 Getting current date...")
                self.get_current_date()
            
            elif intent == "wikipedia":
                print("📚 Searching Wikipedia...")
                self.search_wikipedia(entity)
            
            elif intent == "news":
                print("📰 Opening news...")
                self.open_news()
            
            elif intent == "open_app":
                print(f"🚀 Opening application: {entity}")
                # Check if it's a special command for YouTube
                if entity.lower() == 'youtube':
                    print("🎥 Opening YouTube in browser...")
                    webbrowser.open('https://www.youtube.com')
                    self.speak("Opening YouTube in your browser")
                # Check if it's a special command for Google
                elif entity.lower() == 'google':
                    print("🔍 Opening Google in browser...")
                    webbrowser.open('https://www.google.com')
                    self.speak("Opening Google in your browser")
                else:
                    self.open_application(entity)
            
            elif "stop" in text or "quit" in text or "exit" in text or "goodbye" in text:
                print("👋 Shutting down...")
                self.speak(Config.GOODBYE_MESSAGE)
                return False
            
            else:
                print(f"❌ Unknown command: {text}")
                self.speak(Config.ERROR_MESSAGE)
            
        except Exception as e:
            print(f"❌ Error processing command: {e}")
            self.logger.error(f"Command processing error: {e}")
            self.speak(Config.RESPONSES['error_occurred'])
        
        return True
        
        return True
    
    def check_wake_word(self, text):
        """Check if any wake word is present"""
        if not text or text in ["timeout", "unknown", "network_error", "error"]:
            return False
        
        text = text.lower().strip()
        for wake_word in Config.WAKE_WORDS:
            if wake_word.lower() in text:
                return True
        return False
    
    def run(self):
        """Main execution loop with improved error handling"""
        print(f"🎤 {Config.ASSISTANT_NAME} is ready!")
        print(f"💬 Wake words: {', '.join(Config.WAKE_WORDS)}")
        print("❗ Remember to say a wake word before each command!")
        print("🔴 Press Ctrl+C to exit\n")
        
        consecutive_errors = 0
        max_errors = 5
        command_without_wake = 0
        
        self.speak("Hello! To give me a command, first say 'hey assistant' or 'hello assistant', then wait for my response before giving your command.")
        
        while True:
            try:
                # Listen for wake word
                text = self.listen(timeout=1)  # Short timeout for wake word detection
                
                if text == "timeout":
                    command_without_wake = 0  # Reset counter on timeout
                    continue
                elif text in ["unknown", "network_error", "error"]:
                    consecutive_errors += 1
                    if consecutive_errors >= max_errors:
                        self.speak("I'm having trouble hearing you. Please check your microphone.")
                        time.sleep(5)
                        consecutive_errors = 0
                    continue
                
                consecutive_errors = 0  # Reset error counter
                
                # Debug print
                print(f"🔍 Checking wake word in: {text}")
                
                # Check for wake word
                if self.check_wake_word(text):
                    print("✅ Wake word detected!")
                    command_without_wake = 0  # Reset counter when wake word is used
                    self.speak(Config.RESPONSES['listening'])
                    
                    # Listen for the actual command with longer timeout
                    print("👂 Waiting for your command...")
                    command = self.listen(timeout=10)
                    
                    if command not in ["timeout", "unknown", "network_error", "error"]:
                        print(f"🎯 Processing command: {command}")
                        continue_running = self.process_command(command)
                        if not continue_running:
                            break
                    else:
                        print(f"❌ Command not recognized: {command}")
                        self.speak(Config.RESPONSES['not_understood'])
                else:
                    print("❌ No wake word detected in:", text)
                    # If it seems like a command but no wake word was used
                    if any(cmd in text.lower() for cmd in ["open", "search", "play", "find", "show", "tell", "what"]):
                        command_without_wake += 1
                        if command_without_wake >= 2:
                            self.speak("Remember to say 'hey assistant' or 'hello assistant' first, then wait for my response before giving your command.")
                            command_without_wake = 0
                    else:
                        command_without_wake = 0
                
            except KeyboardInterrupt:
                self.speak(Config.GOODBYE_MESSAGE)
                break
            except Exception as e:
                self.logger.error(f"Main loop error: {e}")
                time.sleep(1)  # Prevent rapid error loops

def main():
    """Main function with startup checks"""
    print("🚀 Starting Advanced Voice Assistant...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return
    
    try:
        assistant = AdvancedVoiceAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n👋 Assistant stopped by user")
    except Exception as e:
        print(f"❌ Failed to start assistant: {e}")
        logging.error(f"Startup error: {e}")

if __name__ == "__main__":
    main()