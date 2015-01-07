from pyramid.response import Response
from pyramid.view import (
    view_config,
    forbidden_view_config,
    HTTPFound
)

from pyramid.security import (
    remember,
    forget
)

from .users import (UserManager, User)

from .security import (try_login)

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )


@view_config(route_name='home', renderer='templates/pyramid.pt')
def my_view(request):
    print request.user
    return {'project': 'jira_connect'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_jira_connect_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login_view(request):
    login_url = request.resource_url(request.context, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'

    came_from = request.params.get('came_from', referrer)
    message = ''
    password = ''
    login = ''
    if request.method == 'POST':
        login = request.params['login']
        password = request.params['password']
        user = try_login(login, password, request.user_mgr)
        if user is not None:
            headers = remember(request, login)
            return HTTPFound(location=came_from, headers=headers)
        message = 'Login failed.'

    return dict(
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password
    )

@view_config(name="logout")
def logout_view(request):
    headers = forget(request)
    return HTTPFound(location=request.application_url, headers=headers)



def __validate_registration_request(request):
    errors = []
    if request.params['password'] != request.params['confirm_password']:
        errors.append('Password does not match.')
    existing = request.user_mgr.find_by_username(request.params['username'])
    if existing is not None:
        errors.append('Username is already in use.')
    return errors

@view_config(name='register', renderer='templates/register.pt')
def register_view(request):
    message = ''

    if request.method == 'POST':
        errors = __validate_registration_request(request)
        if len(errors) == 0:
            user = User()
            user.fullname = request.params['fullname']
            user.username = request.params['username']
            user.password = request.params['password']
            request.user_mgr.save(user)
        else:
            message = 'Form is invalid.'

    return dict(
        message=message,
        username=request.params.get('username', ''),
        fullname=request.params.get('fullname', ''),
        password=request.params.get('password', ''),
        confirm_password=request.params.get('confirm_password', '')
    )

@view_config(name='integrations', renderer='templates/integrations.pt')
def integrations_view(request):
    trellos = request.user.trello_accts
    jiras = request.user.jira_accts
    return dict(
        trellos=trellos,
        jiras=jiras
    )