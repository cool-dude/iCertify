import os
import sys
import smtplib
import mimetypes
import threading
import traceback as tb
from Queue import Queue

from email import encoders
from email.MIMEMultipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.MIMEText import MIMEText
from email.mime.image import MIMEImage

email_queue = Queue()
from lib.config import config


class EmailSender:
    email = config.get('email-sender', 'email')
    passowrd = config.get('email-sender', 'password')
    port = config.get('email-sender', 'port')
    pop_forwarding = config.get('email-sender', 'pop_forwarding')


class SMTPEmailer():

    def __init__(self, recepient, subject, message, attachments):
        self.sender = EmailSender()
        self.recepient = recepient
        self.subject = subject
        self.message = message
        self.attachments = attachments

    def send(self):
        msg = MIMEMultipart()
        msg['From'] = self.sender.email
        msg['To'] = ""
        msg['Subject'] = self.subject

        recepients = [rec.strip() for rec in self.recepient.replace(',', ';').split(';') if rec.strip()]

        msg.attach(MIMEText(self.message, 'html', 'utf-8'))
        if self.attachments:
            for path in self.attachments:
                ctype, encoding = mimetypes.guess_type(path)
                if ctype is None or encoding is not None:
                    # No guess could be made, or the file is encoded (compressed), so
                    # use a generic bag-of-bits type.
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                with open(path, 'rb') as fp:
                    # Note: we should handle calculating the charset
                    attachment = MIMEBase(maintype, subtype)
                    attachment.set_payload(fp.read())
                    encoders.encode_base64(attachment)
                    attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(path))
                    msg.attach(attachment)
        email_queue.put(msg)

        def _send_email_thread():
            msg = email_queue.get()
            mailserver = smtplib.SMTP(self.sender.pop_forwarding, self.sender.port)
            # secure our email with tls encryption
            if not 'rediff' in self.sender.email.lower():
                # identify ourselves to smtp gmail client
                mailserver.ehlo()
                mailserver.starttls()
            # re-identify ourselves as an encrypted connection
            mailserver.ehlo()
            mailserver.login(self.sender.email, self.sender.password)
            mailserver.sendmail(self.sender.email, recepients, msg.as_string())
            mailserver.quit()
            sys.stdout.write("Email sent to : %s" % (recepients))

        email_thread = threading.Thread(target=_send_email_thread, )
        email_thread.setDaemon(True)
        email_thread.start()


def send_email(recepient, subject, message, attachments, parameters):
    subject = subject % (parameters)
    message = message % (parameters)
    # send an email using communication app
    try:
        mail = SMTPEmailer(recepient, subject, message, attachments)
        mail.send()
        sys.stdout.write("Please check, Email sent to %s\n" % (recepient))
    except Exception as e:
        print >> sys.stderr, e
        print >> sys.stderr, tb.format_exc()
