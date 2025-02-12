import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time

# Configuration
WEBSITE_URL = "https://www.depechemode.com"  # Official Depeche Mode website
CHECK_INTERVAL = 86400  # Check every 24 hours (in seconds)
EMAIL_FROM = "your_email@gmail.com"  # Your email address
EMAIL_TO = "your_email@gmail.com"  # Recipient email address
EMAIL_PASSWORD = "your_email_password"  # Your email password or app-specific password
SMTP_SERVER = "smtp.gmail.com"  # SMTP server for Gmail
SMTP_PORT = 587  # SMTP port for Gmail

# Function to check for tour announcements
def check_for_tour_announcement():
    try:
        response = requests.get(WEBSITE_URL)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, "html.parser")

        # Look for specific keywords or elements indicating a tour announcement
        # Update the selector based on the website's structure
        tour_announcement = soup.find(text=lambda text: text and "tour" in text.lower())

        if tour_announcement:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking website: {e}")
        return False

# Function to send an email
def send_email():
    subject = "Depeche Mode Tour Announcement!"
    body = "Depeche Mode has announced a new tour! Check it out: " + WEBSITE_URL

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main loop to check periodically
def main():
    while True:
        print("Checking for tour announcement...")
        if check_for_tour_announcement():
            print("Tour announced! Sending email...")
            send_email()
            break  # Exit loop after sending email
