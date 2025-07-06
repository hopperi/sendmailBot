from dotenv import load_dotenv
import os

def load_config():
    load_dotenv()
    token = os.getenv('BOT_TOKEN')
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')

    if not token:
        raise ValueError("Добавь BOT_TOKEN в .env")
    if not (email_address and email_password):
        raise ValueError("Добавь EMAIL_ADDRESS и EMAIL_PASSWORD в .env")

    return {
        'BOT_TOKEN': token,
        'EMAIL_ADDRESS': email_address,
        'EMAIL_PASSWORD': email_password,
        'SMTP_SERVER': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'SMTP_PORT': int(os.getenv('SMTP_PORT', 587))
    }
