from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

user_job = db.Table(
        'user_job',
        db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete='CASCADE')),
        db.Column('job_id',db.Integer,db.ForeignKey('job.id',ondelete='CASCADE'))
        )

class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),nullable=False,unique=True,index=True)
    email = db.Column(db.String(64),nullable=False,unique=True,index=True)
    _password = db.Column('password',db.String(256),nullable=False)
    phone = db.Column(db.Integer)
    real_name = db.Column(db.String(16))
    work_years = db.Column(db.Integer)
    role = db.Column(db.SmallInteger,default=ROLE_USER)
    resume_url = db.Column(db.String(64))
    #generate_resume
    resume = db.relationship('Resume',uselist=False)
    collect_jobs = db.relationship('Job',secondary=user_job)
#    company_id = db.Column(db.Integer,db.ForeignKey('company.id',ondelete='SET NULL'))
#    company = db.relationship('Company',uselist=False)
#company_user
    is_disable = db.Column(db.Boolean,default=False)
    detail = db.relationship('CompanyDetail',uselist=False)

    def __repr__():
        return '<user:{}>'.format(self.name)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self,password):
        return check_password_hash(self._password,password)

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == ROLE_COMPANY
    @property
    def is_staff(self):
        return self.role == ROLE_USER


class CompanyDetail(Base):
    __tablename__ = 'company_detail'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False,unique=True,index=True)
    site = db.Column(db.String(64))
    about = db.Column(db.String(1024))
    description = db.Column(db.Text)
    logo = db.Column(db.String(64))
    tags = db.Column(db.String(128))
    team_introduction = db.Column(db.String(256))
    welfares = db.Column(db.String(256))
    field = db.Column(db.String(128))
    stack = db.Column(db.String(64))
    finance_stage  = db.Column(db.String(128))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',obdelet="SET NULL"))
    user = db.relationship('User',uselist=False,backref=db.backref('company_detail',uselist=False))

    location = db.Column(db.String(64))
    def __repr__(self):
        return '<CompanyDetail {}>'.format(self.id)


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),nullable=False)
    salary = db.Column(db.String(32))
    experience = db.Column(db.String(8),default='0')
    location = db.Column(db.String(16))
    is_fulltime = db.Column(db.Boolean,default=True)
    is_open = db.Column(db.Boolean,default=True)
    description = db.Column(db.Text)
    requirement = db.Column(db.Text)

    company_id = db.Column(db.Integer,db.ForeignKey('company.id',ondelete='SET NULL'))
    company = db.relationship('Company',uselist=False)
    
    @property
    def current_user_is_applied(self):
        d = Deliver.query.filter_by(job_id=self.id,user_id=current_user.id).first()
        return (d is not None)

class Delivery(Base):
    __tablename__ = 'delivery'
    
    STATUS_WAITING = 10
    STATUS_REJECT = 20
    STATUS_ACCEPT = 30

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='SET NULL'))
    job_id = db.Column(db.Integer,db.ForeignKey('job.id',ondelete='SET NULL'))
    status = db.Column(db.SmallInteger,default=STATUS_WAITING)
    
    response = db.Column(db.Text)



