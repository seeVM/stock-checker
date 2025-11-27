from scripts.telegram_helpers import send_telegram, get_updates
import os, json, sys

token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

if not token:
    print("ERROR: BOT_TOKEN not set in environment", file=sys.stderr)
    sys.exit(1)

if chat_id:
    status, resp = send_telegram(token, chat_id, "Test message from iqoo-stock-watcher")
    print("send_telegram status:", status)
    print(resp)
else:
    print(json.dumps(get_updates(token), indent=2))
