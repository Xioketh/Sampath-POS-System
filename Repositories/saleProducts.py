import sqlite3


def add_Sale_products(saleId, totalProductQty, totalProductAmount, product_id, unitPrice):
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO saleProducts (saleId, productId, totalQty, totalAmount, unitPrice)
        VALUES (?, ?, ?, ?, ?)
    ''', (saleId, product_id, totalProductQty, totalProductAmount, unitPrice))
    conn.commit()
    conn.close()


def getAllTimeTrendProduct():
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pl.name,s.branchName, COUNT(productId) as product_count
        FROM saleProducts
        join productList pl on saleProducts.productId = pl.id
        join sales s on saleProducts.saleId = s.id
        GROUP BY productId
        ORDER BY product_count DESC
        LIMIT 1;
    ''', ())
    tendProduct = cursor.fetchall()
    conn.close()
    return tendProduct


def getTrendProductFromDateRange(from_date, to_date):
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('''
                SELECT pl.name,s.branchName, COUNT(productId) as product_count
                FROM saleProducts
                join productList pl on saleProducts.productId = pl.id
                join sales s on saleProducts.saleId = s.id
                where s.saleDate BETWEEN ? AND ?
                GROUP BY productId
                ORDER BY product_count DESC
                LIMIT 1;
           ''', (from_date, to_date))
    result = cursor.fetchone()
    conn.close()
    return result


def getSaleProductByProID(productID):
    conn = sqlite3.connect('SampathPOS.db')
    cursor = conn.cursor()
    cursor.execute('''
                SELECT sp.productId, s.id, sp.totalAmount, sp.totalQty, s.saleDate, s.branchName, sp.unitPrice
                FROM saleProducts sp
                JOIN sales s ON sp.saleId = s.id
                WHERE sp.productId = ?;
           ''', (productID,))
    productSale = cursor.fetchall()
    conn.close()
    return productSale
