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
from flask_admin.actions import action
from flask_admin.base import AdminIndexView
from flask_admin.base import MenuLink


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
    confirmed_at = db.Column(db.DATETIME())
    active = db.Column(db.Boolean())
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

user_datastore = SQLAlchemyUserDatastore(db, People, Role)
security = Security(app, user_datastore)

class MyModelView(sqla.ModelView):
#     role management
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('supermanager'):
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


    edit_modal = True
    create_modal = True    
    can_export = True
    can_view_details = True
    details_modal = True
    
class UploadFileView(FileAdmin):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('supermanager') or current_user.has_role('manager'):
            return True

        return False
    
    allowed_extensions = ('html','pdf','doc','docx','txt','excel')
    editable_extensions = ('md', 'html', 'txt','png')
    can_upload = True
    can_delete = True
    can_delete_dirs = True
    can_mkdir = True
    can_rename = True
    can_delete_dirs = False
    
class PeopleView(MyModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('supermanager')or current_user.has_role('manager'):
            return True

        return False
    
    column_editable_list = ['email', 'first_name', 'last_name','password','active']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    column_filters = column_editable_list
    page_size = 10

class PoolingView1(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('supermanager') or current_user.has_role('manager'):
            return True

        return False
    
    column_editable_list = ['hash_code','title','unit','publish_time', 'provinces','cities',
                            'url','score','resume','keywords','is_checked','content','doc_type'] 
    column_exclude_list = ['hash_code','resume','url','provinces','cities','url','keywords','content']
    column_labels = {'hash_code':'哈希值','title':'标题','unit':'发布单位','publish_time':'发布时间','doc_type':'分类',
                     'provinces':'省份','cities':'城市','url':'链接','score':'分数','resume':'概要',
                     'keywords':'关键词','is_checked':'是否检查','content':'文章主体'}

    form_overrides = dict(content = CKEditorField)
    page_size = 10
    create_template = 'ck_create.html'
    edit_template = 'ck_edit.html'  # 指定编辑记录的模板
    column_type_formatters=dict()#is_checked 默认值 False
    column_default_sort = ('is_checked', False)# 优先显示is_Checked为true的数据

class PoolingView2(ModelView):
 
    can_export = False
    can_create = False
    column_editable_list = ['hash_code','title','unit','publish_time', 'provinces','cities','url','score','resume','keywords','is_checked','content']
#     column_searchable_list = column_editable_list
#     column_filters = column_editable_list
    column_exclude_list = ['hash_code','resume','url','provinces','cities','url','keywords']
    column_details_exclude_list = column_exclude_list    
    column_labels = {'hash_code':'哈希值','title':'标题','unit':'发布单位','publish_time':'发布时间','doc_type':'分类',
                     'provinces':'省份','cities':'城市','url':'链接','score':'分数','resume':'概要',
                     'keywords':'关键词','is_checked':'是否检查','content':'文章主体'}
#     form_overrides = {
#     'content': CKTextAreaField
#     }
    form_overrides = dict(content = CKEditorField)
    create_template = 'ck_create.html'
    edit_template = 'ck_edit.html'  # 指定编辑记录的模板
    page_size = 10
    column_default_sort = ('is_checked', True)# 优先显示is_Checked为true的数据

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('supermanager') or current_user.has_role('manager'):
            return True

        return False
    
    @action('approve', 'Approve', 'Are you sure you want to approve selected articles?')
    def action_approve(self, ids):
        try:
            query = pooling.query.filter(pooling.id.in_(ids))
            count = 0
            for article in query.all():
                if article.approve():
                    count += 1

            flash(ngettext('article was successfully approved.',
                           '%(count)s articles were successfully approved.',
                           count,
                           count=count))
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(gettext('Failed to approve articles. %(error)s', error=str(ex)), 'error')

            
class ArticleView(ModelView):
    
    list_template = 'policyModel_list.html'
    column_exclude_list = ['hash_code','resume','url','provinces','cities','url','keywords','score']
    can_create = False
    can_edit = False
    page_size = 10
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('supermanager') or current_user.has_role('manager'):
            return True

        return False
    
class CrawlerView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')

class KGraphView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')

class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        num_article = db.session.execute('select count(*) from articlemetadata').scalar()
        num_province = db.session.execute('select count(*) from articleclass').scalar()
        num_user = db.session.execute('select count(*) from people').scalar()
        num_visit = "??"
        return self.render('my_home.html', num_article=num_article,num_province = num_province,num_user = num_user,num_visit = num_visit)

class AuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('supermanager') or current_user.has_role('manager') or current_user.has_role('visitor'):
            return True

        return False   
    
# Flask views
@app.route('/')
def index():
    return render_template('index.html')

# Create admin
admin = flask_admin.Admin(
    app,
    index_view=MyHomeView(),
    base_template='my_master.html',
    template_mode='bootstrap3',

)

# Add model views
admin.add_view(MyModelView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="权限"))
admin.add_view(PeopleView(People, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="用户"))
path = os.path.join(os.path.dirname(__file__), 'uploads')
admin.add_view(UploadFileView(path, endpoint = "uploads/", name='上传文件',menu_icon_type='fa', menu_icon_value='fa-upload'))
admin.add_view(PoolingView1(pooling, db.session, menu_icon_type='fa', menu_icon_value='fa-wrench',name = '文稿一次校验',category = "文稿校验"
                            ,endpoint = "init_check"))
admin.add_view(PoolingView2(pooling, db.session, menu_icon_type='fa', menu_icon_value='fa-wrench',name = '文稿二次校验',category = "文稿校验"
                            ,endpoint = "double_check"))
admin.add_view(ArticleView(articlemetadata, db.session,name='已有文稿', menu_icon_type='fa', menu_icon_value='fa-file'))
admin.add_view(KGraphView(menu_icon_type='fa', menu_icon_value='fa-houzz',name = "知识图谱"))
admin.add_view(CrawlerView(name="数据采集", menu_icon_type='fa', menu_icon_value='fa-bug'))
admin.add_link(AuthenticatedMenuLink(name = "google", url="http://www.google.com",category = "外部链接"))

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