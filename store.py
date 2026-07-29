import json, os

DATA_FILE = "data.json"

def load():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE) as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def reset():
    data = load()
    for uid in data:
        data[uid]["daily_count"] = 0
        data[uid]["daily_words"] = {}
        data[uid]["sent_message_today"] = False
    save(data)

def record_swear(user_id, username, avatar_url, word):
    data = load()
    if user_id not in data:
        data[user_id] = {"username": username, "avatar_url": avatar_url, "daily_count": 0, "daily_words": {}, "total_count": 0, "clean_streak": 0, "sent_message_today": True}
    entry = data[user_id]
    entry["username"] = username
    entry["avatar_url"] = avatar_url
    entry["daily_count"] += 1
    entry["total_count"] += 1
    entry["sent_message_today"] = True
    entry["daily_words"][word] = entry["daily_words"].get(word, 0) + 1
    save(data)

def mark_active(user_id, username, avatar_url):
    data = load()
    if user_id not in data:
        data[user_id] = {"username": username, "avatar_url": avatar_url, "daily_count": 0, "daily_words": {}, "total_count": 0, "clean_streak": 0, "sent_message_today": False}
    data[user_id]["sent_message_today"] = True
    data[user_id]["username"] = username
    data[user_id]["avatar_url"] = avatar_url
    save(data)
