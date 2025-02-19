import requests
import json
import time
from telegram import Bot

# Load Configuration
with open("config.json", "r") as f:
    CONFIG = json.load(f)

# API Endpoints
DEXSCREENER_API = "https://api.dexscreener.com/latest/dex/tokens"
BONKBOT_API = "https://api.bonkbot.com/trade"
TG_BOT_TOKEN = CONFIG["telegram"]["bot_token"]
TG_CHAT_ID = CONFIG["telegram"]["chat_id"]

# Initialize Telegram Bot
tg_bot = Bot(token=TG_BOT_TOKEN)

def fetch_tokens():
    """Fetch token data from DexScreener API."""
    response = requests.get(DEXSCREENER_API)
    if response.status_code == 200:
        return response.json().get("pairs", [])
    return []

def check_valid_token(token):
    """Apply filters to validate the token."""
    if token["baseToken"]["symbol"] in CONFIG["blacklist"]["coins"]:
        return False
    if token["liquidity"]["usd"] < CONFIG["filters"]["min_liquidity"]:
        return False
    if token["volume"]["h24"] < CONFIG["filters"]["min_volume"]:
        return False
    return True

def trade_token(token, action):
    """Execute trade via Bonkbot API."""
    payload = {
        "token": token["pairAddress"],
        "action": action,
        "amount": CONFIG["trading"]["max_trade_amount"]
    }
    response = requests.post(BONKBOT_API, json=payload)
    return response.json()

def send_telegram_message(message):
    """Send a message to Telegram."""
    tg_bot.send_message(chat_id=TG_CHAT_ID, text=message)

def main():
    while True:
        print("Fetching tokens...")
        tokens = fetch_tokens()
        
        for token in tokens:
            if check_valid_token(token):
                trade_response = trade_token(token, "buy")
                send_telegram_message(f"Bought {token['baseToken']['symbol']} at {token['priceUsd']}\nResponse: {trade_response}")
                
        print("Sleeping for", CONFIG["update_interval"], "seconds...")
        time.sleep(CONFIG["update_interval"])

if __name__ == "__main__":
    main()

def test_trade():
    token_address = input("Enter token address to test buy order: ")
    trade_response = trade_token({"pairAddress": token_address}, "buy")
    print("Trade Response:", trade_response)

if __name__ == "__main__":
    test_trade()
