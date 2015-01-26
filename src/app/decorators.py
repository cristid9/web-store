## @package decorators
#
# This file will contain the definition of the all decorators used in the
#  application.

from threading import Thread
from flask import g, redirect, url_for
from functools import wraps

## Use this decorator to asynchronously do te job of a function.
#
#  @param func The function to decorate
def async(func):
    def wrapper(*args, **kwargs):
        t = Thread(target=func, args=args, kwargs=kwargs)
        t.start()

    return wrapper

## Use this decorator to allow only user with a particular state on page.
#  For instance, only admins cand access the adding products page.
#
#  @param kwargs A dictionary of variable arguments, consisting in the
#         users state, desire state and the route to redirect the user if
#         it doesn't have that desired state.
def isAdmin(**kwargs):
    route = kwargs['route']
    state = kwargs['desiredState']

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if g.user.is_admin():
                return redirect(url_for(route))
            return func(*args, **kwargs)

        return wrapper

    return decorator
