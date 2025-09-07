import requests
import smtplib
from email.mime.text import MIMEText
import os

API_URL = "https://isealimkariyerkapisi.cbiko.gov.tr/api/ilan/SearchIlanPublic"
OLD_FILE = "old_list.txt"

def get_announcements():
    payload = {
        "krM_ID": 0,
        "searchText": "",
        "il": "0",
        "ilanTuru": "0"
    }
    r = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
    r.raise_for_status()
    data = r.json()
    ilanlar = []
    for ilan in data:
        ilanlar.append(f"{ilan['kurumAdi']} - {ilan['ilanBaslik']} ({ilan['bitTarih']})")
    return ilanlar

def send_email(new_items):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_TO")

    msg = MIMEText("\n".join(new_items), "plain", "utf-8")
    msg["Subject"] = "Yeni Kariyer Kapısı İlan(lar)ı Yayınlandı!"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

def main():
    new_list = get_announcements()

    if os.path.exists(OLD_FILE):
        with open(OLD_FILE, "r", encoding="utf-8") as f:
            old_list = f.read().splitlines()
    else:
        old_list = []

    new_items = [item for item in new_list if item not in old_list]

    if new_items:
        send_email(new_items)
        print("Yeni ilan bulundu:", new_items)
    else:
        print("Yeni ilan yok.")

    with open(OLD_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_list))

if __name__ == "__main__":
    main()
