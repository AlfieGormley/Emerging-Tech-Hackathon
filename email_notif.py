import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import Gen_Data

Curnt_Usage_elc = 1
Prv_Usage_elc = 1
lftm_elc = None
elc_percentage = None
elc_change = None
elc_percentile = 20


def main(score,data):
    #notify council if household is in the bottome x%
    if score < 50:
        council_email(data)
    occupant_email(data)

def council_email():
    creds = email_creds("councilhackaton@gmail.com","EXPENSIVE!!", "this bum using to much enrgy")
    send_email(creds)

def occupant_email(data):
    with open("Email.html", "r", encoding="utf-8") as file:
        template = Template(file.read())
    #content = {"Curnt_Usage_elk": Curnt_Usage_elc, "Prv_Usage_elk": Prv_Usage_elc, }
    html_body = template.render(data)
    creds = email_creds("ewanbeale2nd@gmail.com", "paying too much!", html_body)
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
    message.attach(MIMEText(creds[2], "html"))

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
    data = Gen_Data.main(1)
    main(60,data)