# Flask E-Commerce Application

## Overview

Welcome to the **Flask E-Commerce Application**! This web application, built using Flask and SQLAlchemy, is designed to provide a full-featured e-commerce experience. Users can browse products, filter them by various criteria, and interact with an admin interface to manage the product catalog. The application also includes user authentication and authorization features, allowing secure access to administrative functions.

## Features

### User Authentication

- **Login:** Users can log in using their username and password. Authentication is handled securely with hashed passwords.
- **Register:** New users can register by providing a username and password. Passwords are hashed for security.
- **Logout:** Users can log out, which clears all session data and redirects them to the shop page.

### Product Management

- **Product Listing:** View all products in the shop with options to sort by price (ascending or descending).
- **Product Details:** Each product has a dedicated page displaying detailed information including price, sizes, colors, and multiple images.
- **Product Filtering:** Filter products based on category and price range to find specific items quickly.
- **Admin Interface:** Admin users can add new products to the catalog via a dedicated form, specifying details such as title, description, price, original price, category, images, sizes, and colors.
- **Product Deletion:** Admins can delete products from the catalog.

### Additional Pages

- **Home Page:** The landing page of the application.
- **About Page:** A page providing information about the application or the organization.
- **Contact Page:** A contact form page (currently non-functional).
- **Blog Page:** A page for blogging or news (currently static).
- **FAQ Page:** A page for frequently asked questions.

## Technologies Used

- **Flask:** A lightweight WSGI web application framework for Python.
- **SQLAlchemy:** An SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Flask-WTF:** Integrates Flask with WTForms to handle form rendering and validation.
- **Flask-Login:** Manages user sessions and authentication.
- **Flask-Bcrypt:** Provides password hashing for secure authentication.
- **Flask-Bootstrap:** A library for integrating Bootstrap with Flask to build responsive layouts.


The application uses the following configurations:

- **SECRET_KEY:** Used for session management and security.
- **SQLALCHEMY_DATABASE_URI:** Specifies the URI for the SQLite database.

## Database Schema

The application uses a SQLite database with the following tables:

### Product

- `id`: Integer, Primary Key
- `title`: String, Not Null
- `price`: Float, Not Null
- `sizes`: String, Not Null
- `colors`: String, Not Null
- `original_price`: Float, Not Null
- `productInfo`: Text, Not Null
- `imgUrl1`: String, Not Null
- `imgUrl2`: String
- `imgUrl3`: String
- `imgUrl4`: String
- `category`: String, Not Null

### User

- `id`: Integer, Primary Key
- `username`: String, Unique, Not Null
- `password`: String, Not Null

