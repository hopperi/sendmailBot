import smtplib
from email.mime.text import MIMEText
import asyncio
import logging

async def send_email(from_email: str, password: str, to_email: str, subject: str, message: str, 
                    smtp_server: str, smtp_port: int):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    loop = asyncio.get_event_loop()
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            await loop.run_in_executor(None, server.starttls)
            await loop.run_in_executor(None, lambda: server.login(from_email, password))
            await loop.run_in_executor(None, lambda: server.sendmail(from_email, to_email, msg.as_string()))
        logging.info(f"Письмо отправлено на {to_email}")
    except Exception as e:
        logging.error(f"Ошибка SMTP: {e}")
        raise
