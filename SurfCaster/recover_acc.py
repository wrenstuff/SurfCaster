import smtplib
from email.mime.text import MIMEText

def accountrecover(useremail):

    with open("surfcaster/emailpass.txt", "r") as file:
        surfcaster_pass = file.read()


    surfcaster = "surfcaster.app@gmail.com"


    email_message = """
    test message
    """

    email_msg = MIMEText(email_message)
    email_msg["Subject"] = "This is a Subject"
    email_msg["From"] = surfcaster
    email_msg["To"] =useremail

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(surfcaster, surfcaster_pass)
        server.send_message(email_msg)
    