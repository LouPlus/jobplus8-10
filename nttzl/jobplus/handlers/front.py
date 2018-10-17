from flask import Blueprint,render_template,url_for,redirect,flash
from models import RegisterForm,LoginForm

front = Blueprint('front',__name__)

@front.route('/')
def index():
    return render_template('index.html')

@front.route('/login')
def login():
    return render_template('login.html')

@front.route('/company-register')
def company_register():
    return render_template('register.html')

@front.route('/userregister',methods=['GET','POST'])
def userregister():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('register success','success')
        return redirect(url_for('.login'))
    return render_template('userregister.html',form=form)
