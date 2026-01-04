import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",          
    password="YOUR_MYSQL_PASSWORD",  
    database="library_db"
)

cursor = db.cursor()

def add_book():
    book_id = int(input("Enter Book ID: "))
    book_name = input("Enter Book Name: ")
    author = input("Enter Author Name: ")
    status = "Available"

    query = "INSERT INTO books (book_id, book_name, author, status) VALUES (%s, %s, %s, %s)"
    values = (book_id, book_name, author, status)

    try:
        cursor.execute(query, values)
        db.commit()
        print("Book added successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def view_books():
    cursor.execute("SELECT * FROM books")
    records = cursor.fetchall()

    if not records:
        print("No books found.")
        return

    print("\nID | Book Name | Author | Status")
    print("-" * 50)
    for row in records:
        print(row[0], "|", row[1], "|", row[2], "|", row[3])

def search_book():
    book_id = int(input("Enter Book ID to search: "))
    cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
    record = cursor.fetchone()

    if record:
        print("Book Found:", record)
    else:
        print("Book not found.")

def issue_book():
    book_id = int(input("Enter Book ID to issue: "))
    cursor.execute(
        "UPDATE books SET status='Issued' WHERE book_id=%s AND status='Available'",
        (book_id,)
    )

    if cursor.rowcount == 0:
        print("Book not available or already issued.")
    else:
        db.commit()
        print("Book issued successfully.")

def return_book():
    book_id = int(input("Enter Book ID to return: "))
    cursor.execute(
        "UPDATE books SET status='Available' WHERE book_id=%s AND status='Issued'",
        (book_id,)
    )

    if cursor.rowcount == 0:
        print("Book was not issued.")
    else:
        db.commit()
        print("Book returned successfully.")

def delete_book():
    book_id = int(input("Enter Book ID to delete: "))
    cursor.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
    db.commit()

    if cursor.rowcount == 0:
        print("Book not found.")
    else:
        print("Book deleted successfully.")

def menu():
    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Book")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Delete Book")
        print("7. Exit")

        choice = input("Enter choice (1-7): ")

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            issue_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            delete_book()
        elif choice == "7":
            print("Exiting system.")
            break
        else:
            print("Invalid choice.")

menu()

cursor.close()
db.close()
