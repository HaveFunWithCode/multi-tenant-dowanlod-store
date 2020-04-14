from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# from .tasks import send_verification_email
from datetime import datetime, timedelta
from .models import CustomerUser, StoreAdminUser
from django.contrib.auth.models import Permission


@receiver(post_save, sender=CustomerUser)
def update_user_profile(sender, instance, created, **kwargs):
    """create token for user after creating user (register or create by site admin"""
    if created:
        if not instance.is_superuser:
            Token.objects.create(user=instance)


@receiver(post_save, sender=StoreAdminUser)
def update_user_profile(sender, instance, created, **kwargs):
    """ set product and file management permissions for store admins"""
    if created:
        instance.user.is_staff = True
        instance.user.is_superuser = False
        product_permissions = Permission.objects.filter(content_type__app_label='content',
                                                        content_type__model='product')
        file_permissions = Permission.objects.filter(content_type__app_label='content',
                                                     content_type__model='file')
        for p_perm in product_permissions:
            instance.user.user_permissions.add(p_perm)
        for f_perm in file_permissions:
            instance.user.user_permissions.add(f_perm)

        instance.user.save()


