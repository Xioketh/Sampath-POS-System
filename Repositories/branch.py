import sqlite3

def getAll():
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM branch')
    branches = cursor.fetchall()
    conn.close()
    return branches


def search_branch_in_db(keyword):
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()

    if keyword.isdigit():
        query = 'SELECT * FROM branch WHERE id = ?'
        parameters = (keyword,)
    else:
        query = 'SELECT * FROM branch WHERE location = ?'
        parameters = (keyword,)

    cursor.execute(query, parameters)
    branch = cursor.fetchall()
    conn.close()
    return branch


def add_brach_to_db(name, location):
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO branch (name, location)
        VALUES (?, ?)
    ''', (name, location))
    conn.commit()
    conn.close()