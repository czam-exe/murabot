import os

TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_BOT_TOKEN")
RESET_HOUR = 15
RESET_MINUTE = 59
FINE_PER_SWEAR = 50

BAD_WORDS = [
    # Multi-word first (longest match priority)
    "putangina mo", "potangina mo", "tangina mo", "fuck you",
    "mamatay ka na",
    # Single words
    "putangina", "potangina", "tangina",
    "ampota", "kingina", "pota",
    "taena", "taina",
    "tarantado", "rantado",
    "gago", "tanga", "bobo", "tado",
    "8080", "pakyu",
    "fuck", "shit", "bitch", "asshole", "damn", "hell",
    "hayop", "haup"
]
