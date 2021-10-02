import smtplib
from settings import Aq_Settings

class SendEmail:

    def email():
        sent_from = Aq_Settings.read_settings('User_info', 'email')
        to = Aq_Settings.read_settings('User_info', 'email')
        subject = 'OMG Super Important Message'
        body = 'Hey, whats up?\n\n- You'

        email_text = """\
        From: %s
        To: %s
        Subject: %s
        %s
        """ % (sent_from, ", ".join(to), subject, body)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login( Aq_Settings.read_settings('User_info', 'email'),  Aq_Settings.read_settings('User_info', 'password'))
            server.sendmail(sent_from, to, email_text)
            server.close()

            print ('Email sent!')
        except:
            print ('Something went wrong...')