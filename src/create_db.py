from app.main import db
from app.user import *
from app.product import *
from app.cart import *

if __name__ == "__main__":
	db.create_all()
