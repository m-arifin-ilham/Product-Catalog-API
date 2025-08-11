from django.db import models


class Category(models.Model):
    """
    Represents a product category (e.g., 'Fiction', 'Non-Fiction').
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Represents a product in the catalog.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    # ForeignKey to link a product to a Category
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # If a category is deleted, set this field to NULL
        related_name="products",  # This allows us to access a category's products easily
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
