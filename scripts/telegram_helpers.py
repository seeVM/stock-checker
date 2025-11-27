# scripts/telegram_helpers.py
import requests

def send_telegram(token: str, chat_id: str, text: str):
    """
    Send a simple Telegram message via the Bot API.
    Returns (status_code, response_text) on success, or (None, error_string) on exception.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": chat_id, "text": text}, timeout=10)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

def get_updates(token: str):
    """
    Fetch recent updates for the bot (useful to obtain chat_id after you message the bot).
    Returns parsed JSON (dict) on success, or raises requests exceptions.
    """
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()
