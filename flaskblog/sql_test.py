import sqlite3

conn = sqlite3.connect('user.db')

c = conn.cursor()

# # to create a users table (cannot create again if alr exists)
# c.execute("""CREATE TABLE users (
#             username text,
#             email text,
#             phone text,
#             birthdate text,
#             gender text,
#             password text
# )""")

# c.execute("INSERT INTO users VALUES ('abcde', 'abcde@xyz.com', '98765432', '01/01/2001', 'F', 'abcd1234')")

#
username = input('input username = ')
password = input('input password = ')
c.execute("SELECT * FROM users WHERE username='{}' AND password = '{}'".format(username, password))

test = c.fetchall()
# for i in test:
#     print(test(i))
print(test)

conn.commit()

conn.close()
