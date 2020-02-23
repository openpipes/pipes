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
# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'jdbc:postgresql://postgres:@localhost:5432/policyreader'
# app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
db = SQLAlchemy(app)
ckeditor = CKEditor(app)  # 初始化扩展
# db.init_app(app)


# Define models
roles_people = db.Table(
    'roles_people',
    db.Column('people_id', db.Integer(), db.ForeignKey('people.id')),
    db.Column('roles_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text(), unique=True)
    description = db.Column(db.Text())

    def __str__(self):
        return self.name


class People(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text())
    last_name = db.Column(db.Text())
    email = db.Column(db.Text(), unique=True)
    password = db.Column(db.Text())
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DATETIME())
    roles = db.relationship('Role', secondary=roles_people,
                            backref=db.backref('people', lazy='dynamic'))

    def __str__(self):
        return self.email

class pooling(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    hash_code = db.Column(db.Text())
    title = db.Column(db.Text())
    unit = db.Column(db.Text())
    publish_time = db.Column(db.Text())
    provinces = db.Column(db.Text())
    cities = db.Column(db.Text())
    doc_type = db.Column(db.Text())
    url = db.Column(db.Text())
    score= db.Column(db.Integer())
    resume = db.Column(db.Text())
    keywords = db.Column(db.Text())
    content = db.Column(db.Text())
    is_checked = db.Column(db.Boolean())

    def __str__(self):
        return self.title

class articlemetadata(db.Model):
    hash_code = db.Column(db.Text(), primary_key=True)
    title = db.Column(db.Text())
    unit = db.Column(db.Text())
    publish_time = db.Column(db.Text())
    provinces = db.Column(db.Text())
    cities = db.Column(db.Text())
    doc_type = db.Column(db.Text())
    url = db.Column(db.Text())
    score= db.Column(db.Text())
    resume = db.Column(db.Text())
    keywords = db.Column(db.Text())

    def __str__(self):
        return self.title

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, People, Role)
security = Security(app, user_datastore)


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('supermanager') or current_user.has_role('manager'):
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
    
class PeopleView(MyModelView):
    column_editable_list = ['email', 'first_name', 'last_name','password','active']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
#     column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class ArticlePoolingView(ModelView):
#     form_overrides = dict(content=CKEditorField)  # 重写表单字段，将 content 字段设为 CKEditorField
    create_template = 'create.html'  
    __tablename__ = "pooling"
    can_export = False
    edit_template = 'edit.html'  # 指定编辑记录的模板
    column_editable_list = ['hash_code','title','unit','publish_time', 'provinces','cities','url','score','resume','keywords','is_checked','content']    
    column_searchable_list = column_editable_list
    column_exclude_list = ['hash_code','resume','url','provinces','cities','url','keywords']
#     form_excluded_columns = column_exclude_list
#     column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class ArticleView(ModelView):
    list_template = 'policyModel_list.html'
    column_exclude_list = ['hash_code','resume','url','provinces','cities','url','keywords','score']
    can_create = False
    can_edit = False



class CrawlerView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')

class KGraphView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')



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
admin.add_view(MyModelView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="权限",category="Team"))
admin.add_view(PeopleView(People, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="用户",category="Team"))
path = os.path.join(os.path.dirname(__file__), 'uploads')
admin.add_view(UploadFileView(path, endpoint = "/uploads/",base_url = '/uploads/', name='上传文件',menu_icon_type='fa', menu_icon_value='fa-upload'))
admin.add_view(ArticlePoolingView(pooling, db.session, menu_icon_type='fa', menu_icon_value='fa-wrench',name = '修改文稿'))
admin.add_view(ArticleView(articlemetadata, db.session,name='已有文稿', menu_icon_type='fa', menu_icon_value='fa-file'))
admin.add_view(KGraphView(menu_icon_type='fa', menu_icon_value='fa-houzz',name = "知识图谱"))
admin.add_view(CrawlerView(name="数据采集", menu_icon_type='fa', menu_icon_value='fa-bug'))

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



if __name__ == '__main__':

    # Start app
    app.run(host = '0.0.0.0',port=5568,debug=True)