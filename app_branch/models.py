from django.db import models
from django.contrib.auth import get_user_model

from app_common.models import BaseModel
from app_company.models import RestaurantModel, RestaurantProductsModel

User = get_user_model()


class ActionChoice(models.TextChoices):
    """
    ActionChoice is a class that contains choices for the action.
    """
    ADD = "add", "Add"
    REMOVE = "remove", "Remove"


class BranchModel(BaseModel):
    """
    Represents a branch of a restaurant.
    Attributes:
        name (str): Name of the branch unique.
        address (str): Address of the branch.
        restaurant (RestaurantModel): Restaurant the branch belongs to.
        is_active (bool): Indicates whether the branch is active or not.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="branches", null=True)
    name = models.CharField(max_length=64, verbose_name="Name", unique=True)
    address = models.CharField(max_length=255, verbose_name="Address")
    restaurant = models.ForeignKey(
        RestaurantModel,
        on_delete=models.CASCADE,
        related_name="branches",
        verbose_name="Restaurant"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name


class BranchProductsModel(models.Model):
    """
    Represents the products available at a branch.
    Attributes:
        branch (BranchModel): Branch the product belongs to.
        restaurant (RestaurantModel): Restaurant the product belongs to.
    """
    branch = models.ForeignKey(BranchModel, on_delete=models.CASCADE, related_name="products")
    restaurant = models.ForeignKey(RestaurantProductsModel, on_delete=models.CASCADE, related_name="branch_products")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Branch Product"
        verbose_name_plural = "Branch Products"
        unique_together = (('branch','restaurant'),)

    def __str__(self):
        return f"{self.branch.name} - {self.restaurant.name}"