from flask import Blueprint,request,current_app,render_template,flash,redirect,url_for
from jobplus.models import Job,Delivery,db
from flask_login import login_required,current_user

job = Blueprint('job',__name__, url_prefix='/job')

@job.route('/')
def index():
    page = request.args.get('page',1,type=int)
    pagination = Job.query.order_by(Job.created_at.desc()).paginate(
        page = page,
        per_page = current_app.config['INDEX_PER_PAGE'],
        error_out = False
    )
    return render_template('job/index.html',pagination=pagination,active='job')

@job.route('/<int:job_id>')
def job_detail(job_id):
#    job = Job.query.filter_by(id = job_id)
    job = Job.query.get_or_404(job_id)
    return render_template('job/detail.html',job=job,active='')

@job.route('/<int:job_id>/apply')
@login_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    if job.current_user_is_applied:
        flash('you have delivered','warning')
    else:
        d = Delivery(
                job_id = job.id,
                user_id = current_user.id
                )
        db.session.add(d)
        db.session.commit()
        flash('successfully delivered','success')
    return redirect(url_for('job.job_detail',job_id=job.id))

@job.route('<int:job_id>/disable')
@login_required
def disable(job_id):
    job = Job.query.get_or_404(job_id)
    if not current_user.is_admin and current_user.id != job.company.id:
        abort(404)
    if job.is_disable:
        flash('Job Offline', 'warning')
    else:
        job.is_disable = True
        db.session.add(job)
        db.session.commit()
        flash('Job Offline Success', 'success')
    if current_user.is_admin:
        return redirect(url_for('admin.jobs'))
    else:
        return redirect(url_for('company.admin_index', company_id=job.company.id))

@job.route('<int:job_id>/enable')
@login_required
def enable(job_id):
    job = Job.query.get_or_404(job_id)
    if not current_user.is_admin and current_user.id != job.company.id:
        abort(404)
    if not job.is_disable:
        flash('Job Online', 'warning')
    else:
        job.is_disable = False
        db.session.add(job)
        db.session.commit()
        flash('Job Online Success', 'success')
    if current_user.is_admin:
        return redirect(url_for('admin.jobs'))
    else:
        return redirect(url_for('company.admin_index', company_id=job.company.id))


