import os, time, webbrowser
import requests
from bs4 import BeautifulSoup
from scripts.telegram_helpers import send_telegram

PRODUCT_URL = "https://shop.iqoo.com/in/product/2038?skuId=8246"
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "15"))
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID", "")
ALERT_SOUND = os.getenv("ALERT_SOUND", "")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def is_in_stock(html: str) -> bool:
    low = html.lower()
    if "out of stock" in low:
        return False

    if "add to cart" in low or "buy now" in low:
        return True

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text().lower()

    if "out of stock" in text:
        return False

    if "buy now" in text or "add to cart" in text:
        return True

    return False

def play_sound(path: str):
    import shlex, subprocess
    try:
        cmd = f"ffplay -nodisp -autoexit -loglevel quiet {shlex.quote(path)}"
        subprocess.Popen(shlex.split(cmd))
    except Exception as e:
        print("sound error:", e)

def main():
    session = requests.Session()
    print("Monitoring:", PRODUCT_URL, "every", POLL_INTERVAL, "seconds")
    try:
        while True:
            try:
                r = session.get(PRODUCT_URL, headers=HEADERS, timeout=15)
            except Exception as e:
                print("HTTP error:", e)
                time.sleep(POLL_INTERVAL)
                continue

            if is_in_stock(r.text):
                msg = f"PRODUCT MAY BE IN STOCK: {PRODUCT_URL}"
                print(msg)

                if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
                    status, resp = send_telegram(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, msg)
                    print("Telegram status:", status)
                if ALERT_SOUND:
                    play_sound(ALERT_SOUND)
                # spawn the playwright add-to-cart script so it opens a browser and tries to click
                import subprocess, sys, os
                script_path = os.path.join(os.getcwd(), "scripts", "playwright_add_to_cart.py")
                subprocess.Popen([sys.executable, script_path])
                # keep monitor stopping behavior if you want; we break so you can attend to checkout
                break

                if ALERT_SOUND:
                    play_sound(ALERT_SOUND)

                webbrowser.open(PRODUCT_URL)
                b

            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S"), "- still out of stock")

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("Stopped by user")

if __name__ == "__main__":
    main()
