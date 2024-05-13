
# This one was a bit stressful, let me know if I went wrong anywhere
# Source is my How-too guides based on Hyperion PDF's, code is my own


#=====importing libraries=====
import sqlite3
import time


#=====Foundation=====

try:
    # Creates/connects to a database file called 'ebookstore.db' and creates a cursor object
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    # Creates an empty table called 'book'
    # Was unsure if I should add AUTOINCREMENT to primary key 'id'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            qty INTEGER)
    ''')
    db.commit()

    # Inserts new records into the table
    id_title_author_qty = [
        (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
        (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO book(id, title, author, qty) 
        VALUES (?, ?, ?, ?)''', id_title_author_qty)
    db.commit()

    # Error check function, if int value type it continues, otherwise informs user to try again
    def valid_int_input(prompt):
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print("Invalid input. Please enter a number.")


    #=====Menu Section=====

    # Simple menu loop, requesting user input
    print("    Welcome to the bookstore app!\n")
    while True:
        menu = input('''
    Select one of the following options:
    new     - Enter book
    up      - Update book
    del     - Delete book
    s       - Search books
    e       - exit

    Selection: ''').lower()

        # Allows user to create a new book record, requires title, author, qty input
        if menu == 'new':
            print("")
            # Displays book table
            cursor.execute('''
                SELECT *
                FROM book''')
            rows = cursor.fetchall()
            for row in rows:
                print(('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3])))

            print("\nThese questions are pertaining to the new book.\n")
            cursor.execute("SELECT MAX(id) FROM book")
            last_id = cursor.fetchone()[0]
            id = last_id + 1
            title = input("Please provide the Title: ")
            author = input("Please provide the Author: ")
            qty = valid_int_input("Please confirm the Quantity: ")

            cursor.execute('''
                INSERT OR IGNORE INTO book(id, title, author, qty)
                VALUES(?, ?, ?, ?)''', (id, title, author, qty))
            db.commit()
            print("Successfully added a new book: %s by %s, quantity: %d." % (title, author, qty))

        # Allows user to update the amount of books for a record based on book 'id' input
        elif menu == 'up':
            print("")
            # Displays book table
            cursor.execute('''
                SELECT *
                FROM book''')
            rows = cursor.fetchall()
            for row in rows:
                print(('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3])))

            print("\nThese questions are pertaining to an existing book.\n")
            update = input("Do you want to update the Author, Title or Quantity? ").lower()
            if update == "author":
                id = valid_int_input("Please provide the ID: ")
                author = input("Please confirm the new Author: ").capitalize()

                cursor.execute('''
                    UPDATE book
                    SET author = ?
                    WHERE id = ?''', (author, id))
                db.commit()
                print("Successfully updated the record %d Author to %s." % (id, author))
            elif update == "title":
                id = valid_int_input("Please provide the ID: ")
                title = input("Please confirm the new Title: ").capitalize()

                cursor.execute('''
                    UPDATE book
                    SET title = ?
                    WHERE id = ?''', (title, id))
                db.commit()
                print("Successfully updated the record %d Title to %s." % (id, title))
            elif update == "quantity":
                id = valid_int_input("Please provide the ID: ")
                qty = valid_int_input("Please confirm the new Quantity: ")

                cursor.execute('''
                    UPDATE book
                    SET qty = ?
                    WHERE id = ?''', (qty, id))
                db.commit()
                print("Successfully updated the record %d quantity to %d." % (id, qty))
            else:
                print("That's an invalid input. Please try: author, title, quantity.")

        # Allows user to delete a record from the database based on book 'id'
        elif menu == 'del':
            print("")
            # Displays book table
            cursor.execute('''
                SELECT *
                FROM book''')
            rows = cursor.fetchall()
            for row in rows:
                print(('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3])))

            print("\nThis will delete the books record.\n")
            id = valid_int_input("Please provide the ID for the book: ")

            cursor.execute('''
                DELETE FROM book
                WHERE id = ?''', (id,))
            db.commit()
            print("Successfully deleted the %d record." % id)

        # Allows user to search the 'book' table with input: 'author', 'title' and 'id', or shows all books
        elif menu == 's':
            print("\nHere you can search the books available.\n")
            search = input("You can search by the Book's ID, Author or Title.\nAlternatively if you wish to show the full catalogue, type books.\nInput: ").lower()
            if search == 'author':
                author = input("Please provide the Author: ")
                cursor.execute('''
                    SELECT *
                    FROM book
                    WHERE author = ?''', (author,))
                rows = cursor.fetchall()
                for row in rows:
                    print(('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3])))
            elif search == 'title':
                title = input("Please provide the Title: ")
                cursor.execute('''
                    SELECT *
                    FROM book
                    WHERE title = ?''', (title,))
                rows = cursor.fetchall()
                for row in rows:
                    print(('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3])))
            elif search == 'id' or search == 'book id':
                id = input("Please provide the book ID: ")
                cursor.execute('''
                    SELECT *
                    FROM book
                    WHERE id = ?''', (id,))
                rows = cursor.fetchall()
                for row in rows:
                    print(('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3])))
            elif search == 'books':
                cursor.execute('''
                        SELECT *
                        FROM book''')
                rows = cursor.fetchall()
                for row in rows:
                    print(('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3])))
            else:
                print("That's an invalid input. Please try: id, author, title, books.")

        # Exits program after short delay, closes db and cursor
        elif menu == 'e':
            print(f'\n\nHave a good day.\nGoodbye! :)\n')
            time.sleep(1)
            exit()

        # Checks for invalid inputs
        else:
            print("\nYou have provided an invalid input. Please try again\n\n")

except Exception as e:
    print("An error occurred: " , e)
finally:
    # Ensure the cursor and database connection are closed in case of any exception
    cursor.close()
    db.close()