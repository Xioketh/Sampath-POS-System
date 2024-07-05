import sqlite3
from datetime import date


def getProductHistoryByProductID(proID):
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productActivity WHERE productId = ?', (proID,))
    historyData = cursor.fetchall()
    conn.close()
    return historyData

def updateProductHistory(proID, newhistoryPriceChanges):
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE productActivity SET history = ?, updateDate = ? WHERE productId = ?', (newhistoryPriceChanges, date.today(), proID))
    conn.commit()
    conn.close()
def saveProductHistory(proID, newhistoryPriceChanges):
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('''
         INSERT INTO productActivity (productId, history, updateDate)
         VALUES (?, ?, ?)
     ''', (proID, newhistoryPriceChanges, date.today()))
    conn.commit()
    conn.close()