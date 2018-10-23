from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from jobplus.forms import CompanyProfileForm
from jobplus.models import User

company = Blueprint('company',__name__,url_prefix='/company')

@company.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.filter(User.role==User.ROLE_COMPANY).order_by(User.created_at.desc()).paginate(
            page=page,
            per_page=12,
            error_out=False
            )
    return render_template('company/index.html', pagination=pagination, active='company')

@company.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    if not current_user.is_company:
        flash('You are not Company User', 'warning')
        return redirect(url_for('front.index'))
    form = CompanyProfileForm(obj=current_user.company_detail)
    form.name.data = current_user.name
    form.email.data = current_user.email
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('Company Info Updated', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form=form)

@company.route('/<int:company_id>')
def company_detail(company_id):
    company = User.query.get_or_404(company_id)
    if not company.is company:
        abort(404)
    else:
        return render_template('company/detail.html',company=company,active='',panel='about')

@company.route('/<int:company_id>/job')
def company_jobs(company_id):
    company = User.query.get_or_404(company_id)
    if not company.is company:
        abort(404)
    else:
        return render_template('company/detail.html',company=company,active='',panel='job')


