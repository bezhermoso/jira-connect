from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    fullname = Column(String)

class TrelloAccount(Base):
    __tablename__ = 'trello_account'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    secret = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    user = relationship('User', backref=backref('trello_accts', order_by=id))

class JiraAccount(Base):
    __tablename__ = 'jira_account'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    secret = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    user = relationship('User', backref=backref('jira_accts', order_by=id))


