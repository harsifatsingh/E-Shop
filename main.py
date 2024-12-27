import mysql.connector as mysql

obj = mysql.connect(host = "localhost", user = "root", password = "root", database = "E-Commerce")
cursor = obj.cursor()

def category():
    print("********** Category **********")
    a = "select DISTINCT CATEGORY from main_table"
    cursor.execute(a)

    fetch = cursor.fetchall()
    for i in fetch:
        print(i[0])
    print("\n")
    inpCategory = input("Enter the category: ")
    print("\n")
    print("We have the following", inpCategory, ":")
    print("\n")
    b = "select PRODUCT_NAME, PRICE from main_table where CATEGORY = '{}'".format(inpCategory)
    cursor.execute(b)
    fetch1 = cursor.fetchall()
    for i in fetch1:
        print(i[0],"```````````", i[1])

    print("----------------X-----------------")

def product():
    a = "select PRODUCT_NAME from main_table"
    cursor.execute(a)
    fetch = cursor.fetchall()
    obj.commit()

    for i in fetch:
        print(i[0],"```````````", "PRICE: ", i[1])
    
    print("----------------X-----------------")

def brand():
    print("********** Brands available are **********")
    a = "select DISTINCT BRAND from main_table"
    cursor.execute(a)
    fetch = cursor.fetchall()
    for i in fetch:
        print(i[0])
    print("\n")
    inpBrand = input("What brand are you looking for? ")
    print("\n")
    print("We have the following available products from", inpBrand, ":")
    print("\n")
    b = "select PRODUCT_NAME, PRICE from main_table where BRAND = '{}'".format(inpBrand)
    cursor.execute(b)
    fetch1 = cursor.fetchall()
    for i in fetch1:
        print(i[0],"```````````","PRICE: ",i[1])
    
    print("----------------X-----------------")


def order():
    inpContact = input("Enter your contact number: ")
    inpOrder = input("Enter the product you want to order: ")
    inpQuantity = input("Enter the quantity: ")
    qty = "select QUANTITY from main_table where PRODUCT_NAME = '{}'".format(inpOrder)
    cursor.execute(qty)
    fetch = cursor.fetchall()

    if fetch < inpQuantity:
        print("Sorry, we do not have enough quantity.")
    else:
        product_id = "select PRODUCT_ID from main_table where PRODUCT_NAME = '{}'".format(inpOrder)
        cursor.execute(product_id)
        fetch1 = cursor.fetchall()

        a = "update main_table set QUANTITY = QUANTITY - {} where PRODUCT_NAME = '{}'".format(inpQuantity, inpOrder)
        cursor.execute(a)

        obj.commit()

    c = "insert into order_table(PRODUCT_ID, PRODUCT_NAME, QUANTITY, CONTACT_DETAILS_OF_CUSTOMER, DATE_OF_DISPATCH) values({}, '{}', {}, {}, {})".format(fetch1[0][0], inpOrder, inpQuantity, inpContact, 'curdate()')
    cursor.execute(c)
    obj.commit()

    print("Order placed successfully!")

while True:
    print("********** Welcome to E-SHOP **********\n")
    while True:
        print("WELCOME TO E-SHOP :) \n")
        print("Press 1 if you are looking for a category.")
        print("Press 2 if you are looking for a product.")
        print("Press 3 if you are looking for a brand.")
        print("Press 4 if you want to place an order.\n")
        inpint = int(input("Enter your number: "))
        print("\n")
        if inpint == 1:
            category()
        elif inpint == 2:
            product()
        elif inpint == 3:
            brand()
        elif inpint == 4:
            order()
        else:
            print("ERROR!!!")
            print("Check your number.")

