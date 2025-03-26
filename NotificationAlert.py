import time
import random
import requests
from twilio.rest import Client  # Twilio for WhatsApp & Calls

# 🔹 Telegram Bot Configuration (Free Unlimited SMS)
TELEGRAM_BOT_TOKEN = "7717557541:AAFBj3Jm2Sp3-MeudL2jucaqeDU56XhWF-o"
TELEGRAM_CHAT_ID = "1092740393"

# 🔹 Twilio API (Free WhatsApp & Calls)
TWILIO_ACCOUNT_SID = "AC99e7e1ff553fc8f07f84ff873d8b5acc"
TWILIO_AUTH_TOKEN = "d74fbc67555db48295933a0f429d2696"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number
YOUR_WHATSAPP_NUMBER = "whatsapp:+918595046356"  # Your verified WhatsApp number
TWILIO_CALL_NUMBER = "+18723122164"  # Twilio phone number


def check_status():
    return random.choice([True, False])  # Simulated True/False condition

# Function to send alert via Telegram
def send_telegram_message():
    message = "🚨 Urgent Alert! Please respond immediately."
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=data)
    print("[INFO] Telegram Alert Sent")

# Function to send WhatsApp alert via Twilio
def send_whatsapp():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body="🚨 Urgent Alert! Please respond.",
        to=YOUR_WHATSAPP_NUMBER
    )
    print("[INFO] WhatsApp Alert Sent", message.sid)

# Function to make a call via Twilio
def make_call():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        twiml='<Response><Say>Urgent alert! Please respond immediately.</Say></Response>',
        from_=TWILIO_CALL_NUMBER,
        to=YOUR_WHATSAPP_NUMBER.replace("whatsapp:", "")  # Convert WhatsApp to normal number
    )
    print("[INFO] Call Alert Sent", call.sid)

random_input= bool(input("enter true or false"))
# Main loop to check status and send notificationswhile  random_input==True:
if random_input == True :
    print("[ALERT] Condition met! Sending notifications...")
    send_telegram_message()
    send_whatsapp()
    make_call()
else:
    print("[INFO] No action required.")
    time.sleep(15)  # Check status again after 15 seconds
