import requests
import logging
from config import BOT_TOKEN, CHAT_ID, SEND_ALERTS

# Set up logging
logger = logging.getLogger(__name__)

def send_telegram_alert(message):
    """
    Send a Telegram alert to the specified chat ID.
    Args:
    - message: str - The message to send.
    """
    if SEND_ALERTS and CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {'chat_id': CHAT_ID, 'text': message}
            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                logger.info(f"Alert sent to Telegram chat {CHAT_ID}")
            else:
                logger.error(f"Failed to send alert. Response: {response.text}")
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {e}")
