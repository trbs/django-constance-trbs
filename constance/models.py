import django
from django.db.models import signals


def create_perm(app, created_models, verbosity, db, **kwargs):
    """
    Creates a fake content type and permission
    to be able to check for permissions
    """
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    if ContentType._meta.installed and Permission._meta.installed:
        kwargs = dict(
            app_label='constance',
            model='config'
        )
        if django.VERSION < (1, 8):
            kwargs['name'] = 'config'

        content_type, created = ContentType.objects.get_or_create(**kwargs)

        permission, created = Permission.objects.get_or_create(
            name='Can change config',
            content_type=content_type,
            codename='change_config')


if django.VERSION < (1, 7):
    signals.post_syncdb.connect(create_perm, dispatch_uid="constance.create_perm")
else:
    signals.post_migrate.connect(create_perm, dispatch_uid="constance.create_perm")
