import sqlite3

class UserRepository:
    def getUser(self, userName):
        conn = sqlite3.connect('SampathPOS.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (userName,))
        user = cursor.fetchall()
        conn.close()
        return user
