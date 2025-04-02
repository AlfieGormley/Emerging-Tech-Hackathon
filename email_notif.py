import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
sender_email = "ewanbeale2003@gmail.com"  # Your Gmail address
receiver_email = "ewanbeale2nd@gmail.com"  # Receiver's email address
password = "nbxz mgju zbcy kzab "  # Your Gmail password or app-specific password
subject = "Test Email from Python"
body = "Hello, this is a test email sent from Python."

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Add body to email
message.attach(MIMEText(body, "plain"))

# Send email using Gmail's SMTP server
try:
    # Set up the server (Gmail SMTP server)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  # Use port 465 for SSL
    server.login(sender_email, password)  # Login to the server
    
    # Send the email
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")

except Exception as e:
    print(f"Error: {e}")

finally:
    server.quit()  # Close the connection to the server
