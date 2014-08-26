## @package decorators
#
#  This file will contain the definition of the all decorators used in the 
#  application.

from threading import Thread

## Use this decorator to asynchronously do te job of a function.
#
#  @param func The function to decorate
def async(func):
	def wrapper(*args, **kwargs):
		t = Thread(target=func, args=args, kwargs=kwargs)
		t.start()
	return wrapper

