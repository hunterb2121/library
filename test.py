from helpers import get_db_connection

db_con, db_cur = get_db_connection()

username = db_cur.execute("SELECT username FROM users WHERE id = ?", (1,))
username = username.fetchall()[0][0]
print(username)