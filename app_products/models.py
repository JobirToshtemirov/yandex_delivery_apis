from django.db import models

from app_common.models import BaseModel


class CategoryModel(models.Model):
    """
    Represents a category of products.

    name: The name of the category.
    status: Indicates whether the category is active or not.
    """
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductsModel(BaseModel):
    """
    Represents a product.

    name: The name of the product.
    description: A brief description of the product.
    price: The price of the product.
    category: The category of the product.
    status: Indicates whether the product is active or not.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.CASCADE,
        related_name="products"
    )
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Foods'


class ProductImageModel(BaseModel):
    """
    Represents an image associated with a product.

    product: The product the image belongs to.
    image: The image file.
    is_main_image: Indicates whether this image is the main image for the product.
    status: Indicates whether the image is active or not.
    """
    # fields
    product = models.ForeignKey(
        ProductsModel,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to='products/')
    is_main_image = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'