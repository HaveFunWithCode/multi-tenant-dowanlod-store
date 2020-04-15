from django.db.models import Q, F
from django.utils import timezone

from content.models import File
from users.models import StoreUser
from membership.models import MemberShipOrder
from order.models import OrderItem, Order


def has_file_permission_access(user: StoreUser, fileobj: File):
    # free file
    if fileobj.price == 0:
        return True
    else:
        if user.is_authenticated:

            # has active membership for current store
            current_store = fileobj.product.store
            current_store_active_plan_for_user = MemberShipOrder.objects.filter(customer__user=user). \
                filter(plan__store=current_store). \
                filter(is_active=True). \
                filter(start_date__gt=timezone.datetime.now() - timezone.timedelta(days=1) * F("plan__type"))

            if current_store_active_plan_for_user:
                return True
            else:
                # user has order with such file
                file_bought = OrderItem.objects.filter(Q(file=fileobj) &
                                                       Q(order__customer__user=user) &
                                                       Q(order__order_status=Order.SUCCESSFUL))
                if file_bought:
                    return True
                else:
                    # user has order with product which contain this file
                    product = OrderItem.objects.filter(Q(product=fileobj.product) &
                                                       Q(order__customer__user=user) &
                                                       Q(order__order_status=Order.SUCCESSFUL))
                    if product:
                        return True
                    else:
                        return False
        else:
            # user is not authenticated and file is not free
            return False
