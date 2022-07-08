from flaskblog import app
import sqlite3

if __name__ == '__main__':
    # conn = sqlite3.connect('site.db')
    # c = conn.cursor()
    # # # to create a users table (cannot create again if alr exists)
    # c.execute("""CREATE TABLE users (
    #             username text,
    #             email text,
    #             password text
    # )""")
    # c.execute("""CREATE TABLE post (
    #                 id text,
    #                 title text,
    #                 content text,
    #                 user_id text
    #     )""")
    # conn.commit()
    # conn.close()
    app.run(debug=True, host='0.0.0.0', port='9999')
