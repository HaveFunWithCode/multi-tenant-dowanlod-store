from rest_framework import permissions
from stores.utils import store_from_request


class IsOwnerOfStore(permissions.BasePermission):
    """custom permission to only allow owners of an store to add product add file to the site"""

    message = "Your are not the owner of this store .Permission denied"

    def has_permission(self, request, view):
        store = store_from_request(request)

        return request.user and request.user.is_authenticated and (request.user == store.owner.user)
