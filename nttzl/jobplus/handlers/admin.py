from flask import Blueprint
from jobplus.decorators import admin_required
from jobplus.models import
admin = Blueprint('admin',__name__,url_prefix='/admin')


@admin.route('/jobs')
def
