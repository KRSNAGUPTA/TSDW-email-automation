import smtplib
import os
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_contacts_from_csv(csv_file):
    contacts = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if len(row) >= 2:
                contacts.append((row[0], row[1]))  
    return contacts

def get_email_body():
    email_body_path = os.getenv("EMAIL_BODY_PATH")
    if not email_body_path or not os.path.exists(email_body_path):
        print("Error: Email body file is missing.")
        return ""
    with open(email_body_path, "r", encoding="utf-8") as file:
        return file.read()

def send_email(to_email, company_name, attachment_path):
    
    sender_email = os.getenv("SENDER_EMAIL")  
    sender_password = os.getenv("EMAIL_APP_PASSWORD") 
    if not sender_email or not sender_password:
        print("Error: Email credentials are missing.")
        return
    
    subject = "Collaboration & Sponsorship Opportunity for Hackanova 4.0, Mumbai"
    # body = f"<p><small>This message was sent at {datetime.now().strftime('%H:%M')}.</small></p>"
    body = get_email_body().replace("{company_name}", company_name)  

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))  

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
        msg.attach(part)
    
    try:
        print(f"Connecting to SMTP server for {to_email}...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        print("Logged in successfully. Sending email...")
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"Email successfully sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

contacts = get_contacts_from_csv("emails.csv")
for email, company in contacts:
    send_email(email, company, "./HACKANOVA 4.0 BROCHURE.pdf")
