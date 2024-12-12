from django.db import models
from django.contrib.auth import get_user_model

from app_common.models import BaseModel
from app_products.models import ProductsModel

User = get_user_model()


class BasketItemModel(models.Model):
    product = models.ForeignKey(
        ProductsModel,
        on_delete=models.CASCADE,
        related_name="basket_items",
        verbose_name="Product"
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    class Meta:
        verbose_name = "Basket Item"
        verbose_name_plural = "Basket Items"


class BasketModel(BaseModel):
    """
    Basket Model. This model is used to store the items added to the basket by the user.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="baskets",
        verbose_name="User"
    )
    items = models.ManyToManyField(
        BasketItemModel,
        related_name="baskets",
        verbose_name="Basket Items"
    )

    def __str__(self):
        return f"Basket #{self.pk} | User: {self.user.phone_number}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    class Meta:
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"
