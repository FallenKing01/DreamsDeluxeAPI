from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl


def sendEmail(userName, role , email):

    sender_email = "lunabistrobizzchatbot1@gmail.com"
    receiver_email = email  # Replace with actual receiver
    password = "rkfs bzmp cayq rvnd"

    # Define the message subject and from/to details
    message = MIMEMultipart("alternative")
    message["Subject"] = "Welcome to Bistro&Bizz – We're Excited to Have You Onboard!"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Customize email content based on the user's role
    if role == "admin":
        text = f"""\
Hi {userName},

Welcome to Bistro&Bizz! 🎉

As a restaurant owner, you’re joining a community committed to helping your business thrive. Discover tools to streamline operations, enhance customer experience, and connect with industry leaders. We’re here to support your success at every step!

Here's what you can do next:
- Explore business tools designed for restaurant owners
- Connect with other business owners and share insights
- Access exclusive resources to grow your restaurant

For any help, reach out at lunabistrobizzchatbot1@gmail.com. We're here for you!

Best regards,
The Bistro&Bizz Team
https://bistroandbizz.com
"""
        html = f"""\
<html>
  <body>
    <p>Hi <strong>{userName}</strong>,</p>
    <p>Welcome to <strong>Bistro&Bizz</strong>! 🎉</p>
    <p>As a restaurant owner, you’re joining a community committed to helping your business thrive. Discover tools to streamline operations, enhance customer experience, and connect with industry leaders. We’re here to support your success at every step!</p>
    <p>Here's what you can do next:</p>
    <ul>
      <li>Explore business tools designed for restaurant owners</li>
      <li>Connect with other business owners and share insights</li>
      <li>Access exclusive resources to grow your restaurant</li>
    </ul>
    <p>For any help, reach out at <a href="mailto:support@bistroandbizz.com">support@bistroandbizz.com</a>. We're here for you!</p>
    <p>Best regards,<br>The Bistro&Bizz Team</p>
  </body>
</html>
"""

    elif role == "ospatar":
        text = f"""\
Hi {userName},

Welcome to Bistro&Bizz! 🎉

We’re excited to have you as part of our community. As a valued member of the restaurant team, you’ll find great resources to enhance your skills, connect with others in the industry, and keep up with the latest trends. Your growth is our priority!

Here's what you can do next:
- Explore tools designed to support your professional development
- Connect with other restaurant staff and share experiences
- Discover resources that help you excel in your role

If you need any assistance, feel free to reach out at lunabistrobizzchatbot1@gmail.com. We're always happy to help!

Best regards,
The Bistro&Bizz Team
https://bistroandbizz.com
"""
        html = f"""\
<html>
  <body>
    <p>Hi <strong>{userName}</strong>,</p>
    <p>Welcome to <strong>Bistro&Bizz</strong>! 🎉</p>
    <p>We’re excited to have you as part of our community. As a valued member of the restaurant team, you’ll find great resources to enhance your skills, connect with others in the industry, and keep up with the latest trends. Your growth is our priority!</p>
    <p>Here's what you can do next:</p>
    <ul>
      <li>Explore tools designed to support your professional development</li>
      <li>Connect with other restaurant staff and share experiences</li>
      <li>Discover resources that help you excel in your role</li>
    </ul>
    <p>If you need any assistance, feel free to reach out at <a href="mailto:support@bistroandbizz.com">support@bistroandbizz.com</a>. We're always happy to help!</p>
    <p>Best regards,<br>The Bistro&Bizz Team</p>
  </body>
</html>
"""

    elif role == "client":
        text = f"""\
Hi {userName},

Welcome to Bistro&Bizz! 🎉

We’re thrilled to have you join our community! Dive into new culinary adventures, connect with fellow food lovers, and discover exciting dining options. We’re here to make your experience memorable and enjoyable!

Here's what you can do next:
- Explore dining options and new culinary experiences
- Connect with others who share your love for food
- Discover insider tips for the best restaurant experiences

If you ever need help, reach out to us at lunabistrobizzchatbot1@gmail.com. We’re always here to make your journey better!

Bon appétit!
The Bistro&Bizz Team
https://bistroandbizz.com
"""
        html = f"""\
<html>
  <body>
    <p>Hi <strong>{userName}</strong>,</p>
    <p>Welcome to <strong>Bistro&Bizz</strong>! 🎉</p>
    <p>We’re thrilled to have you join our community! Dive into new culinary adventures, connect with fellow food lovers, and discover exciting dining options. We’re here to make your experience memorable and enjoyable!</p>
    <p>Here's what you can do next:</p>
    <ul>
      <li>Explore dining options and new culinary experiences</li>
      <li>Connect with others who share your love for food</li>
      <li>Discover insider tips for the best restaurant experiences</li>
    </ul>
    <p>If you ever need help, reach out to us at <a href="mailto:support@bistroandbizz.com">support@bistroandbizz.com</a>. We’re always here to make your journey better!</p>
    <p>Bon appétit!<br>The Bistro&Bizz Team</p>
  </body>
</html>
"""

    # Attach the appropriate message parts
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Attach the MIMEText objects to the MIMEMultipart message
    message.attach(part1)
    message.attach(part2)

    # Secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def sendResetPasswordEmail(userName, email, reset_code):
    sender_email = "lunabistrobizzchatbot1@gmail.com"
    receiver_email = email
    password = "rkfs bzmp cayq rvnd"

    # Email content with HTML formatting
    subject = "Password Reset Code for Your Bistro&Bizz Account"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <p>Hi {userName},</p>
        <p>We received a request to reset your password. Use the following code to reset your password:</p>
        <div style="text-align: center; margin: 20px 0;">
            <span style="display: inline-block; background-color: black; color: white; 
                        padding: 15px 25px; font-size: 24px; font-weight: bold; 
                        border-radius: 5px;">
                {reset_code}
            </span>
        </div>
        <p>If you did not request this change, you can ignore this email.</p>
        <p>Best,</p>
        <p><strong>Bistro&Bizz Support Team</strong></p>
    </body>
    </html>
    """

    # Create email message
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(MIMEText(body, "html"))  # Set content type to HTML

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Password reset email sent successfully!")
    except Exception as e:
        print("Failed to send email:", str(e))

def sendPasswordResetConfirmationEmail(email):
    sender_email = "lunabistrobizzchatbot1@gmail.com"
    receiver_email = email
    password = "rkfs bzmp cayq rvnd"

    # Email content with HTML formatting
    subject = "Your Bistro&Bizz Password Has Been Reset"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <p>Dear user,</p>
        <p>Your password has been successfully reset. You can now log in to your Bistro&Bizz account using your new password.</p>
        <p>If you did not request this password change, please contact our support team immediately.</p>
        <p>For security reasons, never share your password with anyone.</p>
        <p>Best,</p>
        <p><strong>Bistro&Bizz Support Team</strong></p>
    </body>
    </html>
    """

    # Create email message
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(MIMEText(body, "html"))  # Set content type to HTML

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Password reset confirmation email sent successfully!")
    except Exception as e:
        print("Failed to send email:", str(e))
