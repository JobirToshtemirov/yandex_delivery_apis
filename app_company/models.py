from django.db import models
from django.contrib.auth import get_user_model

from app_common.models import BaseModel
from app_products.models import ProductsModel

User = get_user_model()


class RestaurantModel(BaseModel):
    """
    Represents a restaurant in the system.
    Attributes:
        name (str): The name of the restaurant unique.
        logo (ImageField): The logo of the restaurant.
        is_active (bool): Indicates whether the restaurant is active or not.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="branch", null=True)
    name = models.CharField(max_length=100, verbose_name='Name', unique=True)
    logo = models.ImageField(upload_to="restaurant_logos/", verbose_name='Logo')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str_(self):
        return self.name


class RestaurantProductsModel(models.Model):
    """
    Represents a relationship between a restaurant and a product.
    Attributes:
        restaurant (RestaurantModel): The restaurant the product belongs to.
        product (ProductsModel): The product.
    """
    restaurant = models.ForeignKey(RestaurantModel, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE, related_name="restaurants")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Restaurant Product"
        verbose_name_plural = "Restaurant Products"
        unique_together = ('restaurant', 'product')

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"
