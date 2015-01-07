from .users import (
    UserManager,
    User
)

def finder(userid, request):
    user = request.user_mgr.find_by_id(userid)
    if user is not None:
        return ['user']
    else:
        return None

def try_login(username, password, mgr):
    user = mgr.find_by_username(username)
    if user is not None and user.password == password:
        return user

