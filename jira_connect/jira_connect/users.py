from .models import (
    User
)

__all__ = ['UserManager', 'User']

class UserManager():

    def __init__(self, db_session):
        self.db_session = db_session

    def find_by_id(self, id):
        return self.db_session.query(User).filter(User.id==id).first()

    def find_by_username(self, username):
        return self.db_session.query(User).filter(User.username==username).first()

    def save(self, user):
        self.db_session.add(user)
