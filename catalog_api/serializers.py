from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {
            "name": {"help_text": "The name of the product (must be unique)."},
            "description": {"help_text": "A detailed description of the product."},
            "price": {"help_text": "The selling price of the product."},
            "stock_quantity": {"help_text": "The current number of units in stock."},
            "image_url": {"help_text": "URL to the product image."},
            "is_featured": {
                "help_text": "Indicates if the product should be highlighted."
            },
            "category": {
                "help_text": "The ID of the category this product belongs to."
            },
        }
