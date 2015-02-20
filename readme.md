Description
-----------

This is a learning project, its main purpose was to get myself
used to basic principles of web programing like:
  * AJAX
  * DOM manipulation using the jQuery library
  * sending emails using flask-mail
  * using a template engine, jinja2
  * using an ORM, SQLAlchemy in this case
  * learning how to deploy a web application in the cloud
  * implementing a login system

The application can be found at the address `web-store.herokuapp.com`.
Although the app. is pretty easy to use, you will need to know the
admin user and password in order to see all the features of the app,
since only the owner of the server can make an user admin.

```
user: admin
password: 1234
```

Running the app
---------------

If you want to test the app locally you will need to follow
these steps. Make sure that you have a python environment
properly configured. We also recommend you to use a [virtual
environment](https://virtualenv.pypa.io/en/latest/).

1. Clone the application:
 ```
     git clone <link>
 ```

2. Install the requirements:
 ```
     cd src/
     pip install -r requirements.txt
 ```

3. Create an environment variable with the database url.
 Usually, it looks like this `postgresql://cristi:1234@localhost/test_web_store_db`.
 ```
     export DATABASE_URL = "postgresql://cristi:1234@localhost/test_web_store_db"
 ```

4. Create de database:
 ```
     python create_db.py
 ```

5. Run the developement version of the app:
 ```
     python run_dev.py
 ```
