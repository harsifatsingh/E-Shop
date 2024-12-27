import mysql.connector as mysql

# --- Database Connection ---
try:
    obj = mysql.connect(
        host="localhost",
        user="ecom_user",
        password="P@ssword123!",
        database="E-Commerce"
    )
    cursor = obj.cursor()
    print("Connected to the E-Commerce database.\n")
except mysql.Error as err:
    print(f"Error: {err}")
    exit()


# --- Category Function ---
def category():
    """
    Displays distinct categories from the database and prompts the user
    to select one. Shows the products under the chosen category.
    """
    print("********** Category **********")
    query = "SELECT DISTINCT CATEGORY FROM main_table"
    cursor.execute(query)
    categories = cursor.fetchall()

    if not categories:
        print("No categories available.\n")
        return

    # Display categories with numbers
    for idx, cat in enumerate(categories, start=1):
        print(f"{idx}. {cat[0]}")
    print()

    # Prompt user for category selection
    try:
        inp = int(input("Enter the number corresponding to the category: ").strip())
        if inp < 1 or inp > len(categories):
            print("Invalid selection. Please enter a valid number.\n")
            return
    except ValueError:
        print("Invalid input. Please enter a numerical value.\n")
        return

    selected_category = categories[inp - 1][0]
    print(f"\nWe have the following products in '{selected_category}':\n")

    # Fetch and display products in the selected category
    query = "SELECT PRODUCT_NAME, PRICE FROM main_table WHERE CATEGORY = %s"
    cursor.execute(query, (selected_category,))
    products = cursor.fetchall()

    if products:
        for product_name, price in products:
            print(f"{product_name} - Price: {price}")
    else:
        print("No products found in this category.")

    print("----------------X-----------------\n")


# --- Product Function ---
def product():
    """
    Displays all products from the database with their prices.
    """
    print("********** Products **********")
    query = "SELECT PRODUCT_NAME, PRICE FROM main_table"
    cursor.execute(query)
    products = cursor.fetchall()

    if not products:
        print("No products available.")
    else:
        for product_name, price in products:
            print(f"{product_name} - PRICE: {price}")

    print("----------------X-----------------\n")


# --- Brand Function ---
def brand():
    """
    Displays distinct brands from the database and prompts the user
    to select one. Shows the products under the chosen brand.
    """
    print("********** Brands Available **********")
    query = "SELECT DISTINCT BRAND FROM main_table"
    cursor.execute(query)
    brands = cursor.fetchall()

    if not brands:
        print("No brands available.\n")
        return

    # Display brands with numbers
    for idx, br in enumerate(brands, start=1):
        print(f"{idx}. {br[0]}")
    print()

    # Prompt user for brand selection
    try:
        inp = int(input("Enter the number corresponding to the brand: ").strip())
        if inp < 1 or inp > len(brands):
            print("Invalid selection. Please enter a valid number.\n")
            return
    except ValueError:
        print("Invalid input. Please enter a numerical value.\n")
        return

    selected_brand = brands[inp - 1][0]
    print(f"\nWe have the following available products from '{selected_brand}':\n")

    # Fetch and display products under the selected brand
    query = "SELECT PRODUCT_NAME, PRICE FROM main_table WHERE BRAND = %s"
    cursor.execute(query, (selected_brand,))
    products = cursor.fetchall()

    if products:
        for product_name, price in products:
            print(f"{product_name} - PRICE: {price}")
    else:
        print("No products found for this brand.")

    print("----------------X-----------------\n")


# --- Order Function ---
def order():
    """
    Prompts the user for contact number, product name, and quantity, then
    places an order if sufficient quantity is available.
    """
    try:
        # Get user inputs
        inpContact = input("Enter your contact number: ").strip()
        if not inpContact.isdigit():
            print("Invalid contact number.\n")
            return

        inpOrder = input("Enter the product you want to order: ").strip()
        if not inpOrder:
            print("Invalid product name.\n")
            return

        inpQuantity = int(input("Enter the quantity: "))
        if inpQuantity <= 0:
            print("Quantity must be a positive integer.\n")
            return

        # Check quantity in the database
        query = "SELECT QUANTITY, PRODUCT_ID FROM main_table WHERE PRODUCT_NAME = %s"
        cursor.execute(query, (inpOrder,))
        result = cursor.fetchone()

        if result:
            available_qty, product_id = result
            if available_qty < inpQuantity:
                print("Sorry, we do not have enough quantity.\n")
            else:
                # Update quantity in the main table
                update_query = "UPDATE main_table SET QUANTITY = QUANTITY - %s WHERE PRODUCT_NAME = %s"
                cursor.execute(update_query, (inpQuantity, inpOrder))
                obj.commit()

                # Insert the order into order_table
                insert_query = """
                    INSERT INTO order_table 
                    (PRODUCT_ID, PRODUCT_NAME, QUANTITY, CONTACT_DETAILS_OF_CUSTOMER, DATE_OF_DISPATCH) 
                    VALUES (%s, %s, %s, %s, CURDATE())
                """
                cursor.execute(insert_query, (product_id, inpOrder, inpQuantity, inpContact))
                obj.commit()

                print("Order placed successfully!\n")
        else:
            print("Product not found.\n")

    except ValueError:
        print("Invalid input. Quantity must be an integer.\n")
    except mysql.Error as err:
        print(f"Database error: {err}\n")


# --- Main Menu Function ---
def main_menu():
    """
    Displays the main menu and prompts the user for an action:
    1) Category
    2) Product
    3) Brand
    4) Place an order
    5) Exit
    """
    while True:
        print("********** Welcome to E-SHOP **********\n")
        print("Press 1 if you are looking for a category.")
        print("Press 2 if you are looking for a product.")
        print("Press 3 if you are looking for a brand.")
        print("Press 4 if you want to place an order.")
        print("Press 5 to exit.\n")

        try:
            choice = int(input("Enter your choice: ").strip())
            print()

            if choice == 1:
                category()
            elif choice == 2:
                product()
            elif choice == 3:
                brand()
            elif choice == 4:
                order()
            elif choice == 5:
                print("Thank you for visiting E-SHOP. Goodbye!")
                break
            else:
                print("ERROR!!! Invalid choice. Please try again.\n")

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.\n")


# --- Entry Point ---
if __name__ == "__main__":
    main_menu()
    cursor.close()
    obj.close()
