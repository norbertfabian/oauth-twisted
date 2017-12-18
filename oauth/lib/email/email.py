
from twisted.mail.smtp import sendmail
from twisted.internet.task import react
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
me = 'martin@miksanik.net'
to = ["miksanik@profires.cz"]

message = MIMEText("This is my super awesome email, sent with Twisted!2")
mime_msg = MIMEMultipart('alternative')
message["Subject"] = "Twisted is great!"
message["From"] = me
message["To"] = ", ".join(to)
mime_msg.attach(message)

def main(reactor):
    d = sendmail(b"exchange.profires.cz",
                 b"martin@miksanik.net",
                 to,
                 message)

    d.addBoth(print)
    return d

react(main)


class Attachment(object):

    def __init__(self, name, path):
        pass


class Email(object):

    HTML_TEMPLATE = ''
    TXT_TEMPLATE = ''

    def __init__(
        self,
        mail_from='',
        subject='',
        html='',
        text='',
        context={}
    ):
        self.mail_from = mail_from
        self.subject = subject
        self.html = html
        self.text = text
        self.attachment = []

    def render(self, context={}):
        self.html = self.renderHTML(context=context)
        self.txt = self.renderTXT(context=context)

    def renderHTML(self, context={}):
        self.html = ''

    def renderTXT(self, context={}):
        self.txt = ''

    def attach(self, attachment):
        pass

    def send(self, to=[]):
        pass
