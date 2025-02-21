import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = "smtp.elasticemail.com"
EMAIL_PORT = 2525
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
    print("Error: EMAIL_HOST_USER or EMAIL_HOST_PASSWORD is not set!")
else:
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        print("Login successful!")
        server.quit()
    except Exception as e:
        print("Login failed:", e)
