## @package helper
#
#  This file will contain all the functions  that aren't related
#  to a particular module and don't provide crucial functionality.

from flask.ext.mail import Message
from main import mail, app
from decorators import async

## Use this function to send an email asynchronously.
#
#  @param subject A string representing the subject of
#         the mail.
#  @param sender A string representing the email address
#         of the sender.as
#  @param recipients A list of strings representing the
#         recipients of the email.
#  @param messageBody The text body of the email.
#  @param messageHtmlBody The html body of the mail.
#
#  @return void It doesn't return anything
@async
def sendMail(subject, sender, recipients, messageBody, messageHtmlBody):
	with app.app_context():
		msg = Message(subject, sender=sender, recipients=recipients)
		msg.body = messageBody
		msg.html = messageHtmlBody
		mail.send(msg)


## We don't wan't to make dirty and log concatenations in app, to avoid this
#  scenario I created this functions that add the remaining parts to the url,
#  in this case the http://.
def generateUrl(hostname, route):
	return "http://" + hostname + route


## Since the process of flashing all the errors raised when validating a form
#  takes quite more lines of code, a helper that does that for us is a very
#  convinient sollution.
# 
#  @param errors Dictionary of the form `<field>:<errors>`.
#  @param flash The function used to flash errors.
def flashErrors(errors, flash):
	for field in errors:
		for error in errors[field]:
			flash(error)


## Use this helper function to compute the maximum number of pages
#  that can exists, taking into account the number of products
#  that should be displayed on every page.
#
#  @param items The total number of items. For example, the total
#         number of products in a given category.
#  @param items_per_page The maximum number of items
#         that can be displayed ona page.
#
#  @return int The maximum number of pages.
def get_max_pages(items, items_per_page):
	max_pages = items / items_per_page
	if items % items_per_page > 0:
		max_pages += 1
	return  max_pages
