import sqlite3
def init_db():
    conn = sqlite3.connect('../SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS branch (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productList (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            qty INTEGER,
            price DOUBLE
        )
    ''')
    cursor.execute('''
          CREATE TABLE IF NOT EXISTS sales (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              totalQty INTEGER,
              totalAmount DOUBLE,
              saleDate TEXT,
              branchName TEXT
          )
      ''')
    cursor.execute('''
              CREATE TABLE IF NOT EXISTS saleProducts (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  saleId TEXT,
                  productId TEXT,
                  totalQty INTEGER,
                  totalAmount DOUBLE,
                  unitPrice DOUBLE
              )
          ''')
    cursor.execute('''
              CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  password TEXT
              )
          ''')
    cursor.execute('''
                  CREATE TABLE IF NOT EXISTS productActivity (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      productId TEXT,
                      history TEXT,
                      updateDate TEXT
                  )
              ''')
    conn.commit()
    conn.close()
