"""Oct 28th

Revision ID: 82220c2c668a
Revises: 3f45d0b9a32d
Create Date: 2018-10-28 10:16:55.627931

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '82220c2c668a'
down_revision = '3f45d0b9a32d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resume',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('edu_experience',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('begin_at', sa.DateTime(), nullable=True),
    sa.Column('end_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('school', sa.String(length=32), nullable=False),
    sa.Column('specialty', sa.String(length=32), nullable=False),
    sa.Column('degree', sa.String(length=16), nullable=True),
    sa.Column('resume_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('job_experience',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('begin_at', sa.DateTime(), nullable=True),
    sa.Column('end_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('company', sa.String(length=32), nullable=False),
    sa.Column('city', sa.String(length=32), nullable=False),
    sa.Column('resume_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('preject_experience',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('begin_at', sa.DateTime(), nullable=True),
    sa.Column('end_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('role', sa.String(length=32), nullable=True),
    sa.Column('technologys', sa.String(length=64), nullable=True),
    sa.Column('resume_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['resume_id'], ['resume.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('company', sa.Column('about', sa.String(length=1024), nullable=True))
    op.add_column('company', sa.Column('field', sa.String(length=128), nullable=True))
    op.add_column('company', sa.Column('finance_stage', sa.String(length=128), nullable=True))
    op.add_column('company', sa.Column('logo', sa.String(length=256), nullable=False))
    op.add_column('company', sa.Column('team_introduction', sa.String(length=256), nullable=True))
    op.add_column('company', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('company', sa.Column('welfares', sa.String(length=256), nullable=True))
    op.alter_column('company', 'location',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.alter_column('company', 'site',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.drop_index('ix_company_name', table_name='company')
    op.create_foreign_key(None, 'company', 'user', ['user_id'], ['id'], ondelete='SET NULL')
    op.drop_column('company', 'finance')
    op.drop_column('company', 'name')
    op.drop_column('company', 'logo_url')
    op.add_column('job', sa.Column('degree_requirement', sa.String(length=32), nullable=True))
    op.add_column('job', sa.Column('experience_requirement', sa.String(length=32), nullable=True))
    op.add_column('job', sa.Column('salary_high', sa.Integer(), nullable=False))
    op.add_column('job', sa.Column('salary_low', sa.Integer(), nullable=False))
    op.add_column('job', sa.Column('tags', sa.String(length=128), nullable=True))
    op.add_column('job', sa.Column('views_count', sa.Integer(), nullable=True))
    op.alter_column('job', 'name',
               existing_type=mysql.VARCHAR(length=16),
               nullable=True)
    op.drop_constraint('job_ibfk_1', 'job', type_='foreignkey')
    op.create_foreign_key(None, 'job', 'user', ['company_id'], ['id'], ondelete='CASCADE')
    op.drop_column('job', 'requirement')
    op.drop_column('job', 'description')
    op.drop_column('job', 'salary')
    op.drop_column('job', 'experience')
    op.add_column('user', sa.Column('is_disable', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('real_name', sa.String(length=20), nullable=True))
    op.drop_constraint('user_ibfk_1', 'user', type_='foreignkey')
    op.drop_column('user', 'company_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('company_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('user_ibfk_1', 'user', 'company', ['company_id'], ['id'], ondelete='SET NULL')
    op.drop_column('user', 'real_name')
    op.drop_column('user', 'is_disable')
    op.add_column('job', sa.Column('experience', mysql.VARCHAR(length=8), nullable=True))
    op.add_column('job', sa.Column('salary', mysql.VARCHAR(length=32), nullable=True))
    op.add_column('job', sa.Column('description', mysql.TEXT(), nullable=True))
    op.add_column('job', sa.Column('requirement', mysql.TEXT(), nullable=True))
    op.drop_constraint(None, 'job', type_='foreignkey')
    op.create_foreign_key('job_ibfk_1', 'job', 'company', ['company_id'], ['id'], ondelete='SET NULL')
    op.alter_column('job', 'name',
               existing_type=mysql.VARCHAR(length=16),
               nullable=False)
    op.drop_column('job', 'views_count')
    op.drop_column('job', 'tags')
    op.drop_column('job', 'salary_low')
    op.drop_column('job', 'salary_high')
    op.drop_column('job', 'experience_requirement')
    op.drop_column('job', 'degree_requirement')
    op.add_column('company', sa.Column('logo_url', mysql.VARCHAR(length=64), nullable=True))
    op.add_column('company', sa.Column('name', mysql.VARCHAR(length=64), nullable=False))
    op.add_column('company', sa.Column('finance', mysql.VARCHAR(length=8), nullable=True))
    op.drop_constraint(None, 'company', type_='foreignkey')
    op.create_index('ix_company_name', 'company', ['name'], unique=True)
    op.alter_column('company', 'site',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.alter_column('company', 'location',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.drop_column('company', 'welfares')
    op.drop_column('company', 'user_id')
    op.drop_column('company', 'team_introduction')
    op.drop_column('company', 'logo')
    op.drop_column('company', 'finance_stage')
    op.drop_column('company', 'field')
    op.drop_column('company', 'about')
    op.drop_table('preject_experience')
    op.drop_table('job_experience')
    op.drop_table('edu_experience')
    op.drop_table('resume')
    # ### end Alembic commands ###
