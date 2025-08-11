# Product Catalog API with Django

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-green.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.x-red.svg)](https://www.django-rest-framework.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-blue.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)
[![drf-yasg](https://img.shields.io/badge/Docs-Swagger/ReDoc-orange.svg)](https://drf-yasg.readthedocs.io/en/stable/)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-brightgreen?style=flat&logo=github)](https://github.com/m-arifin-ilham/Product-Catalog-API)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

***

## Overview

This project is a robust and feature-rich **Product Catalog RESTful API** built using **Django** and **Django REST Framework (DRF)**. It serves as the backend for an e-commerce platform, providing comprehensive management of product and category data. The API is designed for scalability and usability, offering advanced querying capabilities.

## Features

* **Product & Category Management:** Full CRUD (Create, Read, Update, Delete) operations for both products and categories.
* **Relational Data Modeling:** Products are linked to categories via a foreign key, demonstrating proper database relationships.
* **Advanced Filtering:** Efficiently search products by:
    * `name` (case-insensitive partial match)
    * `category` (by ID)
    * `min_price` and `max_price` (price range)
    * `available` (products with `stock_quantity > 0`)
    * `is_featured` (boolean flag)
* **Dynamic Sorting:** Order product listings by `name`, `price`, `stock_quantity`, or `created_at` in ascending or descending order.
* **Basic Inventory Management:** Products include `stock_quantity`, with a dedicated custom endpoint to simulate **purchases** and decrement stock, including handling for out-of-stock scenarios.
* **Product Attributes:** Includes fields like `image_url` and `is_featured` flag for enhanced product representation.
* **Interactive API Documentation:** Automatically generated Swagger UI and ReDoc documentation for all endpoints, making the API easy to understand and integrate with.
* **Django Admin Panel:** Leverages Django's powerful built-in admin interface for convenient data management of products and categories.

***

## Admin Panel vs. RESTful API: Different Purposes

It's important to understand the distinct roles of the Django Admin Panel and the RESTful API in this project, as they serve different users and use cases:

### Django Admin Panel: Internal Management Tool 🛠️

The Django Admin Panel is a **Graphical User Interface (GUI)** primarily designed for **internal, trusted users** (e.g., administrators, content managers, or internal staff).

* **Purpose:** To provide a quick, easy, and secure way for non-technical or semi-technical personnel to **manually manage** the application's data (create, view, update, delete products and categories) directly in the backend.
* **Use Cases:**
    * A store manager adding new products or updating stock levels.
    * An administrator reviewing all product categories.
    * Internal staff correcting data entry errors.
* **Key Characteristic:** Designed for **human interaction** and direct database manipulation via a web interface. It's a "batteries-included" tool for operational tasks.


### RESTful API (Django REST Framework): Programmatic Interface 🔌

The RESTful API, built with Django REST Framework, is a **programmatic interface** designed for **other software systems** (clients) to interact with your application's data.

* **Purpose:** To allow different applications (e.g., a public-facing e-commerce website, a mobile app, another backend service, or a third-party analytics tool) to **programmatically read from and write data** to your system in a standardized, machine-readable format (JSON).
* **Use Cases:**
    * A **frontend e-commerce website** fetching product listings to display to customers.
    * A **mobile application** allowing users to browse products and view details.
    * An **external inventory system** automatically updating product stock quantities after a sale.
    * An **analytics dashboard** pulling sales data for reporting.
* **Key Characteristic:** Designed for **machine-to-machine communication** and integration, providing flexible data access for diverse client applications.


### Why Both Are Necessary

These two interfaces are complementary and serve different needs:

* You would **not expose the Django Admin Panel to end-users** (customers) due to security risks and poor user experience.
* You would **not manually manage thousands of product updates** or integrate with external systems using the Admin Panel; that's where the API's programmatic power is essential.

Together, they provide a complete solution for both internal data management and external application integration.

***

## Architectural Design & Principles

This project utilizes Django's inherent structure, which naturally aligns with many software design principles.

* **Django's MVT (Model-View-Template) / MVC (Model-View-Controller) Pattern:** Provides a clear separation of concerns.
    * **Models (`catalog_api/models.py`):** Define the database schema and data integrity (SRP).
    * **Serializers (`catalog_api/serializers.py`):** Handle data validation and transformation (SRP).
    * **Views (`catalog_api/views.py`):** Process API requests, apply business logic, and interact with models via the ORM (SRP).
* **Django ORM (Object-Relational Mapper):** Abstracts database interactions, allowing Python objects to represent database rows. This promotes **Dependency Inversion Principle (DIP)** as views and services depend on the abstract model, not a specific database technology.
* **Django REST Framework (DRF):** Simplifies API development, providing generic views and viewsets that are **Open for Extension, Closed for Modification (OCP)**, allowing custom actions (like `purchase`) and filters to be added easily.

***

## Technologies Used

* **Python:** Core programming language.
* **Django:** High-level Python web framework.
* **Django REST Framework (DRF):** Powerful toolkit for building Web APIs in Django.
* **SQLite:** Default database for local development.
* **django-filter:** For advanced filtering capabilities.
* **drf-yasg:** For automatic generation of Swagger/OpenAPI documentation.

***

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

* Python 3.8+ installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/m-arifin-ilham/Product-Catalog-API
    cd product_catalog_api
    ```

2.  **Set up a Python virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Running the API

Ensure your virtual environment is active, then run the Django development server:

```bash
python manage.py runserver
```

The API will be accessible at `http://127.0.0.1:8000/api/`.

### Accessing Documentation
* Swagger UI: `http://127.0.0.1:8000/swagger/`
* ReDoc: `http://127.0.0.1:8000/redoc/`

### Django Admin Panel

Django provides a powerful built-in administration interface. To access and manage your product catalog data:

1.  **Create a Superuser:** If you haven't already, create an administrator account:
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set a username, email, and password.

2.  **Register Models:** Ensure your `Category` and `Product` models are registered with the admin site. (You've already done this in `catalog_api/admin.py`).

3.  **Access the Admin:**
    * Ensure your Django development server is running (`python manage.py runserver`).
    * Open your web browser and navigate to `http://127.0.0.1:8000/admin/`.
    * Log in using the superuser credentials you created.

    You will now see "Categories" and "Products" under your `CATALOG API` app, allowing you to add, view, and edit data directly.

***

## API Endpoints

All endpoints assume a base URL of `http://127.0.0.1:8000/api/`.

### Categories
| Method   | Endpoint           | Description                       |
| :------- | :----------------- | :-------------------------------- |
| `GET`    | `/categories`      | List all product categories.      |
| `POST`   | `/categories`      | Create a new product category.    |
| `GET`    | `/categories/{id}` | Retrieve a single category by ID. |
| `PUT`    | `/categories/{id}` | Update an existing category.      |
| `DELETE` | `/categories/{id}` | Delete a category.                |

### Products
| Method   | Endpoint                  | Description                                                                  |
| :------- | :------------------------ | :--------------------------------------------------------------------------- |
| `GET`    | `/products`               | List all products with advanced filtering and sorting.                       |
| `POST`   | `/products`               | Create a new product.                                                        |
| `GET`    | `/products/{id}`          | Retrieve a single product by ID.                                             |
| `PUT`    | `/products/{id}`          | Update an existing product.                                                  |
| `PATCH`  | `/products/{id}`          | Partially update an existing product (e.g., `is_featured`).                  |
| `DELETE` | `/products/{id}`          | Delete a product.                                                            |
| `POST`   | `/products/{id}/purchase` | **Custom Action:** Simulate a product purchase, decreasing `stock_quantity`. |

### `GET /products/` Query Parameters
| Parameter     | Type      | Description                                                               | Example             |
| :------------ | :-------- | :------------------------------------------------------------------------ | :------------------ |
| `name`        | `string`  | Filter by product name (case-insensitive contains).                       | `?name=keyboard`    |
| `category`    | `integer` | Filter by category ID.                                                    | `?category=1`       |
| `min_price`   | `decimal` | Filter by minimum price (inclusive).                                      | `?min_price=50.00`  |
| `max_price`   | `decimal` | Filter by maximum price (inclusive).                                      | `?max_price=150.00` |
| `available`   | `boolean` | Filter to show only in-stock products (`true`) or out-of-stock (`false`). | `?available=true`   |
| `is_featured` | `boolean` | Filter by featured status (`true` or `false`).                            | `?is_featured=true` |
| `ordering`    | `string`  | Sort results by field (e.g., `name`, `-price` for descending).            | `?ordering=-price`  |

***

## How to Run Tests

A comprehensive test suite is included to validate the API's functionality.

1.  Ensure your virtual environment is active.
2.  Run the tests:
    ```bash
    python manage.py test
    ```

***

## Future Enhancements

* **User Authentication & Authorization:** Integrate with Django's built-in authentication system and DRF's authentication classes (e.g., Token Authentication, JWT).

* **Image Uploads:** Implement actual image file uploads and storage (e.g., using cloud storage like AWS S3).

* **Pagination:** Implement more advanced pagination options (e.g., cursor-based pagination for large datasets).

* **Search Backend:** Integrate with a dedicated search engine (e.g., Elasticsearch) for more powerful and scalable search.

* **Deployment:** Deploy the API to a cloud platform like Render, Heroku, or AWS.

***

## License
This project is licensed under the MIT License.

---

*Developed by [Muhammad Arifin Ilham](https://www.linkedin.com/in/arifin-ilham-at-ska/)* 

*Current Date: August 5, 2025*


