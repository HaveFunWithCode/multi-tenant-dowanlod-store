from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from users.models import CustomerUser
from content.models import Product, File


class Cart(models.Model):
    """Model for saving shopping cart"""
    customer = models.OneToOneField(CustomerUser, null=False, on_delete=models.CASCADE, related_name='cart')
    total_price = models.BigIntegerField(default=0)


class CartItem(models.Model):
    """Model for saving shopping cart items in which if file is null it means customer wanna buy the whole product"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cartitems')
    product = models.ForeignKey(Product, null=True, unique=True, on_delete=models.CASCADE)
    file = models.ForeignKey(File, null=True, unique=True, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    price = models.BigIntegerField()

    class Meta:
        unique_together = ['cart',
                           'product',
                           'file']

    def clean(self):
        if not self.product and not self.file:
            raise ValidationError({'message': _('Even one of file or product should have a value.')})
