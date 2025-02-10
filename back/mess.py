import os
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr

def send_email(to_email, attachment_path, end):
    # Load environment variables
    load_dotenv()

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    from_email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')

    subject = f'Summary Report for {end}'
    body = """Greetings from MoneyMaster!\n\nPlease see your attached financial report.\n\nBest regards,\nMoneyMaster Team"""

    display_name = "MoneyMaster"
    login = from_email

    # Create a MIME message
    msg = MIMEMultipart()
    msg['From'] = formataddr((display_name, from_email))
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))
    
    # Open the file to be sent
    with open(attachment_path, "rb") as attachment:
        # Instance of MIMEBase and named as part
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        
        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)
        
        # Add header to the attachment
        part.add_header('Content-Disposition', f"attachment; filename= {attachment_path}")
        
        # Attach the instance 'part' to the message
        msg.attach(part)
    
    # Create SMTP session for sending the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Enable security
        server.login(login, password)  # Login to the email server
        text = msg.as_string()  # Convert the message to a string
        server.sendmail(from_email, to_email, text)  # Send the email

# Example usage:
# send_email("recipient@example.com", "path/to/attachment.pdf", "2024-06-30")
