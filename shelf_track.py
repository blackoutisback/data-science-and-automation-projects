import sqlite3

# ---------------- DATABASE SETUP ---------------- #
def create_db():
    with sqlite3.connect("ebookstore.db") as db:
        cursor = db.cursor()

        # Create author table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS author(
            id INTEGER PRIMARY KEY,
            name TEXT,
            country TEXT
        )
        """)

        # Create book table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS book(
            id INTEGER PRIMARY KEY,
            title TEXT,
            authorID INTEGER,
            qty INTEGER,
            FOREIGN KEY(authorID) REFERENCES author(id)
        )
        """)

        # Insert authors
        authors = [
            (1290, "Charles Dickens", "England"),
            (8937, "J.K. Rowling", "England"),
            (2356, "C.S. Lewis", "Ireland"),
            (6380, "J.R.R. Tolkien", "South Africa"),
            (5620, "Lewis Carroll", "England")
        ]

        cursor.executemany("INSERT OR IGNORE INTO author VALUES (?, ?, ?)", authors)

        # Insert books
        books = [
            (3001, "A Tale of Two Cities", 1290, 30),
            (3002, "Harry Potter", 8937, 40),
            (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
            (3004, "The Lord of the Rings", 6380, 37),
            (3005, "Alice in Wonderland", 5620, 12)
        ]

        cursor.executemany("INSERT OR IGNORE INTO book VALUES (?, ?, ?, ?)", books)

# ---------------- FUNCTIONS ---------------- #

def add_book():
    try:
        with sqlite3.connect("ebookstore.db") as db:
            cursor = db.cursor()

            id = int(input("Enter book ID (4 digits): "))
            title = input("Enter title: ")
            authorID = int(input("Enter author ID: "))
            qty = int(input("Enter quantity: "))

            cursor.execute("INSERT INTO book VALUES (?, ?, ?, ?)", (id, title, authorID, qty))
            print("✅ Book added!")

    except Exception as e:
        print("❌ Error:", e)


def update_book():
    try:
        with sqlite3.connect("ebookstore.db") as db:
            cursor = db.cursor()

            id = int(input("Enter book ID to update: "))

            print("1. Update Quantity")
            print("2. Update Title")
            print("3. Update Author")
            choice = input("Choose: ")

            if choice == "1":
                qty = int(input("New quantity: "))
                cursor.execute("UPDATE book SET qty=? WHERE id=?", (qty, id))

            elif choice == "2":
                title = input("New title: ")
                cursor.execute("UPDATE book SET title=? WHERE id=?", (title, id))

            elif choice == "3":
                name = input("New author name: ")
                country = input("New country: ")

                cursor.execute("""
                UPDATE author
                SET name=?, country=?
                WHERE id = (SELECT authorID FROM book WHERE id=?)
                """, (name, country, id))

            print("✅ Updated!")

    except Exception as e:
        print("❌ Error:", e)


def delete_book():
    try:
        with sqlite3.connect("ebookstore.db") as db:
            cursor = db.cursor()

            id = int(input("Enter book ID to delete: "))
            cursor.execute("DELETE FROM book WHERE id=?", (id,))
            print("🗑️ Book deleted!")

    except Exception as e:
        print("❌ Error:", e)


def search_book():
    try:
        with sqlite3.connect("ebookstore.db") as db:
            cursor = db.cursor()

            title = input("Enter title to search: ")
            cursor.execute("SELECT * FROM book WHERE title LIKE ?", ('%' + title + '%',))

            results = cursor.fetchall()

            if results:
                for book in results:
                    print(book)
            else:
                print("No book found.")

    except Exception as e:
        print("❌ Error:", e)


def view_books():
    try:
        with sqlite3.connect("ebookstore.db") as db:
            cursor = db.cursor()

            cursor.execute("""
            SELECT book.title, author.name, author.country
            FROM book
            INNER JOIN author
            ON book.authorID = author.id
            """)

            results = cursor.fetchall()

            print("\nDetails\n" + "-"*40)
            for title, name, country in results:
                print(f"Title: {title}")
                print(f"Author: {name}")
                print(f"Country: {country}")
                print("-"*40)

    except Exception as e:
        print("❌ Error:", e)


# ---------------- MAIN MENU ---------------- #
def menu():
    while True:
        print("""
1. Enter book
2. Update book
3. Delete book
4. Search books
5. View all books
0. Exit
        """)

        choice = input("Choose option: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            search_book()
        elif choice == "5":
            view_books()
        elif choice == "0":
            print("Goodbye 👋")
            break
        else:
            print("Invalid option!")


# ---------------- RUN PROGRAM ---------------- #
create_db()
menu()
