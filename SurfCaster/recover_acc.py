import smtplib,ssl,random,string
from flask_sqlalchemy import SQLAlchemy
from email.mime.text import MIMEText
from db_models import RecoveryCodes, Users
from datetime import datetime, timedelta, timezone
from flask import session
from extensions import db
from sqlalchemy import text, select
from flask import flash

#generates random recovery code tied to user id (email)
def recovery_code(len):
    if len < 4:
        raise ValueError("This code must be at least 4 characters long")
    return ''.join(random.choices(string.ascii_uppercase +string.digits, k = len))




def accountrecover(useremail,code):
   
    #checks if user exists
    user_id=db.session.execute(select(Users.id).where(Users.email==useremail)).scalar_one_or_none()
    print (type(user_id))

    if user_id is None:
        flash("Error: Account does not exist")
        return
    
    #creates time of code creation and expiration time
    creationtime = datetime.now(timezone.utc)
    expirationtime = creationtime+timedelta(minutes=15)

    #opens secret file with email app
    with open("surfcaster/emailpass.txt", "r") as file:
        surfcaster_pass = file.read()


    surfcaster = "surfcaster.app@gmail.com"

    #email formatting
    email_message = f"""
    Please enter the following code into the relevent text field on the application. 
    When entered suuccessfully this will begin the account recovery process.

    {code}


    """

    email_msg = MIMEText(email_message)
    email_msg["Subject"] = "Recover your account"
    email_msg["From"] = surfcaster
    email_msg["To"] =useremail

    #gmail email logic
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(surfcaster, surfcaster_pass)
        server.send_message(email_msg)
        print("recovery email sent, please check your inbox / spam folder")

    #storing code information into db
    dbinfo = RecoveryCodes(
        user_id = user_id,
        code = code,
        time_created = creationtime,
        expiration_time = expirationtime,
        status = True
    )
    db.session.add(dbinfo)
    db.session.commit()
    return 

def code_verifcation(user_id, inputcode):
    code_status = RecoveryCodes.query.filter_by(
        user_id = user_id,
        code = inputcode,
        status = True
    ).first()

    if not code_status:
        return "Code not  valid"
    
    if code_status.expiration_time < datetime.now(timezone.utc):
        code_status.status = False 
        db.session.commit()

    code_status.status = False
    db.session.commit()




    
        