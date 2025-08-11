# from django.shortcuts import render
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import viewsets, status
from django_filters.rest_framework import (
    DjangoFilterBackend,
)  # Import the filter backend
from rest_framework.filters import OrderingFilter  # Import OrderingFilter
from .filters import ProductFilter  # Import your custom filterset
from rest_framework.decorators import action  # Import action decorator
from rest_framework.response import Response  # Import Response


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing products in the catalog.

    Provides CRUD operations, filtering by name, category, price range,
    availability, and featured status, and sorting by various fields.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = [
        "name",
        "price",
        "stock_quantity",
        "created_at",
    ]  # Specify fields for ordering
    # You can also set a default ordering if no 'ordering' param is provided:
    # ordering = ['name']

    # --- Custom Action for Product Purchase ---
    @action(detail=True, methods=["post"])
    def purchase(self, request, pk=None):
        """
        Custom action to simulate purchasing a product, decreasing its stock.
        Requires 'quantity' in the request body.
        """
        product = self.get_object()  # Get the specific product instance

        # Get quantity from request body
        quantity = request.data.get("quantity")

        # Input validation for quantity
        if quantity is None:
            return Response(
                {"detail": "Quantity is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response(
                    {"detail": "Quantity must be a positive integer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"detail": "Quantity must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check for sufficient stock
        if product.stock_quantity < quantity:
            return Response(
                {
                    "detail": f"Not enough stock. Only {product.stock_quantity} available."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Decrease stock quantity
        product.stock_quantity -= quantity
        product.save()  # Save changes to the database

        # Return updated product data
        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
