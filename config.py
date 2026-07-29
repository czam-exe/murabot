import os

TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_BOT_TOKEN")
RESET_HOUR = 15    # 11:59 PM PH time = 15:59 UTC
RESET_MINUTE = 59
FINE_PER_SWEAR = 50

BAD_WORDS = [
    "tangina", "tangina mo", "putangina", "pota", "kingina",
    "gago", "tanga", "ampota", "potangina mo", "taina", "taena"
]
