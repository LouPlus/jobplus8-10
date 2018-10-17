from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, TextField
from jobplus.models import db, User
from wtforms.validators import Required,Length,Email,EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(),Length(6,24)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

    def validate_emaill(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册')
    
    def validate_password(self, field):
        user = User.query.filter_by(email=self.emial.data).first()
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
        if User.query.filter_by(email=fild.data).first:
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
        user.real_name = self.real_name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_years = self.work_years.data
        user.resume_url = self.resume_url.data
        db.session.add(user)
        db.session.commit()


