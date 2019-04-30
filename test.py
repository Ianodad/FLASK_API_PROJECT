import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

# insert mutiple entries in the database
users = [
    (2, 'rolf', 'yudf'),
    (3, 'anne', 'zyz')
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

# print each row from the database
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
