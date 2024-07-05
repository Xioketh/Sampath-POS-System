import sqlite3

def getAllProducts():
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productList')
    products = cursor.fetchall()
    conn.close()
    return products

def findByProductId(productId):
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productList WHERE id = ?', (productId,))
    product = cursor.fetchall()
    conn.close()
    return product


def updateProductPrice(proID, newPrice):
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE productList SET price = ? WHERE id = ?', (newPrice, proID))
    conn.commit()
    conn.close()


