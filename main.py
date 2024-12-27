import mysql.connector as mysql

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
BOLD_GREEN = "\033[1;32m"
BOLD_BLUE = "\033[1;34m"
BOLD_MAGENTA = "\033[1;35m"
BOLD_YELLOW = "\033[1;33m"
BOLD_CYAN = "\033[1;36m"
RED = "\033[0;31m"

# ASCII art banner
BANNER = r"""
=============================================================================
╔═══════════════════════════════════════════════════════════════════════════╗
║                       W E L C O M E   T O   E - S H O P                   ║
╚═══════════════════════════════════════════════════════════════════════════╝
=============================================================================
"""

def print_section_header(title: str):
    """Prints a nicely formatted header for a major section."""
    print()
    print("=" * 73)
    print(f"{BOLD}{title.upper()}{RESET}")
    print("=" * 73)

def print_subsection_header(title: str):
    """Prints a minimal subsection header (e.g., 'Category', 'Products')."""
    print()
    print(f"{BOLD_BLUE}{title}{RESET}")
    print()

def print_spacer():
    """Prints a simple spacer line to separate sections."""
    print()
    print("─" * 73)
    print()

# --- Database Connection ---
try:
    obj = mysql.connect(
        host="localhost",
        user="ecom_user",
        password="P@ssword123!",
        database="E-Commerce"
    )
    cursor = obj.cursor()
    
    # Print the banner
    print(BANNER)
    
    # Connected message
    print(f"{BOLD_GREEN}Connected to the E-Commerce database!{RESET}\n")
except mysql.Error as err:
    print(f"{RED}Error: {err}{RESET}")
    exit()


# --- Category Function ---
def category():
    print_section_header("Category Search")
    print_subsection_header("Category")

    query = "SELECT DISTINCT CATEGORY FROM main_table"
    cursor.execute(query)
    categories = cursor.fetchall()

    if not categories:
        print("No categories available.\n")
        return

    for idx, cat in enumerate(categories, start=1):
        print(f"{idx}. {cat[0]}")
    print()

    try:
        inp = int(input("Enter the number corresponding to the category: ").strip())
        if inp < 1 or inp > len(categories):
            print(f"{RED}Invalid selection. Please enter a valid number.\n{RESET}")
            return
    except ValueError:
        print(f"{RED}Invalid input. Please enter a numerical value.\n{RESET}")
        return

    selected_category = categories[inp - 1][0]
    print(f"\nWe have the following products in '{selected_category}':\n")

    query = "SELECT PRODUCT_NAME, PRICE FROM main_table WHERE CATEGORY = %s"
    cursor.execute(query, (selected_category,))
    products = cursor.fetchall()

    if products:
        for product_name, price in products:
            print(f"{product_name} - Price: {price}")
    else:
        print("No products found in this category.")

    print_spacer()


# --- Product Function ---
def product():
    print_section_header("Product List")
    print_subsection_header("Products")

    query = "SELECT PRODUCT_NAME, PRICE FROM main_table"
    cursor.execute(query)
    products = cursor.fetchall()

    if not products:
        print("No products available.")
    else:
        for product_name, price in products:
            print(f"{product_name} - PRICE: {price}")

    print_spacer()


# --- Brand Function ---
def brand():
    print_section_header("Brand Search")
    print_subsection_header("Brands Available")

    query = "SELECT DISTINCT BRAND FROM main_table"
    cursor.execute(query)
    brands = cursor.fetchall()

    if not brands:
        print("No brands available.\n")
        return

    for idx, br in enumerate(brands, start=1):
        print(f"{idx}. {br[0]}")
    print()

    try:
        inp = int(input("Enter the number corresponding to the brand: ").strip())
        if inp < 1 or inp > len(brands):
            print(f"{RED}Invalid selection. Please enter a valid number.\n{RESET}")
            return
    except ValueError:
        print(f"{RED}Invalid input. Please enter a numerical value.\n{RESET}")
        return

    selected_brand = brands[inp - 1][0]
    print(f"\nWe have the following available products from '{selected_brand}':\n")

    query = "SELECT PRODUCT_NAME, PRICE FROM main_table WHERE BRAND = %s"
    cursor.execute(query, (selected_brand,))
    products = cursor.fetchall()

    if products:
        for product_name, price in products:
            print(f"{product_name} - PRICE: {price}")
    else:
        print("No products found for this brand.")

    print_spacer()


# --- Order Function ---
def order():
    print_section_header("Place an Order")

    try:
        inpContact = input(f"{BOLD_GREEN}Enter your contact number:{RESET} ").strip()
        if not inpContact.isdigit():
            print(f"{RED}Invalid contact number.\n{RESET}")
            return

        inpOrder = input(f"{BOLD_GREEN}Enter the product you want to order:{RESET} ").strip()
        if not inpOrder:
            print(f"{RED}Invalid product name.\n{RESET}")
            return

        inpQuantity = int(input(f"{BOLD_GREEN}Enter the quantity:{RESET} "))
        if inpQuantity <= 0:
            print(f"{RED}Quantity must be a positive integer.\n{RESET}")
            return

        query = "SELECT QUANTITY, PRODUCT_ID FROM main_table WHERE PRODUCT_NAME = %s"
        cursor.execute(query, (inpOrder,))
        result = cursor.fetchone()

        if result:
            available_qty, product_id = result
            if available_qty < inpQuantity:
                print(f"{RED}Sorry, we do not have enough quantity.\n{RESET}")
            else:
                update_query = "UPDATE main_table SET QUANTITY = QUANTITY - %s WHERE PRODUCT_NAME = %s"
                cursor.execute(update_query, (inpQuantity, inpOrder))
                obj.commit()

                insert_query = """
                    INSERT INTO order_table 
                    (PRODUCT_ID, PRODUCT_NAME, QUANTITY, CONTACT_DETAILS_OF_CUSTOMER, DATE_OF_DISPATCH) 
                    VALUES (%s, %s, %s, %s, CURDATE())
                """
                cursor.execute(insert_query, (product_id, inpOrder, inpQuantity, inpContact))
                obj.commit()

                print(f"{BOLD_MAGENTA}Order placed successfully!\n{RESET}")
        else:
            print(f"{RED}Product not found.\n{RESET}")

    except ValueError:
        print(f"{RED}Invalid input. Quantity must be an integer.\n{RESET}")
    except mysql.Error as err:
        print(f"{RED}Database error: {err}\n{RESET}")


# --- Main Menu Function ---
def main_menu():
    while True:
        print_section_header("MAIN MENU")
        
        print(f"{BOLD}[ 1 ]{RESET}  Looking for a category.")
        print(f"{BOLD}[ 2 ]{RESET}  Looking for a product.")
        print(f"{BOLD}[ 3 ]{RESET}  Looking for a brand.")
        print(f"{BOLD}[ 4 ]{RESET}  Place an order.")
        print(f"{BOLD}[ 5 ]{RESET}  Exit.\n")

        choice = input("Enter your choice: ").strip()
        print()
        
        if not choice.isdigit():
            print(f"{RED}Invalid input. Please enter a number between 1 and 5.\n{RESET}")
            continue
        
        choice = int(choice)
        
        if choice == 1:
            category()
        elif choice == 2:
            product()
        elif choice == 3:
            brand()
        elif choice == 4:
            order()
        elif choice == 5:
            print(f"{BOLD_GREEN}Thank you for visiting E-SHOP. Goodbye!{RESET}")
            break
        else:
            print(f"{RED}ERROR!!! Invalid choice. Please try again.\n{RESET}")


# --- Entry Point ---
if __name__ == "__main__":
    main_menu()
    cursor.close()
    obj.close()
