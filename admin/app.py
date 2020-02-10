#!venv/bin/python
import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_admin import BaseView, expose
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction
from flask_ckeditor import CKEditor, CKEditorField  # 导入扩展类 CKEditor 和 字段类 CKEditorField
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditorField

# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
ckeditor = CKEditor(app)  # 初始化扩展



# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

class Pooling(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    is_checked = db.Column(db.Boolean())
    hash_code = db.Column(db.Text())
    title = db.Column(db.Text())
    unit = db.Column(db.Text())
    publish_time = db.Column(db.Date())
    content = db.Column(db.Text())
    provinces = db.Column(db.Text())
    cities = db.Column(db.Text())
    """
    下拉表单
    """
    doc_type = db.Column(db.Text())
    url = db.Column(db.Text())
    score= db.Column(db.Text())
    resume = db.Column(db.Text())
    keywords = db.Column(db.Text())
    

    def __str__(self):
        return self.title

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


    # can_edit = True
    edit_modal = True
    create_modal = True    
    can_export = True
    can_view_details = True
    details_modal = True

class UserView(MyModelView):
    column_editable_list = ['email', 'first_name', 'last_name']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class PoolingView(ModelView):
    form_overrides = dict(text=CKEditorField)  # 重写表单字段，将 text 字段设为 CKEditorField
    create_template = 'edit.html'  # 指定创建记录的模板
    edit_template = 'edit.html'  # 指定编辑记录的模板

    column_editable_list = ['id','title','unit','publish_time', 'provinces','cities','url','score','resume','keywords','content','is_checked']
    column_searchable_list = column_editable_list
    column_exclude_list = ['hash_code','resume','url','provinces','cities','url','keywords','score']
    # 'content',
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

    # column_extra_row_actions = [
    #     EndpointLinkRowAction(
    #         'off glyphicon glyphicon-off',
    #         'pooling.modify_view',
    #     )
    # ]
    # @expose('/modify/', methods=('GET',))
    # def modify_view(self):
    #     return """ success """

class UploadFileView(FileAdmin):
    # @expose('/')
    allowed_extensions = ('html','pdf','doc','docx','txt','excel')
    editable_extensions = ('md', 'html', 'txt','png')
    can_upload = True
    can_delete = True
    can_delete_dirs = True
    can_mkdir = True
    can_rename = True
    can_delete_dirs = False

class CrawlerView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')

class KGraphView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')

class ModelView(BaseView):
    @expose('/')
    def index(self):
        return self.render('toggle_page.html')


# Flask views
@app.route('/')
def index():
    return render_template('index.html')

# Create admin
admin = flask_admin.Admin(
    app,
    'My Dashboard',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add model views
admin.add_view(MyModelView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="权限"))
admin.add_view(UserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="用户"))
path = os.path.join(os.path.dirname(__file__), 'uploads')
admin.add_view(UploadFileView(path, endpoint = "/uploads/",base_url = '/uploads/', name='上传文件',menu_icon_type='fa', menu_icon_value='fa-upload'))
admin.add_view(PoolingView(Pooling, db.session, menu_icon_type='fa', menu_icon_value='fa-wrench',name = '修改文稿'))
admin.add_view(KGraphView(menu_icon_type='fa', menu_icon_value='fa-houzz',name = "知识图谱"))
admin.add_view(CrawlerView(name="数据采集", menu_icon_type='fa', menu_icon_value='fa-houzz'))
admin.add_view(ModelView(name="模型控制", menu_icon_type='fa', menu_icon_value='fa-houzz'))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            first_name='Admin',
            email='admin',
            password=encrypt_password('admin'),
            roles=[user_role, super_user_role]
        )

        first_names = [
            'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie', 'Sophie', 'Mia',
            'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
            'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
        ]
        last_names = [
            'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
            'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
            'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
        ]

        for i in range(len(first_names)):
            tmp_email = first_names[i].lower() + "." + last_names[i].lower() + "@example.com"
            tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
            user_datastore.create_user(
                first_name=first_names[i],
                last_name=last_names[i],
                email=tmp_email,
                password=encrypt_password(tmp_pass),
                roles=[user_role, ]
            )
        db.session.commit()
    return

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)