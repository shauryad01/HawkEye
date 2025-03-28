import os
import time
import random
import requests
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables
load_dotenv()

# 🔹 Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
TWILIO_CALL_NUMBER = os.getenv("TWILIO_CALL_NUMBER")
YOUR_WHATSAPP_NUMBER = os.getenv("YOUR_WHATSAPP_NUMBER")

# 🔹 Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 🔹 SendGrid API (For Email)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_API_URL = os.getenv("SENDGRID_API_URL")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Function to check the condition (Simulated)
def check_status():
    return random.choice([True, False])

# Function to send Telegram alert
def send_telegram():
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    message = {"chat_id": TELEGRAM_CHAT_ID, "text": "🚨 Urgent Alert! Please respond immediately."}
    response = requests.post(telegram_url, json=message)
    print("[INFO] Telegram Alert Sent:", response.status_code)

# Function to send WhatsApp alert via Twilio
def send_whatsapp():
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body="🚨 Urgent Alert! Please respond.",
        to=YOUR_WHATSAPP_NUMBER
    )
    print("[INFO] WhatsApp Alert Sent:", message.sid)

# Function to make a call via Twilio
def make_call():
    call = client.calls.create(
        twiml="<Response><Say>Urgent alert! Please respond immediately.</Say></Response>",
        from_=TWILIO_CALL_NUMBER,
        to=YOUR_WHATSAPP_NUMBER.replace("whatsapp:", "")  # Convert WhatsApp to a normal number
    )
    print("[INFO] Call Alert Sent:", call.sid)

# Function to send email via SendGrid
def send_email():
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "personalizations": [{"to": [{"email": EMAIL_RECEIVER}]}],
        "from": {"email": EMAIL_SENDER},
        "subject": "🚨 Urgent: Action Required",
        "content": [{"type": "text/plain", "value": "The system detected an issue. Please respond immediately."}]
    }
    response = requests.post(SENDGRID_API_URL, json=data, headers=headers)
    print("[INFO] Email Alert Sent:", response.status_code, response.text)

# Function to check if the authority has responded (Simulated API Check)
def check_response():
    try:
        response = requests.get("https://your-server.com/check-response")  # Replace with actual API
        return response.json().get("response_received", False)
    except Exception as e:
        print("[ERROR] Checking response failed:", e)
        return False

# Main loop to check status and send notifications
while True:
    if check_status():
        print("[ALERT] Condition met! Sending notifications...")

        while not check_response():
            send_telegram()   
            send_whatsapp()   
            send_email()      
            make_call()       
            time.sleep(15)    # Wait 15 sec before sending again

        print("[INFO] Response received. Stopping notifications.")
    else:
        print("[INFO] No action required.")

    time.sleep(15)  # Check status again after 15 sec
