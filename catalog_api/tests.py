from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_api_key.models import APIKey
from .models import Category, Product
from decimal import Decimal  # Import the Decimal type


class CategoryModelTest(TestCase):
    """
    Test suite for the Category model.
    """

    def test_create_category(self):
        """
        Ensure we can create a Category object with a name.
        """
        category = Category.objects.create(name="Books")
        self.assertEqual(category.name, "Books")
        self.assertTrue(Category.objects.filter(name="Books").exists())

    def test_category_str_representation(self):
        """
        Ensure the __str__ method of the Category model returns the category name.
        """
        category = Category.objects.create(name="Electronics")
        self.assertEqual(str(category), "Electronics")


class ProductModelTest(TestCase):
    """
    Test suite for the Product model.
    """

    def setUp(self):
        """
        Set up a common category for all tests in this class.
        """
        self.category = Category.objects.create(name="Books")

    def test_create_product(self):
        """
        Ensure we can create a Product with all required fields.
        """
        product = Product.objects.create(
            name="The Great Gatsby",
            description="A classic novel by F. Scott Fitzgerald.",
            price=15.99,
            category=self.category,
            stock_quantity=50,
            image_url="http://example.com/gatsby.jpg",
        )
        self.assertEqual(product.name, "The Great Gatsby")
        self.assertEqual(product.price, 15.99)
        self.assertEqual(product.category.name, "Books")
        self.assertTrue(Product.objects.filter(name="The Great Gatsby").exists())

    def test_product_str_representation(self):
        """
        Ensure the __str__ method of the Product model returns the product name.
        """
        product = Product.objects.create(
            name="1984", price=12.50, category=self.category
        )
        self.assertEqual(str(product), "1984")


class ProductAPITest(TestCase):
    """
    Test suite for the Product API endpoints.
    """

    def setUp(self):
        """
        Set up a test client and some initial data.
        """
        self.api_key_obj, self.api_key_str = APIKey.objects.create_key(name="test_key")
        self.client = APIClient()

        self.category_books = Category.objects.create(name="Books")
        self.category_electronics = Category.objects.create(name="Electronics")

        # Create products with distinct names and prices for clear sorting
        self.product_a = Product.objects.create(
            name="Animal Farm",
            description="A satirical novella by George Orwell",
            price=10.00,
            category=self.category_books,
            stock_quantity=10,
            is_featured=True,
        )
        self.product_z = Product.objects.create(
            name="Zealot: The Life and Times of Jesus of Nazareth",
            price=30.00,
            category=self.category_books,
            stock_quantity=10,
            is_featured=False,
        )
        self.product_m = Product.objects.create(
            name="Macbeth",
            description=" A play by William Shakespeare",
            price=20.00,
            category=self.category_books,
            stock_quantity=10,
            is_featured=False,
        )
        self.product_low_price = Product.objects.create(
            name="Charger",
            price=5.00,
            category=self.category_electronics,
            stock_quantity=10,
            is_featured=False,
        )
        self.product_high_price = Product.objects.create(
            name="Laptop",
            price=1000.00,
            category=self.category_electronics,
            stock_quantity=10,
            is_featured=True,
        )
        self.product_zero_stock = Product.objects.create(
            name="Broken Item",
            price=1.00,
            category=self.category_electronics,
            stock_quantity=0,
            is_featured=False,
        )

        # Data for creating a new product via API (if needed for other tests)
        self.valid_payload = {
            "name": "New Book",
            "description": "A newly added book.",
            "price": 18.00,
            "category": self.category_books.id,
            "stock_quantity": 75,
            "image_url": "http://example.com/newbook.jpg",
            "is_featured": False,
        }
        self.invalid_payload = {
            "description": "An invalid product.",
            "category": self.category_books.id,
        }

        # API Key for testing authenticated requests
        self.auth_headers = {'Authorization': f'API-Key {self.api_key_str}'}

    def test_list_all_products(self):
        """
        Ensure the API can retrieve a list of all products.
        """
        response = self.client.get(reverse("product-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    def test_create_product(self):
        """
        Ensure the API can create a new product.
        """
        response = self.client.post(
            reverse("product-list"),
            data=self.valid_payload,
            format="json",  # Important for sending JSON data
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Product.objects.count(), 7
        )  # Check if a new product was added to the DB
        self.assertEqual(response.data["name"], self.valid_payload["name"])
        self.assertEqual(Decimal(response.data["price"]), self.valid_payload["price"])
        self.assertTrue(Product.objects.filter(name="New Book").exists())

    def test_create_invalid_product(self):
        """
        Ensure the API does not create a product with invalid data.
        """
        response = self.client.post(
            reverse("product-list"), 
            data=self.invalid_payload, 
            format="json",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.count(), 6)  # No new product should be added

    def test_retrieve_single_product(self):
        """
        Ensure the API can retrieve a single product by its ID.
        """
        response = self.client.get(
            reverse("product-detail", kwargs={"pk": self.product_m.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product_m.name)
        self.assertEqual(
            Decimal(response.data["price"]), self.product_m.price
        )  # Price might be string in JSON
        self.assertEqual(response.data["id"], self.product_m.id)

    def test_retrieve_non_existent_product(self):
        """
        Ensure the API returns 404 for a non-existent product ID.
        """
        response = self.client.get(
            reverse("product-detail", kwargs={"pk": 99999})
        )  # Assuming 99999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- TESTS FOR FILTERING ---

    def test_filter_products_by_name(self):
        """
        Ensure products can be filtered by name.
        """
        response = self.client.get(reverse("product-list"), {"name": "farm"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.product_a.name)

    def test_filter_products_by_category(self):
        """
        Ensure products can be filtered by category ID.
        """
        response = self.client.get(
            reverse("product-list"), {"category": self.category_electronics.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # Check if the correct products are returned
        product_names = [p["name"] for p in response.data]
        self.assertIn(self.product_low_price.name, product_names)
        self.assertIn(self.product_high_price.name, product_names)
        self.assertIn(self.product_zero_stock.name, product_names)

    def test_filter_products_by_price_range(self):
        """
        Ensure products can be filtered by min_price and max_price.
        """
        # Filter for products between 10.00 and 20.00
        response = self.client.get(
            reverse("product-list"), {"min_price": 10.00, "max_price": 20.00}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        product_names = [p["name"] for p in response.data]
        self.assertIn(self.product_a.name, product_names)
        self.assertIn(self.product_m.name, product_names)

        # Filter for products above 100.00
        response = self.client.get(reverse("product-list"), {"min_price": 100.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.product_high_price.name)

    def test_filter_products_by_availability(self):
        """
        Ensure products can be filtered by availability (in stock).
        """
        response = self.client.get(reverse("product-list"), {"available": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 5
        )  # Apple, Mango, Zebra, Charger, Laptop (Broken Item is 0 stock)
        product_names = [p["name"] for p in response.data]
        self.assertIn(self.product_a.name, product_names)
        self.assertIn(self.product_z.name, product_names)
        self.assertIn(self.product_m.name, product_names)
        self.assertIn(self.product_low_price.name, product_names)
        self.assertIn(self.product_high_price.name, product_names)
        self.assertNotIn(self.product_zero_stock.name, product_names)

    def test_filter_products_by_featured_flag(self):
        """
        Ensure products can be filtered by is_featured flag.
        """
        response = self.client.get(reverse("product-list"), {"is_featured": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Apple, Laptop
        product_names = [p["name"] for p in response.data]
        self.assertIn(self.product_a.name, product_names)
        self.assertIn(self.product_high_price.name, product_names)
        self.assertNotIn(self.product_z.name, product_names)
        self.assertNotIn(self.product_m.name, product_names)
        self.assertNotIn(self.product_low_price.name, product_names)
        self.assertNotIn(self.product_zero_stock.name, product_names)

    # --- TESTS FOR SORTING ---

    def test_sort_products_by_name_asc(self):
        """
        Ensure products can be sorted by name in ascending order.
        """
        response = self.client.get(reverse("product-list"), {"ordering": "name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the order of names
        # expected_order = ["Apple", "Charger", "Laptop", "Mango", "Zebra", "Broken Item"] # Default ordering by name
        actual_order = [p["name"] for p in response.data]
        self.assertEqual(
            actual_order, sorted(actual_order)
        )  # Simple check for sorted order
        # More precise check:
        self.assertEqual(actual_order[0], self.product_a.name)
        self.assertEqual(actual_order[1], self.product_zero_stock.name)
        self.assertEqual(actual_order[2], self.product_low_price.name)

    def test_sort_products_by_name_desc(self):
        """
        Ensure products can be sorted by name in descending order.
        """
        response = self.client.get(reverse("product-list"), {"ordering": "-name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        actual_order = [p["name"] for p in response.data]
        self.assertEqual(
            actual_order, sorted(actual_order, reverse=True)
        )  # Simple check for reverse sorted order
        # More precise check:
        self.assertEqual(actual_order[0], self.product_z.name)
        self.assertEqual(actual_order[1], self.product_m.name)
        self.assertEqual(actual_order[2], self.product_high_price.name)

    def test_sort_products_by_price_asc(self):
        """
        Ensure products can be sorted by price in ascending order.
        """
        response = self.client.get(reverse("product-list"), {"ordering": "price"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        actual_prices = [
            float(p["price"]) for p in response.data
        ]  # Convert to Decimal for comparison
        self.assertEqual(actual_prices, sorted(actual_prices))
        # More precise check:
        self.assertEqual(actual_prices[0], self.product_zero_stock.price)
        self.assertEqual(actual_prices[1], self.product_low_price.price)
        self.assertEqual(actual_prices[2], self.product_a.price)

    def test_sort_products_by_price_desc(self):
        """
        Ensure products can be sorted by price in descending order.
        """
        response = self.client.get(reverse("product-list"), {"ordering": "-price"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        actual_prices = [float(p["price"]) for p in response.data]
        self.assertEqual(actual_prices, sorted(actual_prices, reverse=True))
        # More precise check:
        self.assertEqual(actual_prices[0], self.product_high_price.price)
        self.assertEqual(actual_prices[1], self.product_z.price)
        self.assertEqual(actual_prices[2], self.product_m.price)

    # --- TESTS FOR INVENTORY MANAGEMENT AND FEATURED FLAG UPDATE ---

    def test_purchase_product_decreases_stock(self):
        """
        Ensure purchasing a product decreases its stock quantity.
        """
        initial_stock = self.product_a.stock_quantity  # product_a has 10 stock
        purchase_quantity = 3

        # We'll need a new URL for purchase, e.g., 'product-purchase'
        # This will be a POST request to decrease stock
        response = self.client.post(
            reverse("product-purchase", kwargs={"pk": self.product_a.id}),
            data={"quantity": purchase_quantity},
            format="json",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Fetch the product again from the database to check updated stock
        self.product_a.refresh_from_db()
        self.assertEqual(
            self.product_a.stock_quantity, initial_stock - purchase_quantity
        )
        self.assertEqual(
            response.data["stock_quantity"], initial_stock - purchase_quantity
        )

    def test_purchase_out_of_stock_product_fails(self):
        """
        Ensure purchasing an out-of-stock product returns an error.
        """
        initial_stock = (
            self.product_zero_stock.stock_quantity
        )  # product_zero_stock has 0 stock
        purchase_quantity = 1

        response = self.client.post(
            reverse("product-purchase", kwargs={"pk": self.product_zero_stock.id}),
            data={"quantity": purchase_quantity},
            format="json",
            headers=self.auth_headers,
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )  # Or 409 Conflict
        self.assertIn(
            "not enough stock", response.data["detail"].lower()
        )  # Check for error message

        # Ensure stock quantity did not change
        self.product_zero_stock.refresh_from_db()
        self.assertEqual(self.product_zero_stock.stock_quantity, initial_stock)

    def test_update_product_featured_status(self):
        """
        Ensure the is_featured flag can be updated via API.
        """
        initial_featured_status = self.product_m.is_featured  # Should be False
        self.assertEqual(initial_featured_status, False)

        update_data = {"is_featured": True}
        response = self.client.patch(  # Use PATCH for partial update
            reverse("product-detail", kwargs={"pk": self.product_m.id}),
            data=update_data,
            format="json",
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_featured"], True)

        # Verify in database
        self.product_m.refresh_from_db()
        self.assertEqual(self.product_m.is_featured, True)

    # --- NEW TESTS FOR PERMISSIONS ---

    def test_create_product_unauthenticated(self):
        """
        Ensure creating a product without API key returns 403 Forbidden.
        """
        response = self.client.post(
            reverse('product-list'),
            data=self.valid_payload,
            format='json',
            # No headers=self.auth_headers here
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 6) # No new product should be added

    def test_update_product_unauthenticated(self):
        """
        Ensure updating a product without API key returns 403 Forbidden.
        """
        update_data = {'name': 'Unauthorized Update'}
        response = self.client.patch(
            reverse('product-detail', kwargs={'pk': self.product_a.id}),
            data=update_data,
            format='json',
            # No headers=self.auth_headers here
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.product_a.refresh_from_db()
        self.assertNotEqual(self.product_a.name, 'Unauthorized Update')

    def test_delete_product_unauthenticated(self):
        """
        Ensure deleting a product without API key returns 403 Forbidden.
        """
        response = self.client.delete(
            reverse('product-detail', kwargs={'pk': self.product_a.id})
            # No headers=self.auth_headers here
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(id=self.product_a.id).exists()) # Product should still exist

    def test_purchase_product_unauthenticated(self):
        """
        Ensure purchasing a product without API key returns 403 Forbidden.
        """
        initial_stock = self.product_a.stock_quantity
        response = self.client.post(
            reverse('product-purchase', kwargs={'pk': self.product_a.id}),
            data={'quantity': 1},
            format='json',
            # No headers=self.auth_headers here
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.product_a.refresh_from_db()
        self.assertEqual(self.product_a.stock_quantity, initial_stock)