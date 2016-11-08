from flask_peewee.admin import ModelAdmin
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin
from models.models import SiteUser
from models.utils import get_user_exclude_fields


# create a modeladmin for it
class UserAdmin(ModelAdmin):
    columns = ('username', 'email', 'is_superuser',)

    # Make sure the user's password is hashed, after it's been changed in
    # the admin interface. If we don't do this, the password will be saved
    # in clear text inside the database and login will be impossible.
    def save_model(self, instance, form, adding=False):
        orig_password = instance.password

        user = super(UserAdmin, self).save_model(instance, form, adding)

        if orig_password != form.password.data:
            user.set_password(form.password.data)
            user.save()

        return user


# subclass Auth so we can return our custom classes
class CustomAuth(Auth):
    def get_user_model(self):
        return SiteUser

    def get_model_admin(self):
        return UserAdmin


class CustomAdmin(Admin):
    def check_user_permission(self, user):
        return user.is_superuser


class UserShowAdmin(ModelAdmin):
    columns = ('username', 'first_name', 'is_active', 'phone', 'surname',)
    exclude = get_user_exclude_fields()
    filter_exclude = get_user_exclude_fields()


class StpShowAdmin(ModelAdmin):
    filter_exclude = get_user_exclude_fields('user__')


class RequestShowAdmin(ModelAdmin):
    filter_exclude = get_user_exclude_fields('user__') + get_user_exclude_fields('stp__user__')


class MessageShowAdmin(ModelAdmin):
    columns = ('is_read', 'text', 'request', 'to_user', 'from_user')
    filter_exclude = get_user_exclude_fields('to_user__') + get_user_exclude_fields(
        'from_user__') + get_user_exclude_fields('request__user__') + get_user_exclude_fields(
        'request__stp__user__') + get_user_exclude_fields('msg_from_user__') + get_user_exclude_fields('msg_to_user__')


class StpSectionShowAdmin(ModelAdmin):
    filter_exclude = get_user_exclude_fields('stp__user__')
