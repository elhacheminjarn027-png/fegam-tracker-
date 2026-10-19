import os
import datetime
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
URL = "https://fegam.uiz.ac.ma/"
STATE_FILE = "last_title.txt"
REPORT_FILE = "last_report_date.txt"

KEYWORDS = [
    "A2PD",
    "Master Applied Economics Artificial Intelligence and Policy Design",
    "Applied Economics Artificial Intelligence",
    "Policy Design",
    "Applied Economics",
    "Artificial Intelligence",
    "Master"
]

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, data=data)
    print("Telegram API Response:", response.text)

def check_updates():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        print(f"Connecting to college website: {URL}")
        response = requests.get(URL, headers=headers, timeout=15)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all(['article', 'h1', 'h2', 'h3', 'h4', 'a'])
        
        target_title = None
        for post in posts:
            title = post.get_text(strip=True)
            for kw in KEYWORDS:
                if kw.lower() in title.lower() and len(title) > 5:
                    target_title = title
                    break
            if target_title:
                break

        # 1. Instant Monitoring: If a new announcement appears at any time, notify immediately
        if target_title:
            last_title = ""
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    last_title = f.read().strip()
            
            if target_title != last_title:
                msg = f"🚨 New Important Master Announcement:\n\n📌 Title: {target_title}\n\n🔗 Link: {URL}"
                send_msg(msg)
                with open(STATE_FILE, 'w', encoding='utf-8') as f:
                    f.write(target_title)
                print("Instant alert sent successfully!")

        # 2. Daily Report: Sent every day at 10 PM UTC
        now = datetime.datetime.utcnow()
        current_hour = now.hour
        current_date = now.strftime("%Y-%m-%d")
        
        if current_hour == 22:
            last_report_date = ""
            if os.path.exists(REPORT_FILE):
                with open(REPORT_FILE, 'r', encoding='utf-8') as f:
                    last_report_date = f.read().strip()
            
            if last_report_date != current_date:
                if target_title:
                    report_msg = f"🌙 **Daily Report (10 PM):**\n\nLatest recorded announcement:\n📌 {target_title}\n\n🔗 {URL}"
                else:
                    report_msg = f"🌙 **Daily Report (10 PM):**\n\nNo new updates regarding the Master currently. The bot continues to monitor automatically."
                
                send_msg(report_msg)
                with open(REPORT_FILE, 'w', encoding='utf-8') as f:
                    f.write(current_date)
                print("Daily report sent successfully!")

    except Exception as e:
        print(f"Technical error: {e}")

if __name__ == "__main__":
    check_updates()

