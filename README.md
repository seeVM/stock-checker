## IQOO Stock Checker (Automated Stock Monitor)

A lightweight Python + Playwright tool to automatically monitor stock availability for iQOO smartphones on the official iQOO India Store.
The script checks the product page at fixed intervals, notifies via Telegram, and triggers a sound and browser popup when stock becomes available.

## Features
- Automated periodic stock checks  
- Telegram notifications using bot + chat ID  
- Optional sound alert  
- Playwright browser automation  
- Configurable through `.env`  
- Log output saved locally


## Project Structure
iqoo-stock-watcher/
│── assets/
│   └── pike_pika.mp3         # Optional alert sound
│── scripts/
│   ├── monitor.py            # Main monitoring script
│   ├── telegram_helpers.py   # Telegram notification utility
│   ├── playwright_add_to_cart.py # Browser automation for fast checkout (optional)
│   ├── test_send_env.py      # Test your Telegram token & chat ID
│   └── __init__.py
│── venv/                     # Virtual environment (ignored)
│── start_monitor.sh          # Auto-start helper script
│── requirements.txt
│── .env                      # Your secret config (ignored)
│── .gitignore
│── LICENSE
└── README.md


## Installation

### 1. Clone the repository

git clone https://github.com/seeVM/stock-checker.git/
cd stock-checker


### 2. Create and activate virtual environment

python3 -m venv venv
source venv/bin/activate


### 3. Install dependencies

pip install -r requirements.txt
python3 -m playwright install chromium


### 4. Create `.env`

BOT_TOKEN=your_bot_token
CHAT_ID=your_chat_id
POLL_INTERVAL=15
ALERT_SOUND=assets/pika_pika.mp3


### 5. Test Telegram

python3 -m scripts.test_send_env


---

## Usage

### Run the monitor

python3 -m scripts.monitor


### Or with the helper script

./start_monitor.sh

