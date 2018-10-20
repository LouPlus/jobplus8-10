from flask import Blueprint,request,current)app,redirect,url_for,flash
from jobplus.decorators import admin_required
from jobplus.models import User,db
from jobplus.forms import RegisterForm,UserEditForm,CompanyEditForm

admin = Blueprint('admin',__name__,url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page',default=1,type=int)
    pagination = User.query.paginate(
            page=page,
            per_page=current_app.config['ADMIN_PER_PAGE'],
            error_out=False
            )
    return render_template('admin/users.html',pagination=pagination)

@admin.route('/users/create_user',methods=['GET','POST'])
@admin_required
def create_user():
    form = RegisterForm()
    if form.is_submitted():
        form.create_user()
        flash('求职者创建成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html',form=form)

@admin.route('users/create_company',methods=['GET','POST'])
@admin_required
def create_company():
    form = RegisterForm()
    form.name.label = 'Name of Company'
    if form.validate_on_submit():
        form.create_user()
        flash('company created','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_company.html',form=form)

@admin.route('/users/<int:user_id>/edit',methods=['GET','POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_company:
        form = CompanyEditForm(obj=user)
    else:
        form = UserEditForm(obj=user)
    if form.validate_on_submit():
        form.update(user)
        flash('Updated','success')
        return redirect(url_for('amin.users'))
    if user.is_company:
        form.site.data = user.detail.site
        form.description.data=user.detail.description
    return render_template('admin/edit_user.html',form=form,user=user)

@admin.route('/users/<int:user_id>/disable',methods=['GET','POST'])
@admin_required
def disable_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_disable:
        user.is_disable = False
        flash('Enabled','success')
    else:
        user.is_disable = True
        flash('Banned','success')
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users'))
