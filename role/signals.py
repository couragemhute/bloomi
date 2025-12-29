
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from role.models import Role
from accounts.models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_admin_role(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        # Create or get the admin role
        admin_role = Role.objects.filter(is_admin=True).first()
        if not admin_role:
            admin_role = Role.objects.create(name='Super Admin', code='system_admin', is_admin=True)

        all_permissions = Permission.objects.all()
        admin_role.permissions.set(all_permissions)    

        # Assign admin role to superuser
        instance.role = admin_role
        instance.save()
        



