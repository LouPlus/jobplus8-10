import os
from flask import url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SelectField, TextAreaField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, TextField
from jobplus.models import db, User, Company, Job
from wtforms.validators import Required,Length,Email,EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(),Length(6,24)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册')
    
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')

class RegisterForm(FlaskForm):
    name = StringField('User Name',validators=[Required(), Length(3,24)])
    email = StringField('Email Address', validators=[Required(),Email()])
    password = PasswordField('Password', validators=[Required(),Length(6,24)])
    repeat_password = PasswordField('Repeat Password', validators=[Required(),EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username Exists')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email Exists')

    def create_user(self):
        user = User(name=self.name.data,
                    email=self.email.data,
                    password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user

class UserProfileForm(FlaskForm):
    real_name = StringField('Name')
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password')
    phone = StringField('PhoneNumber')
    work_years = IntegerField('WorkYears')
    resume_url = StringField('ResumeAddress')
    submit = SubmitField('Submit')

    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('Please Input Valid Number')

    def updated_profile(self, user):
        user.name = self.real_name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_years = self.work_years.data
        user.resume_url = self.resume_url.data
        db.session.add(user)
        db.session.commit()

class CompanyProfileForm(FlaskForm):
    name = StringField('Company Name')
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password')
    slug = StringField('Slug', validators=[Required(), Length(3, 24)])
    location = StringField('Address', validators=[Length(0, 64)])
    site = StringField('Website', validators=[Length(0, 64)])
    logo = StringField('Logo')
    description = StringField('Description', validators=[Length(0, 100)])
    about = TextAreaField('Company Detail', validators=[Length(0, 1024)])
    submit = SubmitField('Submit')


    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('Please Input Valid Number')

    def updated_profile(self, user):
        user.name = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data

        if user.detail:
            detail  = user.detail
        else:
            detail = Company()
            detail.user_id = user.id
        self.populate_obj(detail)
        db.session.add(user)
        db.session.add(detail)
        db.session.commit()
class UserEditForm(FlaskForm):
    email = StringField("email",validators=[Required(),Email()])
    password = PasswordField("password")
    real_name = StringField("name")
    phone = StringField("phone")
    submit = SubmitField("submit")
    def update(self,user):
        self.populate_obj(user)
        if self.password.data:
            user.password = self.password.data
        db.session.add(user)
        db.session.commit()
class CompanyEditForm(FlaskForm):
    name = StringField("CompanyName")
    email = StringField("email",validators=[Required(),Email()])
    password = PasswordField("password")
    phone = StringField("phone")
    site = StringField("CompanySite",validators=[Length(0,64)])
    desctiption = StringField("description",validators=[Length(0,100)])
    submit = SubmitField("submit")
    def update(self,company):
        company.name = self.name.data
        company.email = self.email.data
        if self.password.data:
            company.password = self.password.data
        if company.detail:
            detail = company.detail
        else:
            detail = CompanyDetial()
            detail.user_id = company.id
        detail.site = self.site.data
        detail.description = self.description.data
        db.session.add(company)
        db.session.add(detail)
        db.session.commit()

class JobForm(FlaskForm):
    name = StringField('Job Name')
    salary_low = IntegerField('Lowest Salary')
    salary_high = IntegerField('Highest Salary')
    location = StringField('Work Location')
    tags = StringField('Job Tags(Seperate with ,)')
    experience_requirement = SelectField(
            'Experience Requirement(Year)',
            choices=[
                ('NoLimit', 'NoLimit'),
                ('1', '1'),
                ('2', '2'),
                ('3', '3'),
                ('1-3','1-3'),
                ('3-5','3-5'),
                ('5+','5+')
                ]
            )
    degree_requirement = SelectField(
            'Degree Requirement',
            choices=[
                ('NoLimit', 'NoLimit'),
                ('Master', 'Master'),
                ('PhD', 'PhD')
                ]
            )
    description = TextAreaField('Job Description', validators=[Length(0, 1500)])
    submit = SubmitField('Submit')

    def create_job(self, company):
        job = Job()
        self.populate_obj(job)
        job.company_id = company.id
        db.session.add(job)
        db.session.commit()
        return job

    def update_job(self, job):
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
        return job

