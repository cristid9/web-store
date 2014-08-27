## @package helper
#
#  This file will contain all the functions  that aren't related
#  to a particular module and don't provide crucial functionality.

from flask.ext.mail import Message
from main import mail

def sendMail(subject, sender, recipients, messageBody, messageHtmlBody):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = messageBody
	msg.html = messageHtmlBody
	mail.send(msg)

## We don't wan't to make dirty and log concatenations in app, to avoid this
#  scenario I created this functions that add the remaining parts to the url,
#  in this case the http://.
def generateUrl(hostname, route):
	return "http://" + hostname + route
