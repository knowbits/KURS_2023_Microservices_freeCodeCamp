import smtplib, os, json
from email.message import EmailMessage


# Will use gmail to send emails
# Reads message from the "mp3s" queue
def notification(message):
    # try:
    message = json.loads(message)
    mp3_fid = message["mp3_fid"]

    # NOTE! He recommends to create a DUMMY gmail account:
    sender_address = os.environ.get("GMAIL_ADDRESS")
    sender_password = os.environ.get("GMAIL_PASSWORD")
    receiver_address = message["username"]

    msg = EmailMessage()
    msg.set_content(f"mp3 file_id: {mp3_fid} is now ready!")
    msg["Subject"] = "MP3 Download"
    msg["From"] = sender_address
    msg["To"] = receiver_address

    session = smtplib.SMTP("smtp.gmail.com", 587)
    # Put the SMTP connection int TLS mode: for encrypted communication
    # => Secure IP packets so they cannot be intercepted: Data cannot be read.
    session.starttls()
    session.login(sender_address, sender_password)
    session.send_message(msg, sender_address, receiver_address)
    session.quit()
    print("Mail Sent")


# except Exception as err:
# print(err)
# return err
