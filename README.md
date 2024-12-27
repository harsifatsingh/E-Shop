
# E-SHOP (CLI-Based E-Commerce Application)

Welcome to **E-SHOP**, a simple command-line application for exploring products by category/brand, viewing all products, and placing orders. This project uses a MySQL database to store product data and order records.

## Table of Contents

- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Project Setup](#project-setup)  
  - [1. Create Database and Tables](#1-create-database-and-tables)  
  - [2. Configure Database Connection](#2-configure-database-connection)  
- [How to Run](#how-to-run)  
- [Project Structure](#project-structure)  
- [Usage](#usage)  
- [Improvements & Suggestions](#improvements--suggestions)  
- [License](#license)

---

## Features

- **Category Search**: Browse products based on category.  
- **Product Listing**: List all available products and their prices.  
- **Brand Search**: Browse products based on brand.  
- **Order Placement**: Place an order for a product with a specific quantity.  
- **MySQL Integration**: Connect to a MySQL database to fetch product info and store orders.  

---

## Prerequisites

- **Python** 3.7+ installed  
- **MySQL** 5.7+ (or compatible) installed  
- `mysql-connector-python` library (use `pip install mysql-connector-python`)  

---

## Project Setup

### 1. Create Database and Tables

1. **Open MySQL console** or a GUI client (e.g., MySQL Workbench).  
2. **Create the database** and **create a user** with the specified credentials:
   ```sql
   -- Create the database
   CREATE DATABASE IF NOT EXISTS E-Commerce;

   -- Create a dedicated user (e.g., ecom_user) and set a secure password
   CREATE USER 'ecom_user'@'localhost' IDENTIFIED BY 'P@ssword123!';
   GRANT ALL PRIVILEGES ON E-Commerce.* TO 'ecom_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Select your database**:
   ```sql
   USE E-Commerce;
   ```

4. **Create the main table** (`main_table`) for products:
   ```sql
   CREATE TABLE IF NOT EXISTS main_table (
       id INT AUTO_INCREMENT PRIMARY KEY,
       PRODUCT_ID INT NOT NULL,
       PRODUCT_NAME VARCHAR(255) NOT NULL,
       PRICE DECIMAL(10, 2) NOT NULL,
       BRAND VARCHAR(255) NOT NULL,
       CATEGORY VARCHAR(255) NOT NULL,
       QUANTITY INT NOT NULL
   );
   ```

5. **Create the order table** (`order_table`) for customer orders:
   ```sql
   CREATE TABLE IF NOT EXISTS order_table (
       order_id INT AUTO_INCREMENT PRIMARY KEY,
       PRODUCT_ID INT NOT NULL,
       PRODUCT_NAME VARCHAR(255) NOT NULL,
       QUANTITY INT NOT NULL,
       CONTACT_DETAILS_OF_CUSTOMER VARCHAR(255),
       DATE_OF_DISPATCH DATE
   );
   ```

6. **Populate the `main_table`** with initial products if desired:
   ```sql
   INSERT INTO main_table 
     (PRODUCT_ID, PRODUCT_NAME, PRICE, BRAND, CATEGORY, QUANTITY)
   VALUES
     (1, 'iPhone 14', 899.99, 'Apple', 'Electronics', 10),
     (2, 'Galaxy S21', 799.00, 'Samsung', 'Electronics', 15),
     (3, 'Nike Air Max', 119.99, 'Nike', 'Footwear', 20),
     (4, 'Adidas Ultraboost', 129.99, 'Adidas', 'Footwear', 15);
   ```

### 2. Configure Database Connection

In the script, you will see:

```python
obj = mysql.connect(
    host="localhost",
    user="ecom_user",
    password="P@ssword123!",
    database="E-Commerce"
)
```

- Make sure these values (host, user, password, database) match what you set up in your MySQL environment.  
- If you need to change the host, user, password, or database name, simply update them in the script accordingly.

---

## How to Run

1. **Install dependencies** (assuming you have Python 3 and `pip`):
   ```bash
   pip install mysql-connector-python
   ```
2. **Run the script** from your terminal or command prompt:
   ```bash
   python e-shop.py
   ```
   > **Note**: Replace `e-shop.py` with whatever filename you gave to the script.

3. If the connection is successful, you will see the following banner and main menu:

   ```
   ============================================================================
   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║                       W E L C O M E   T O   E - S H O P                   ║
   ╚═══════════════════════════════════════════════════════════════════════════╝
   ============================================================================
   Connected to the E-Shop database!
   ========================================================================
   MAIN MENU
   ========================================================================
   [ 1 ]  Looking for a category.
   [ 2 ]  Looking for a product.
   [ 3 ]  Looking for a brand.
   [ 4 ]  Place an order.
   [ 5 ]  Exit.
   ```

---

## Project Structure

```
.
├─ e-shop.py                    # Main Python script
├─ README.md                    # Documentation
└─ requirements.txt             # Python dependencies
```

**Key Functions** inside `e-shop.py`:
- `main_menu()`: Displays the main menu and handles user choices.  
- `category()` : Lists categories and products within the chosen category.  
- `product()`  : Lists all products in the database.  
- `brand()`    : Lists brands and products within the chosen brand.  
- `order()`    : Places an order by updating the database accordingly.  

---

## Usage

1. **Category Search**  
   - Type `1` at the main menu, select a category by number, and see all products in that category.

2. **Product Listing**  
   - Type `2` to list all products with names and prices.

3. **Brand Search**  
   - Type `3` at the main menu, select a brand by number, and see all related products.

4. **Placing Orders**  
   - Type `4`, enter your contact info, product name, and quantity.  
   - The script updates the `main_table` and inserts a new record in `order_table`.

5. **Exit**  
   - Type `5` to exit the application.

---

## License

This project is open-source under the [MIT License](LICENSE), which allows commercial and private use, modification, and distribution.

---

### Happy Coding!

If you find any issues or have improvements, feel free to submit a pull request or open an issue. Thank you for checking out **E-SHOP**!
