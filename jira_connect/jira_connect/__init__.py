from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from pyramid.security import unauthenticated_userid
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import finder
from .users import (User, UserManager)

from .models import (
    DBSession,
    Base,
    )

def db(request):
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()
    request.add_finished_callback(cleanup)
    return session

def get_user_manager(request):
    session = request.db_session
    return UserManager(db_session=session)

def get_user(request):
    userid = unauthenticated_userid(request)
    if userid is not None:
        return request.user_mgr.find_by_username(userid)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    auth_policy = AuthTktAuthenticationPolicy(
        secret='com.activelamp', callback=finder, hashalg='sha512'
    )
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings)

    # Auth
    config.set_authentication_policy(auth_policy)
    config.set_authorization_policy(authz_policy)

    # Registry
    config.registry.dbmaker = sessionmaker(bind=engine)

    # Request methods
    config.add_request_method(db, name='db_session', reify=True)
    config.add_request_method(get_user, name='user', reify=True)
    config.add_request_method(get_user_manager, name='user_mgr', reify=True)

    config.include('pyramid_chameleon')

    # Routes
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()

    return config.make_wsgi_app()
