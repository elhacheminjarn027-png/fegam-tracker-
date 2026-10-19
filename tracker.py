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
    response = requests.post(url, data=data)
    print("Telegram API Response:", response.text)

def check_updates():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        print(f"جاري الاتصال بموقع الكلية: {URL}")
        response = requests.get(URL, headers=headers, timeout=15)
        print(f"حالة الاتصال (Status Code): {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # البحث في جميع العناصر المحتملة للعناوين
        posts = soup.find_all(['article', 'h1', 'h2', 'h3', 'h4', 'a'])
        print(f"تم العثور على {len(posts)} عنصر للتحقق منها.")
        
        target_title = None
        for post in posts:
            title = post.get_text(strip=True)
            if len(title) > 10:
                # طباعة العناوين للتشخيص في السجلات
                print(f"عنوان ملقوف: {title[:70]}...")
            for kw in KEYWORDS:
                if kw.lower() in title.lower() and len(title) > 5:
                    print(f"✨ تطابق ناجح! الكلمة المفتاحية: '{kw}' في العنوان: '{title}'")
                    target_title = title
                    break
            if target_title:
                break

        if target_title:
            last_title = ""
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    last_title = f.read().strip()
            
            print(f"العنوان المستهدف: {target_title}")
            print(f"آخر عنوان مسجل: {last_title}")

            if target_title != last_title:
                msg = f"🚨 إعلان جديد خاص بالماستر (اقتصاد تطبيقي وذكاء اصطناعي):\n\n📌 العنوان: {target_title}\n\n🔗 الرابط: {URL}"
                send_msg(msg)
                with open(STATE_FILE, 'w', encoding='utf-8') as f:
                    f.write(target_title)
                print("تم إرسال الإشعار بنجاح إلى تليجرام!")
            else:
                print("نفس العنوان السابق، لا يوجد جديد للتنبيه.")
        else:
            print("❌ لم يتم العثور على أي إعلان يطابق الكلمات المفتاحية في الصفحة الحالية.")

    except Exception as e:
        print(f"خطأ تقني: {e}")

if __name__ == "__main__":
    check_updates()

