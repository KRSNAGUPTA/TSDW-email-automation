import smtplib
import os
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def get_contacts_from_csv(csv_file):
    contacts = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if present
        for row in reader:
            if len(row) >= 2:
                contacts.append((row[0], row[1]))  # Email in first column, company name in second
    return contacts

def send_email(to_email, company_name, attachment_path):
    sender_email = "tcet.hackanova@gmail.com"  # Updated sender email
    sender_password = "wcsf peqc eljo whvg"   # Replace with your app password
    
    subject = "Collaboration & Sponsorship Opportunity for Hackanova 4.0, Mumbai"
    
    body = f"""
    Warm Greetings,
    
    We are pleased to announce <strong>Hackanova 4.0</strong>, 4th edition of our flagship 36-hour <strong>National Level hackathon</strong> hosted by the <strong>TCET Student Development and Welfare Association (TSDW)</strong>. Hackanova 4.0 is designed to test the skills of the brightest minds in technology and will be held from <strong>21st to 22nd February 2025.</strong>
    
    The theme of the event is "<strong>Redefining the Norms through Intelligence.</strong>"
    Hackanova 4.0 focuses on trending technologies like <strong>Artificial Intelligence</strong>, <strong>Machine Learning</strong>, and <strong>Blockchain</strong>, empowering participants to address real-world challenges. The event will feature an <strong>online selection round on Devfolio</strong>, followed by an <strong>offline finale at Thakur College of Engineering and Technology, Mumbai.</strong>
    
    <strong>Event Highlights:</strong>
    - <strong>Dates:</strong> 21st and 22nd February 2025
    - <strong>Duration:</strong> 36 hours
    - <strong>Participants:</strong> Top tech enthusiasts from institutions across India
    
    <strong>Why collaborate with us?</strong>
    - Expected registration of 850+ on Devfolio based on past engagement we received for previous editions.
    - Prizes worth ₹ 80,000+ to be awarded.
    - Option to access the contact details of participants and winners for further interaction, funding opportunities, and prospecting for interns.
    
    <strong>About TCET and TSDW:</strong>
    TCET is a graded autonomous institute affiliated with the University of Mumbai and recognized by AICTE. It has a strong legacy of hosting impactful events like Hackanova, Zephyr, and Leadership Summits, managed by the student-driven TSDW.
    
    <strong>Previous Sponsors:</strong>
    Hackanova has been fortunate to collaborate with industry-leading brands in its previous editions, including:
    <strong>Replit, Taskade, Interview Buddy, Solana, Polygon, Digital Ocean, Filecoin, Devfolio, Newton School, FOSS United, .xyz, Nova Nova</strong>
    
    We are truly inspired by your company's unwavering commitment to innovation and believe a partnership with {company_name} would elevate Hackanova 4.0 to even greater heights. We are looking for both monetary and in-kind sponsorship and would be grateful to have you as part of this event to make it more impactful.
    
    Looking forward to your response!
    
    Best regards,
    <strong>TSDW-Technical Team.</strong>
    <strong>Contact us:</strong> Dhyey Swadia – +91 9892439017
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
        msg.attach(part)
    
    try:
        print("Process started...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        print("sending Login request...")
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        print("Collected all the data....sending now")
        server.quit()
        print(f"Email successfully sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example Usage
contacts = get_contacts_from_csv("emails.csv")
for email, company in contacts:
    send_email(email, company, "./HACKANOVA 4.0 BROCHURE.pdf")
