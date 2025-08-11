import django_filters
from .models import (
    Product,
    Category,
)  # Import Category if you plan to filter by category name later


class ProductFilter(django_filters.FilterSet):
    # Filter by name (case-insensitive contains)
    name = django_filters.CharFilter(lookup_expr="icontains")

    # Filter by price range
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte"
    )  # Greater than or equal
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte"
    )  # Less than or equal

    # Filter by category (using category ID)
    category = django_filters.NumberFilter(
        field_name="category__id"
    )  # __id allows filtering by FK ID

    # Filter by availability (stock_quantity > 0)
    # This is a custom method filter
    available = django_filters.BooleanFilter(method="filter_available")

    # Filter by is_featured flag
    is_featured = django_filters.BooleanFilter(field_name="is_featured")

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "min_price",
            "max_price",
            "available",
            "is_featured",
        ]

    def filter_available(self, queryset, name, value):
        """
        Custom filter method for 'available' field.
        If value is True, return products with stock_quantity > 0.
        If value is False, return products with stock_quantity = 0.
        """
        if value:
            return queryset.filter(stock_quantity__gt=0)  # __gt means "greater than"
        else:
            return queryset.filter(
                stock_quantity=0
            )  # For products that are NOT available (out of stock)
