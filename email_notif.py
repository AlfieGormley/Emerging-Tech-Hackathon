import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def main(score):
    if score < 50:
        creds = email_creds("councilhackaton@gmail.com","EXPENSIVE!!", "this bum using to much enrgy")
        send_email(creds)
    creds = email_creds("ewanbeale2nd@gmail.com", "paying too much!", "stop it ")
    send_email(creds)

def email_creds(receiver, sub, bdy):
    receiver_email = receiver  # Receiver's email address
    subject = sub
    body = bdy

    return receiver_email, subject, body

def send_email(creds):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = "ewanbeale203@gmail.com"
    message["To"] = creds[0]
    message["Subject"] = creds[1]

    # Add body to email
    message.attach(MIMEText(creds[2], "plain"))

    # Send email using Gmail's SMTP server
    try:
        # Set up the server (Gmail SMTP server)
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  # Use port 465 for SSL
        server.login("ewanbeale2003@gmail.com", "nbxz mgju zbcy kzab" )  # Login to the server
        
        # Send the email
        server.sendmail("ewanbeale2003@gmail.com", creds[0], message.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server.quit()  # Close the connection to the server

if __name__ == "__main__":
    main(40)