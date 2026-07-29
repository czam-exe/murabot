import os

TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_BOT_TOKEN")
RESET_HOUR = 15
RESET_MINUTE = 59
FINE_PER_SWEAR = 50

BAD_WORDS = [
    "tangina mo", "potangina mo", "putangina mo",
    "tangina", "putangina", "potangina",
    "pota", "kingina", "ampota",
    "taina", "taena",
    "tarantado", "tado", "bobo",
    "gago", "tanga", "8080"
]
