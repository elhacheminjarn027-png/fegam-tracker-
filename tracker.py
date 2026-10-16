import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
URL = "https://fegam.uiz.ac.ma/"
STATE_FILE = "last_title.txt"

KEYWORDS = [
    "A2PD", 
    "Master Applied Economics Artificial Intelligence and Policy Design",
    "Applied Economics Artificial Intelligence",
    "Policy Design",
    "Applied Economics", 
    "Artificial Intelligence", 
    "Master", 
    "ماستر"
]

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def check_updates():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        posts = soup.find_all(['h2', 'h3', 'a'])

        target_title = None
        for post in posts:
            title = post.get_text(strip=True)
            if any(kw.lower() in title.lower() for kw in KEYWORDS) and len(title) > 5:
                target_title = title
                break

        if target_title:
            last_title = ""
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    last_title = f.read().strip()

            if target_title != last_title:
                msg = f"🎓 إعلان جديد مهم خاص بماستر A2PD (اقتصاد تطبيقي وذكاء اصطناعي)!\n\nالعنوان: {target_title}\nالرابط: {URL}"
                send_msg(msg)

                with open(STATE_FILE, 'w', encoding='utf-8') as f:
                    f.write(target_title)
                print("تم إرسال إشعار بإعلان مطابق للماستر!")
            else:
                print("ماكاين حتى جديد يخص الماستر حالياً.")
        else:
            print("لم يتم العثور على أي إعلان يطابق كلمات الماستر حالياً.")

    except Exception as e:
        print(f"خطأ: {e}")

if __name__ == "__main__":
    check_updates()
