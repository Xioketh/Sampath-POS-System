import sqlite3

class SalesRepository:
    def getLatestId(self):
        conn = sqlite3.connect('SampathPOS.db')
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(id) AS last_id FROM sales')
        result = cursor.fetchone()
        conn.close()
        last_id = result[0] if result[0] is not None else 0
        return last_id

    def addSale(self,totalQty, totalAmount, saleDate, branchName):
        conn = sqlite3.connect('SampathPOS.db')
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO sales (totalQty, totalAmount, saleDate, branchName)
                VALUES (?, ?, ?, ?)
            ''', (totalQty, totalAmount, saleDate, branchName))
        conn.commit()
        conn.close()

    def getSaleFromDateRangeAndBranchWise(self,branchName, from_date, to_date):
        conn = sqlite3.connect('SampathPOS.db')
        cursor = conn.cursor()
        cursor.execute('''
                   SELECT SUM(totalQty), SUM(totalAmount)
                   FROM sales
                   WHERE saleDate BETWEEN ? AND ?
                   AND branchName = ?;
               ''', (from_date, to_date, branchName))
        result = cursor.fetchone()
        conn.close()
        return result

    def getSaleFromDateRange(self,from_date, to_date):
        conn = sqlite3.connect('SampathPOS.db')
        cursor = conn.cursor()
        cursor.execute('''
                   SELECT SUM(totalQty), SUM(totalAmount) , branchName 
                   FROM sales
                   WHERE saleDate BETWEEN ? AND ? group by branchName;
               ''', (from_date, to_date))
        result = cursor.fetchall()
        conn.close()
        return result

