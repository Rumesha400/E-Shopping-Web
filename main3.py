import mysql.connector
import nltk
import re
from nltk.chat.util import Chat, reflections

# Initialize NLTK
nltk.download("punkt")

# Connect to MySQL database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eshop2"
    )
    cursor = conn.cursor()

    def Query_Output_Name(product_name):
        cursor.execute(
            "SELECT products.name, products.description, products.company, products.price, categories1.name "
            "FROM Products "
            "INNER JOIN categories1 ON products.category_id = categories1.category_id "
            "WHERE products.name = %s", (product_name , )
        )
        product_rows = cursor.fetchall()
        return product_rows

    def Query_Output_Category(category):
        cursor.execute(
            "SELECT products.name, products.description, products.company, products.price "
            "FROM Products "
            "INNER JOIN categories1 ON products.category_id = categories1.category_id "
            "WHERE categories1.name = %s", (category , )
        )
        product_rows = cursor.fetchall()
        return product_rows

    def Query_Output_Price(product_price):
        cursor.execute(
            "SELECT products.company, products.name, products.description, products.price, categories1.name "
            "FROM Products "
            "INNER JOIN categories1 ON products.category_id = categories1.category_id "
            "WHERE products.price = %s", (product_price , )
        )
        product_rows = cursor.fetchall()
        return product_rows

    def Query_Output_Company(company_name):
        cursor.execute(
            "SELECT products.name, products.description, products.company, products.price, categories1.name "
            "FROM Products "
            "INNER JOIN categories1 ON products.category_id = categories1.category_id "
            "WHERE products.company = %s", (company_name , )
        )
        product_rows = cursor.fetchall()
        return product_rows

    def Query_Output_Category_Price(category, min_price, max_price):
        cursor.execute(
            "SELECT products.name, products.description, products.company, products.price, categories1.name "
            "FROM Products "
            "INNER JOIN categories1 ON products.category_id = categories1.category_id "
            "WHERE categories1.name = %s AND products.price BETWEEN %s AND %s", (category, min_price, max_price)
        )
        product_rows = cursor.fetchall()
        return product_rows

    def Query_Output_Description(description):
        cursor.execute(
            "SELECT products.name, products.description, products.company, products.price, categories1.name "
            "FROM Products "
            "INNER JOIN categories1 ON products.category_id = categories1.category_id "
            "WHERE products.description LIKE %s", ('%' + description + '%',)
        )
        product_rows = cursor.fetchall()
        return product_rows

    def Query_Low_Inventory(threshold):
        cursor.execute(
            "SELECT products.name, products.description, products.company, products.price, categories1.name "
            "FROM Products "
            "INNER JOIN categories1 ON products.category_id = categories1.category_id "
            "WHERE products.inventory_quantity < %s", (threshold,)
        )
        product_rows = cursor.fetchall()
        return product_rows

    def Query_Orders_By_Customer_Email(email):
        cursor.execute(
            "SELECT * FROM Orders WHERE customer_id IN (SELECT customer_id FROM Customers WHERE email = %s)", (email,)
        )
        order_rows = cursor.fetchall()
        return order_rows

    def Query_Customers_By_Phone(phone_number):
        cursor.execute(
            "SELECT * FROM Customers WHERE phone = %s", (phone_number,)
        )
        customer_rows = cursor.fetchall()
        return customer_rows

    def Query_Orders_By_Customer_Name(first_name, last_name):
        cursor.execute(
            "SELECT * FROM Orders WHERE customer_id IN (SELECT customer_id FROM Customers WHERE first_name = %s AND last_name = %s)", (first_name, last_name)
        )
        order_rows = cursor.fetchall()
        return order_rows

    def Query_Output_Price_Range(min_price, max_price):
        cursor.execute(
            "SELECT products.name, products.description, products.company, products.price, categories1.name "
            "FROM Products "
            "INNER JOIN categories1 ON products.category_id = categories1.category_id "
            "WHERE products.price BETWEEN %s AND %s", (min_price, max_price)
        )
        product_rows = cursor.fetchall()
        return product_rows
  
    def Query_Trendy_Winter_Jackets():
        cursor.execute(
            "SELECT products.name, products.description, products.company, products.price, categories1.name "
            "FROM Products "
            "INNER JOIN categories1 ON products.category_id = categories1.category_id "
            "WHERE products.description = 'jacket' AND products.season = 'winter' "
            "ORDER BY products.release_date DESC "
            "LIMIT 10"
        )
        product_rows = cursor.fetchall()
        return product_rows
    def Query_Cozy_Sweaters():
        cursor.execute(
            "SELECT products.name, products.description, products.company, products.price, categories1.name "
            "FROM Products "
            "INNER JOIN categories1 ON products.category_id = categories1.category_id "
            "WHERE products.type = 'sweater' AND products.season = 'winter' "
            "ORDER BY products.price ASC "
            "LIMIT 10"
        )
        product_rows = cursor.fetchall()
        return product_rows
    def Query_Popular_TShirt_Designs():
        cursor.execute(
            "SELECT products.name, products.description, products.company, products.price, categories1.name "
            "FROM Products "
            "INNER JOIN categories1 ON products.category_id = categories1.category_id "
            "WHERE products.type = 't-shirt' "
            "ORDER BY products.sales DESC "
            "LIMIT 10"
        )
        product_rows = cursor.fetchall()
        return product_rows
    def Query_Latest_Sneaker_Releases():
        cursor.execute(
            "SELECT products.name, products.description, products.company, products.price, categories1.name "
            "FROM Products "
            "INNER JOIN categories1 ON products.category_id = categories1.category_id "
            "WHERE products.type = 'sneaker' "
            "ORDER BY products.release_date DESC "
            "LIMIT 10"
        )
        product_rows = cursor.fetchall()
        return product_rows

    # Fetch data from the database to use as pairs for the chatbot
    pairs = [
        ['Show the latest Heels', Query_Output_Name('Heels')],
        ['What are the product in childrens Shoes section?', Query_Output_Category('Childrens Shoes')],
        ['399.99', Query_Output_Price('399.99')],
        ['Show the latest Heels', Query_Output_Name('Heels')],
        ['What are the products in the Children\'s Shoes section?', Query_Output_Category('Childrens Shoes')],
        ['399.99', Query_Output_Price('399.99')],
        ['Show products from Nike', Query_Output_Company('Nike')],
        ['Show products in the range $50 to $100 in the Women\'s Clothing category', Query_Output_Category_Price('Womens Clothing', 50, 100)],
        ['Find products with "running" in the description', Query_Output_Description('running')],
        ['Show products with low inventory (less than 10 items)', Query_Low_Inventory(10)],
        ['Show orders by email address example@example.com', Query_Orders_By_Customer_Email('example@example.com')],
        ['Find customers by phone number +1234567890', Query_Customers_By_Phone('+1234567890')],
        ['Show orders placed by John Doe', Query_Orders_By_Customer_Name('John', 'Doe')],
        ['Show me products between $50 and $100', Query_Output_Price_Range(50, 100)],
        ['Gifting ideas below 30$', Query_Output_Price_Range(0, 30)],
        ["Show me trendy jackets for the winter season.", Query_Trendy_Winter_Jackets()],
        ["I need some cozy sweaters for cold weather, can you help?", Query_Cozy_Sweaters()],
        ["What are the popular t-shirt designs?", Query_Popular_TShirt_Designs()],
        ["what's up?" , ["Not much, just trying to help you find some products."]],
        ["how are you?" , ["I'm just a computer program, but I'm here to help you."]],
        ["i'm good" , ["That's great to hear! How can I assist you today?"]],
        ["i want to buy something?" , ["Sure, I can help you with that. What are you looking to buy?"]],
        ["i'm looking for" , ["What kind of product are you looking for?"]],
        ["can you help me find?" , ["Of course, I'd be happy to help you find what you're looking for."]],
        ["i need" , ["What do you need? I can help you find it."]],
        ["do you have any product" , ["Yes, we have many products. What are you looking for?"]],
        ["bye" , ["Goodbye! Have a great day!"]],
        ["see you later" , ["See you later!"]],
        ["quit" , ["Goodbye! Have a great day!"]],
        ["exit" , ["Goodbye! Have a great day!"]],
        ["done" , ["Goodbye! Have a great day!"]],
    ]


    # Create the chatbot instance
    chatbot = Chat(pairs, reflections)

#Run the chatbot
    print("WELCOME TO E-COMMERCE CHATBOT!")
    print("------------------------------------------------------------------------------------")
    print("Enter a Question or Quit, Exit, Done to exit from the chat bot")
    print("-----------------------------------------------------------------------------------")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ['quit', 'exit', 'done']:
            break
        else:
            response = chatbot.respond(user_input)
            print("Chatbot:", response)
            print("----------------------------------------------------------------------------------------")

except mysql.connector.Error as err:
    print("Error connecting to MySQL:", err)

finally:
    # Close the database connection
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()