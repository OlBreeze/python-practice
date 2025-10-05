"""
Redis — User Session Management
"""

import redis
import json
from datetime import datetime, timedelta

# Підключення до Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Час життя сесії (у секундах) — 30 хвилин
SESSION_TTL = 30 * 60


def create_session(user_id: str, session_token: str):
    """
    Створює нову сесію користувача та зберігає її у Redis.
    """
    session_data = {
        "user_id": user_id,
        "session_token": session_token,
        "login_time": datetime.now().isoformat(),
        "last_activity": datetime.now().isoformat()
    }

    # Зберігаємо як JSON з TTL (Time To Live)
    r.setex(f"session:{user_id}", SESSION_TTL, json.dumps(session_data))
    print(f"✅ Session created for user {user_id}")


def get_session(user_id: str):
    """
    Отримує активну сесію користувача з Redis.
    """
    data = r.get(f"session:{user_id}")
    if data:
        return json.loads(data)
    else:
        print(f"⚠️ No active session for user {user_id}")
        return None


def update_session_activity(user_id: str):
    """
    Оновлює час останньої активності користувача і подовжує TTL.
    """
    session = get_session(user_id)
    if not session:
        return

    session["last_activity"] = datetime.now().isoformat()
    r.setex(f"session:{user_id}", SESSION_TTL, json.dumps(session))
    print(f"🔄 Session for user {user_id} updated")


def delete_session(user_id: str):
    """
    Видаляє сесію користувача (наприклад, при виході із системи).
    """
    r.delete(f"session:{user_id}")
    print(f"🗑️ Session for user {user_id} deleted")


# ===========================
if __name__ == "__main__":
    user = "user_123"
    token = "abc123xyz"

    create_session(user, token)          # Create
    print(get_session(user))             # Read
    update_session_activity(user)        # Update
    print(get_session(user))
    delete_session(user)                 # Delete
    print(get_session(user))             # Check deleted
