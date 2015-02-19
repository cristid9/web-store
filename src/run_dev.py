## Use this module to start the developement version of
#  the app.
from app.views import *
from app.main import app

app.debug = True

if __name__ == '__main__':
	app.run()
