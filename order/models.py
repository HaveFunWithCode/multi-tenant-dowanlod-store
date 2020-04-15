from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from content.models import Product, File
from users.models import CustomerUser


class Order(models.Model):
    """ This model used for saving customer order status and a reference for download access"""

    PENDING = 'pending'
    CANCELED = 'canceled'
    UNSUCCESSFUL = 'unsuccessful'
    SUCCESSFUL = 'successful'

    ORDER_STATUS = [
        (PENDING, _('Waiting for paying')),
        (CANCELED, _('Canceled order')),
        (UNSUCCESSFUL, _('Unsuccessful payment')),
        (SUCCESSFUL, _('Successful payment')),
    ]

    customer = models.ForeignKey(CustomerUser, null=False, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    order_status = models.CharField(max_length=12, choices=ORDER_STATUS, default=PENDING)
    total_price = models.PositiveIntegerField(null=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return 'order {}'.format(self.id)


class OrderItem(models.Model):
    """ This model save customer order detail + order item type """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    file = models.ForeignKey(File, null=True, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(null=False)
    item_type = models.CharField(max_length=7)

    def save(self, *args, **kwargs):
        if self.product is not None:
            self.item_type = "Product"
        else:
            self.item_type = "File"
        super(OrderItem,self).save(*args, **kwargs)

    def __str__(self):
        return '{}\n{}'.format(self.product.name if self.product is None else self.file.name)

    def clean(self):
        if not self.product and not self.file:
            raise ValidationError({'message': _('Even one of file or product should have a value.')})
