import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the Voice Assistant"""
    
    # API Keys
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', 'your_spotify_client_id')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', 'your_spotify_client_secret')
    SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_openweather_api_key')
    
    # Speech Recognition Settings
    SPEECH_TIMEOUT = 5  # seconds
    PHRASE_TIME_LIMIT = 10  # seconds
    AMBIENT_NOISE_DURATION = 0.5  # seconds
    
    # Text-to-Speech Settings
    TTS_RATE = 180  # words per minute
    TTS_VOLUME = 0.9  # 0.0 to 1.0
    TTS_VOICE_PREFERENCE = 'female'  # 'male', 'female', or None
    
    # Wake Words
    WAKE_WORDS = [
        'lucky',
        'hey assistant',
        'hello assistant',
        'assistant',
        'hey jarvis',  # Add your custom wake words here
    ]
    
    # Command Confidence Threshold
    CONFIDENCE_THRESHOLD = 0.7
    
    # Default Browser
    DEFAULT_BROWSER = None  # None uses system default
    
    # Spotify Scope
    SPOTIFY_SCOPE = "user-modify-playback-state,user-read-playback-state,user-read-currently-playing"
    
    # Weather Settings
    WEATHER_UNITS = 'metric'  # 'metric', 'imperial', or 'kelvin'
    DEFAULT_CITY = 'New York'  # Default city for weather without location
    
    # Assistant Personality
    ASSISTANT_NAME = "Assistant"
    GREETING_MESSAGE = "Hello! I'm your voice assistant. Remember to say 'hey assistant' or 'hello assistant' before each command. How can I help you today?"
    ERROR_MESSAGE = "I'm sorry, I didn't understand that command. Can you please repeat or try a different way?"
    GOODBYE_MESSAGE = "Goodbye! Have a great day!"
    
    # Debug Settings
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Voice Commands Patterns (NLP)
    COMMAND_PATTERNS = {
        'play_spotify': [
            r'play (.*) on spotify',
            r'spotify play (.*)',
            r'play song (.*)',
            r'play music (.*)',
            r'play (.*) by (.*)',
            r'put on (.*)',
            r'start playing (.*)'
        ],
        'pause_spotify': [
            r'pause music',
            r'pause spotify',
            r'stop music',
            r'stop playing'
        ],
        'next_song': [
            r'next song',
            r'skip song',
            r'next track',
            r'skip this'
        ],
        'previous_song': [
            r'previous song',
            r'last song',
            r'go back',
            r'previous track'
        ],
        'search_youtube': [
            r'search youtube for (.*)',
            r'youtube search (.*)',
            r'search for (.*) on youtube',
            r'find (.*) on youtube',
            r'play (.*) on youtube',
            r'show me (.*) on youtube',
            r'youtube (.*)',
            r'watch (.*) on youtube',
            r'search youtube (.*)$'
        ],
        'search_google': [
            r'search google for (.*)',
            r'google (.*)',
            r'search for (.*)',
            r'find (.*) on google',
            r'look up (.*)',
            r'what is (.*)',
            r'who is (.*)'
        ],
        'weather': [
            r'weather in (.*)',
            r'what is the weather like in (.*)',
            r'weather forecast for (.*)',
            r'how is the weather in (.*)',
            r'weather today in (.*)',
            r'temperature in (.*)'
        ],
        'time': [
            r'what time is it',
            r'current time',
            r'tell me the time',
            r'time please',
            r'what\'s the time'
        ],
        'date': [
            r'what is the date',
            r'today\'s date',
            r'what date is it',
            r'what day is it',
            r'current date'
        ],
        'wikipedia': [
            r'tell me about (.*)',
            r'what is (.*)',
            r'who is (.*)',
            r'wikipedia (.*)',
            r'information about (.*)',
            r'facts about (.*)'
        ],
        'news': [
            r'news',
            r'latest news',
            r'today\'s news',
            r'what\'s in the news',
            r'current events'
        ],
        'open_app': [
            r'open (.*)',
            r'launch (.*)',
            r'start (.*)',
            r'run (.*)'
        ],
        'volume_up': [
            r'volume up',
            r'increase volume',
            r'louder',
            r'turn up volume'
        ],
        'volume_down': [
            r'volume down',
            r'decrease volume',
            r'quieter',
            r'turn down volume'
        ],
        'mute': [
            r'mute',
            r'silence',
            r'turn off sound'
        ]
    }
    
    # Supported Applications for opening
    APPLICATIONS = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'chrome': 'chrome.exe',
        'firefox': 'firefox.exe',
        'word': 'winword.exe',
        'excel': 'excel.exe',
        'powerpoint': 'powerpnt.exe',
        'spotify': 'spotify.exe',
        'discord': 'discord.exe',
        'steam': 'steam.exe',
        'vlc': 'vlc.exe'
    }
    
    # Web Applications
    WEB_APPLICATIONS = {
        'google': 'https://www.google.com',
        'youtube': 'https://www.youtube.com',
        'gmail': 'https://mail.google.com',
        'maps': 'https://maps.google.com',
        'facebook': 'https://www.facebook.com',
        'twitter': 'https://twitter.com',
        'instagram': 'https://www.instagram.com',
        'linkedin': 'https://www.linkedin.com',
        'github': 'https://github.com',
        'amazon': 'https://www.amazon.com',
    }
    
    # Response Templates
    RESPONSES = {
        'spotify_playing': "Playing {song} by {artist} on Spotify",
        'spotify_paused': "Music paused",
        'spotify_resumed': "Music resumed",
        'spotify_next': "Playing next song",
        'spotify_previous': "Playing previous song",
        'spotify_not_found': "Sorry, I couldn't find {query} on Spotify",
        'spotify_no_device': "No active Spotify devices found. Please open Spotify on a device.",
        'youtube_search': "Searching YouTube for {query}",
        'google_search': "Searching Google for {query}",
        'weather_info': "The weather in {location} is {description} with a temperature of {temp}°C, feels like {feels_like}°C",
        'weather_not_found': "Sorry, I couldn't find weather information for {location}",
        'time_response': "The current time is {time}",
        'date_response': "Today is {date}",
        'wikipedia_info': "According to Wikipedia: {summary}",
        'wikipedia_not_found': "Sorry, I couldn't find information about {query} on Wikipedia",
        'app_opened': "Opening {app}",
        'app_not_found': "Sorry, I couldn't find or open {app}",
        'volume_changed': "Volume {action}",
        'news_opening': "Opening latest news for you",
        'listening': "Yes, I'm listening. What can I do for you?",
        'not_understood': "I didn't catch that. Please try again.",
        'error_occurred': "Sorry, there was an error processing your request"
    }
    
    # File Paths
    LOG_FILE = 'assistant.log'
    CACHE_DIR = 'cache'
    
    # Network Settings
    REQUEST_TIMEOUT = 10  # seconds
    MAX_RETRIES = 3
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        missing_keys = []
        
        if cls.SPOTIFY_CLIENT_ID == 'your_spotify_client_id':
            missing_keys.append('SPOTIFY_CLIENT_ID')
        
        if cls.SPOTIFY_CLIENT_SECRET == 'your_spotify_client_secret':
            missing_keys.append('SPOTIFY_CLIENT_SECRET')
        
        if cls.OPENWEATHER_API_KEY == 'your_openweather_api_key':
            missing_keys.append('OPENWEATHER_API_KEY')
        
        if missing_keys:
            print(f"⚠️  Warning: Missing API keys: {', '.join(missing_keys)}")
            print("Some features may not work properly. Please update your .env file.")
        
        return len(missing_keys) == 0
    
    @classmethod
    def print_config_status(cls):
        """Print configuration status"""
        print("\n" + "="*50)
        print("🔧 VOICE ASSISTANT CONFIGURATION STATUS")
        print("="*50)
        
        print(f"✅ Assistant Name: {cls.ASSISTANT_NAME}")
        print(f"✅ Wake Words: {', '.join(cls.WAKE_WORDS)}")
        print(f"✅ TTS Rate: {cls.TTS_RATE} WPM")
        print(f"✅ Debug Mode: {'ON' if cls.DEBUG_MODE else 'OFF'}")
        
        # API Status
        print("\n🔑 API KEYS STATUS:")
        print(f"{'✅' if cls.SPOTIFY_CLIENT_ID != 'your_spotify_client_id' else '❌'} Spotify: {'Configured' if cls.SPOTIFY_CLIENT_ID != 'your_spotify_client_id' else 'Missing'}")
        print(f"{'✅' if cls.OPENWEATHER_API_KEY != 'your_openweather_api_key' else '❌'} Weather: {'Configured' if cls.OPENWEATHER_API_KEY != 'your_openweather_api_key' else 'Missing'}")
        
        # Features Status
        print("\n🎯 AVAILABLE FEATURES:")
        print("✅ Speech Recognition")
        print("✅ Text-to-Speech")
        print("✅ Google Search")
        print("✅ YouTube Search")
        print("✅ Wikipedia Search")
        print("✅ Time & Date")
        print("✅ Application Control")
        print(f"{'✅' if cls.SPOTIFY_CLIENT_ID != 'your_spotify_client_id' else '❌'} Spotify Control")
        print(f"{'✅' if cls.OPENWEATHER_API_KEY != 'your_openweather_api_key' else '❌'} Weather Information")
        
        print("="*50 + "\n")

# Make sure Config is available when importing from this module
__all__ = ['Config']