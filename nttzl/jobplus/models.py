from flask-sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.Datetime,default=datetime.utcnow)
    updated_at = db.Column(db.Datetime,default=datetime.utcnow,onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),nullable=False,unique=True,index=True)
    email = db.Column(db.String(64),nullable=False,unique=True,index=True)
    _password = db.Column('password',db.String(256),nullable=False)
    role = db.Column(db.SmallInteger,default=ROLE_USER)
    company_id = db.Column(db.Integer,db.ForeignKey('company.id',ondelete='SET NULL'))
    company = db.relationship('Company')

class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False,unique=True,index=True)
    website = db.Column(db.String(64))
    describe = db.Column(db.Text)
    logo_url = db.Column(db.String(64))
    field = db.Column(db.String(64))
    finance = db.Column(db.String(8))
    city = db.Column(db.String(16))
    position = db.relation('Position')


class Position(Base):
    __tablename__ = 'position'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),nullable=False)
    range = db.Column(db.String(32))
    experience = db.Column(db.String(8),default='0')
    place = db.Column(db.String(16))
    company = db.relationship('Company',userlist=True)
    describe = db.Column(db.text)
    requirement = db.Column(db.text)


