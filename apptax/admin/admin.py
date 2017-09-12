
from flask_admin import Admin, AdminIndexView
from flask import current_app, Blueprint

from pypnusershub.routes import check_auth

from flask_admin.contrib.sqla import ModelView
from apptax.taxonomie.models import BibThemes, BibTypesMedia, BibAttributs, Taxref
from apptax.log.models import TaxhubAdminLog

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_admin.contrib.sqla.form import AdminModelConverter
from flask_admin.model.form import converts

from flask_admin.menu import MenuLink

class SQLAUtilsModelConverter(AdminModelConverter):
    """ Allow fields from SQLA-utils to be used in the admin """

    @converts('sqlalchemy_utils.types.choice.ChoiceType')
    def conv_ChoiceType(self, column, field_args, **extra):
        choices = column.type.choices

        def coerce(val):
            if isinstance(val, str):
                return val
            return val.code

        return form.Select2Field(
            choices=[(k, v) for k, v in choices],
            coerce=coerce,
            **field_args
        )

class AuthenticatedModelView(ModelView):
    """ Common features for all our admin configurations classes """
    model_form_converter = SQLAUtilsModelConverter
    column_exclude_list = form_excluded_columns = ('created', 'updated')
    can_delete = False
    can_export = True

    @check_auth(
        3,
        redirect_on_expiration="/",
        redirect_on_invalid_token="/"
    )
    def _handle_view(self, name, **kwargs):
        return super()._handle_view(name, **kwargs)

class NoActionsModelView(AuthenticatedModelView):
    can_create = False
    can_edit = False
    can_delete = False

from flask_admin.base import expose
class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/admin.html')

    def get_url(self, *args, **kwargs):
        print('get_url')
        url = super(CustomAdminIndexView, self).get_url(self, *args,**kwargs)
        return '/taxhub' + url

    def get_url(self, *args, **kwargs):
            # url = super(MyHomeView, self).get_url(self,**kwargs)
            return '/taxhub/admin'

def setup_admin(app):
    # Automatic admin
    admin = Admin(
        app,
        name='Admin de Taxhub',
        template_mode='bootstrap3',
        index_view=MyHomeView()
    )
    # admin.add_view(ModelView(BibThemes, db.session))
    admin.add_link(
        MenuLink(name='Retour à taxhub', url='/')
    )
    admin.add_view(AuthenticatedModelView(BibThemes, db.session, name='Themes',category='Attributs'))
    admin.add_view(AuthenticatedModelView (BibAttributs, db.session, name='Attributs',category='Attributs'))
    admin.add_view(AuthenticatedModelView(BibTypesMedia, db.session, name='Type de média'))
    admin.add_view(NoActionsModelView(TaxhubAdminLog, db.session, name='Logs'))
