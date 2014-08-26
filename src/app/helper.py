## @package helper
#
#  This file will contain all the functions and decorator that aren't related
#  to a particular module and don't provide crucial functionality.

from flask.ext.mail import Mail
from main import mail

def sendMail(subject, sender, recipients, messageBody, messageHtmlBody):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = messageBody
	msg.html = messageHtmlBody
	mail.send(msg)
