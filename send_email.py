import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings import Aq_Settings

class SendEmail:

    def email_error(type):
        try:
            sender_email = Aq_Settings.read_settings('User_info', 'email')
            receiver_email = Aq_Settings.read_settings('User_info', 'email')
            password = Aq_Settings.read_settings('User_info', 'password')

            message = MIMEMultipart("alternative")
            message["Subject"] = "Aquarium External Sensor Error"
            message["From"] = sender_email
            message["To"] = receiver_email
            if(type==1):
                error="internal"
            elif(type==0):
                error="external"
            # Create the plain-text and HTML version of your message
            text = """\
            Hi,
            Your %s Sensor is not working.
            Please check the connections"""% (error,)
            html = """\
            <html>
            <body>
                <p>Hi,<br>
                Your %s Sensor is not working.<br>
                Please check the connections
                </p>
            </body>
            </html>
            """% (error,)

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)
            message.attach(part2)

            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )
            print("Email Sent")
        except:
            print("Email Error")

    def email_temp_error(temp, type):
        try:
            sender_email = Aq_Settings.read_settings('User_info', 'email')
            receiver_email = Aq_Settings.read_settings('User_info', 'email')
            password = Aq_Settings.read_settings('User_info', 'password')

            message = MIMEMultipart("alternative")
            message["Subject"] = "Aquarium External Sensor Error"
            message["From"] = sender_email
            message["To"] = receiver_email
            if(type==1):
                error="internal"
            elif(type==0):
                error="external"
            # Create the plain-text and HTML version of your message
            text = """\
            Hi,
            Your %s Temperature is %s°C."""% (error,temp,)
            html = """\
            <html>
            <body>
                <p>Hi,<br>
                Your %s Temperature is %s°C.<br>
                
                </p>
            </body>
            </html>
            """ % (error,temp,)

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)
            message.attach(part2)

            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )
            print("Email Sent")
        except:
            print("Email Error")