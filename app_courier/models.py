from app_common.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CourierModel(BaseModel):
    """
    Courier model represents a courier in the application.
    field name for unique
    """
    name = models.CharField(max_length=64, verbose_name="Name", unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courier",
        verbose_name="User"
    )

    class Meta:
        verbose_name = "Courier"
        verbose_name_plural = "Couriers"

    def __str__(self):
        return self.name
