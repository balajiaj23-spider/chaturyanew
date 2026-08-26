from django.apps import AppConfig
from django.db.models.signals import post_migrate

def sync_admin_credentials(sender, **kwargs):
    from django.contrib.auth.models import User
    try:
        # Automatically clean up old default admin users on deployment
        User.objects.filter(username__in=['admin', 'Admin', 'admin_test']).delete()

        # Guarantee chathuryasdc user is created with updated credentials
        user, created = User.objects.get_or_create(username='chathuryasdc')
        user.set_password('balajinaveen@26')
        user.is_staff = True
        user.is_superuser = True
        user.email = 'chathuryastudentdeveloperclub@gmail.com'
        user.save()
    except Exception:
        pass


class WorkshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workshop'

    def ready(self):
        post_migrate.connect(sync_admin_credentials, sender=self)
