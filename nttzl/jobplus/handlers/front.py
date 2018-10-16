from flask import Blueprint,render_template

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

#@front.route('/user-register')
