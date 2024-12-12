from django.contrib.auth.models import AbstractUser
from django.db import models

from app_common.models import BaseModel


class UserRoleChoice(models.TextChoices):
    """
    UserRoleChoice is a class that contains choices for the user role.
    """
    ADMIN = "admin", "Admin"
    USER = "user", "User"
    RESTAURANT = "restaurant", "Restaurant"
    BRANCH = "branch", "Branch"
    COURIER = "courier", "Courier"


class UserStatusChoice(models.TextChoices):
    """
    UserStatusChoice is a class that contains choices for the user status.
    """
    ACTIVE = "active", "Active"
    DELETE = "delete", "Delete"
    INACTIVE = "inactive", "Inactive"


class UserModel(AbstractUser):
    """
    UserModel is a custom user model that extends the AbstractUser model provided by Django.
    It has additional fields such as role, status, phone_number.
    The role field is a CharField with choices to specify the user's role in the system.
    The status field is a CharField to specify the user's status in the system.
    The phone_number field is a CharField to store the user's phone number.
    """

    # fields
    role = models.CharField(
        default=UserRoleChoice.USER,
        max_length=20,
        choices=UserRoleChoice.choices)
    status = models.CharField(
        default=UserStatusChoice.ACTIVE,
        max_length=20,
        choices=UserStatusChoice.choices)
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.phone_number


class UserLocations(BaseModel):
    """
    UserLocations model represents the user's location.

    address: The user's address.
    is_default: Indicates whether the location is the default location for the user.
    address: The user's address
    user: The user who has this location.
    """

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='locations',
        verbose_name='User'
    )
    address = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'User Location'
        verbose_name_plural = 'User Locations'
