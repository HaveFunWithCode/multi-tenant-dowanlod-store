from django import forms
from django.contrib.auth.backends import ModelBackend
from django.utils.translation import ugettext_lazy as _
from .models import StoreUser

from stores.utils import store_from_request
from stores.models import Store


class StoreBackend(ModelBackend):

    def authenticate(self, request, username, password):
        store_name = store_from_request(request)

        try:
            user = StoreUser.objects.get(email=username)
            if user.check_password(password) is True:
                # check authenticated user is owner of store or not
                try:
                    is_owner = Store.objects.get(owner__user=user, name=store_name)
                    return user
                except Store.DoesNotExist:
                    raise forms.ValidationError(
                        _("You are not the owner of {} store. You don't have access to this page").format(store_name))

        except StoreUser.DoesNotExist:
            pass
