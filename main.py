import sqlite3
from datetime import date
from bs4 import BeautifulSoup
from fpdf import FPDF
from datetime import datetime

from Repositories import branch as branchDB
from Repositories import products as productsDB
from Repositories import sales as salesDB
from Repositories import saleProducts as saleProductDB
from Repositories import user as userDB
from Repositories import productActivity as productActivityDB


def init_db():
    conn = sqlite3.connect('SampathPOS.db')
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

def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def main():
    init_db()
    print("---------------------------------------------")
    print("         Sampath Food City (PVT) Ltd         ")
    print("---------------------------------------------")

    print("Please Enter Username and Password to continue:")

    looping = 0

    while looping !=1:
        username = input("Enter Username >>")
        password = input("Enter Password >>")

        user = userDB.getUser(username)

        if user and password == user[0][2]:
            print("Login Success!")
            print("---------------------------------------------")
            print("\n")

            print("*** Welcome To Sampath POS System ***")
            looping =1;
        else:
            print("Invalid Password or User, Try Again!")


    choice = 0
    while choice != 99:
        print("\n")
        print("1) Add New Branch")
        print("2) All Branches")
        print("3) Add Sale")
        print("4) All Products")
        print("5) Date wise sales Analyse for each branch")
        print("6) Product Price change")
        print("7) Product Sales Analyse")
        print("8) Sale Analyse for whole Market Network")
        print("9) Trending Product Research")
        print("10) Top Product Selling Branch Research")
        print("99) Exit")
        choice = int(input())

        if choice == 1:
            print("Adding a Branch...")
            nBranch = input("Enter the Branch Name >>>")
            nLocation = input("Enter the Branch Location >>>")
            branchDB.add_brach_to_db(nBranch, nLocation)
            print("Branch Saved Success!")
            print("---------------------------------------------")


        elif choice == 2:
            print("All Branchs...")
            branches = branchDB.getAll()
            for branch in branches:
                print(branch[0], " - ", branch[2])
            print("---------------------------------------------")

        elif choice == 3:
            print("Adding Sale...")
            product_data = []
            count = int(input("How many Products?"))
            c = 0
            totalQty = 0;
            totalSaleAmount = 0.0
            branch = ""
            while c != count:
                product_id = input("Enter Product ID >>>")

                product = productsDB.findByProductId(product_id)
                if product:
                    lastSaleId = salesDB.getLatestId();
                    # print(lastSaleId)

                    if lastSaleId == 0:
                        lastSaleId = 1;
                        # print(lastSaleId)
                    else:
                        lastSaleId += 1;
                        # print(lastSaleId)

                    availableQuantity = product[0][2]
                    print("Available Qty: ", availableQuantity)
                    sale_qty = int(input("How many Qty for this Sale >>> "))

                    sale_total_amount = float(sale_qty) * product[0][3]

                    totalQty += sale_qty;
                    totalSaleAmount += sale_total_amount

                    saleProductDB.add_Sale_products(lastSaleId, sale_qty, sale_total_amount, product_id, product[0][3])

                    print(sale_total_amount)
                    c += 1

                else:
                    print("Product not found, Try Again")

                product_data.append(product)

            getLocationCount = 0;
            branches = branchDB.getAll();

            for branch in branches:
                print(branch[0], " - ", branch[2])

            while getLocationCount != 2:
                n_location = input("Enter the Branch Location >>>")

                branch = branchDB.search_branch_in_db(n_location);

                if branch:
                    getLocationCount = 2;
                    # print("Branch found")
                    # print(branch[0][2])
                else:
                    print("Branch not found, Try again")
            salesDB.addSale(totalQty, totalSaleAmount, date.today(), branch[0][2])
            print("Sale Saved!")
            print("---------------------------------------------")

        elif choice == 4:
            print("All Products")
            products = productsDB.getAllProducts()
            for product in products:
                print("Id:", product[0], "/Product Name:", product[1], "/Product Qty:", product[2],
                      "/Product Price(Rs):", product[3])
            print("---------------------------------------------")

        elif choice == 5:
            print("Select Branch to Analyse Date wise Sales")
            branches = branchDB.getAll();

            for branch in branches:
                print(branch[0], " - ", branch[2])

            n_location = "";
            getLocationCount = 0;
            while getLocationCount != 2:
                n_location = input("Enter the Branch >>>")

                branch = branchDB.search_branch_in_db(n_location);

                if branch:
                    getLocationCount = 2;
                    # print("Branch found")
                    # print(branch[0][2])

                    print("Please Provide Date Range yyyy-mm-dd")
                    c = 0;
                    from_date =""
                    to_date =""
                    while c == 0:
                        from_date = input("From >")
                        to_date = input("To >")

                        if not (validate_date(from_date) and validate_date(to_date)):
                            print("One or both dates are invalid. Please enter the dates in yyyy-mm-dd format.")
                        else:
                            c =1;

                    # from_date = "2023-09-09";
                    # to_date = "2024-09-09";
                    result = salesDB.getSaleFromDateRangeAndBranchWise(branch[0][2], from_date, to_date)
                    print("Total Amount: ", result[1], " Total Sold Qty: ", result[0])

                    isReportDownload = input("Do you want to Download report PDF ? (y/n)")

                    if isReportDownload == "y":
                        html_content = f"""
                                                <html>
                                                <body>
                                                <h1><u>Sales Report</u></h1>
                                                <p>Branch: {branch[0][2]}</p>
                                                <p>From Date: {from_date}   To Date: {to_date}</p>
                                                <br><br>
                                                <p>Total Amount: {result[1]}</p>
                                                <p>Total Sold Qty: {result[0]}</p>
                                                </body>
                                                </html>
                                                """

                        # Parse HTML content
                        soup = BeautifulSoup(html_content, 'html.parser')

                        # Create PDF with A5 size
                        pdf = FPDF(format='A5')
                        pdf.add_page()
                        pdf.set_font("Arial", size=12)

                        for element in soup.stripped_strings:
                            pdf.cell(200, 10, txt=element, ln=True)

                        # Generate file path
                        pdf_file_path = f"Sale Reports/{branch[0][2]}_sales_report_{from_date} to {to_date}.pdf"
                        pdf.output(pdf_file_path)

                        print(f"PDF Saved to {pdf_file_path}")

                else:
                    print("Branch not found, Try again")
            print("---------------------------------------------")

        elif choice == 6:
            print("Active Product List")

            products = productsDB.getAllProducts()
            for product in products:
                print("Id:", product[0], "/Product Name:", product[1],
                      "/Product Price(Rs):", product[3])

            productId = int(input("Please Enter the ID of Product that need to Price change:"))
            selectedProduct = productsDB.findByProductId(productId)

            c = 0
            while c != 1:
                if selectedProduct:
                    productHistory = productActivityDB.getProductHistoryByProductID(productId);
                    newPrice = input("Please Enter productId " + str(productId) + " New price>>")

                    if productHistory:
                        oldHistoryPriceChanges = productHistory[0][2];
                        newhistoryPriceChanges = oldHistoryPriceChanges + "," + str(float(newPrice))
                        productActivityDB.updateProductHistory(productId, newhistoryPriceChanges)
                        productsDB.updateProductPrice(productId, float(newPrice))
                    else:
                        newhistoryPriceChanges = str(float(newPrice))
                        productActivityDB.saveProductHistory(productId, newhistoryPriceChanges)
                        productsDB.updateProductPrice(productId, float(newPrice))

                    c = 1
                    print("Price Update Successfully!")

                else:
                    print("Product not found, Try Again")

            print("---------------------------------------------")

        elif choice == 7:
            print("Product Sales Analyse")

            products = productsDB.getAllProducts()
            for product in products:
                print("Id:", product[0], "/Product Name:", product[1],
                      "/Product Price(Rs):", product[3])

            productId = int(input("Please Enter the ID of Product that need to Analyse Sales:"))
            selectedProduct = productsDB.findByProductId(productId)
            # print(selectedProduct)

            c = 0
            while c != 1:
                if selectedProduct:
                    productHistory = productActivityDB.getProductHistoryByProductID(productId);


                    if productHistory:
                        # print(productHistory)
                        values = productHistory[0][2].split(',')
                        currentPrice = values[-1]
                        priceBeforeCurrentPrice = values[-2]

                        # print(currentPrice)
                        # print(priceBeforeCurrentPrice)

                        lastUpdateDate = productHistory[0][3]
                        # print(lastUpdateDate)

                        productSale = saleProductDB.getSaleProductByProID(productId);

                        # print(productSale)


                        beforeSales =[];
                        currentPriceSales =[];

                        date_format = "%Y-%m-%d"

                        totalCurrentPriceSalesAmount = 0;
                        totalCurrentPriceSalesQty = 0;

                        totalBeforePriceSalesAmount = 0;
                        totalBeforePriceSalesQty = 0;

                        for sale in productSale:
                            date1 = datetime.strptime(sale[4], date_format)
                            date2 = datetime.strptime(lastUpdateDate, date_format)
                            # print(sale)
                            # print(sale[6])
                            if date1 >= date2:
                                # print("true part!!")
                                currentPriceSales.append(sale)
                                totalCurrentPriceSalesAmount +=sale[2]
                                totalCurrentPriceSalesQty +=sale[3]
                            elif float(sale[6]) == float(priceBeforeCurrentPrice):
                                # print("in else part!!!")
                                totalBeforePriceSalesAmount += sale[2]
                                totalBeforePriceSalesQty += sale[3]
                                beforeSales.append(sale)

                        # print("currentPriceSales:::")
                        # print(currentPriceSales)
                        #
                        # print("before sales::")
                        # print(beforeSales)

                        print("\n")
                        print("<<<< Analyse Results >>>>")

                        print("Selected Item: ",selectedProduct[0][1])
                        print("Current Selling Price: Rs.",currentPrice)
                        print("Last Price Update Date: ",lastUpdateDate)
                        print("Previous Price: Rs.",priceBeforeCurrentPrice)
                        print("Current Price Total Sold Amount: Rs.",totalCurrentPriceSalesAmount)
                        print("Current Price Total Sold Qty: ",totalCurrentPriceSalesQty)
                        print("Previous Price Total Sold Amount: Rs.",totalBeforePriceSalesAmount)
                        print("Previous Price Total Sold Qty: ",totalBeforePriceSalesQty)
                        if(len(beforeSales)>0):
                            print(lastUpdateDate, "-", date.today(),
                                  " Product Qty Sold Percentage Relevent to Previous Price: ",
                                  (totalCurrentPriceSalesQty / totalBeforePriceSalesQty) * 100)

                    c = 1

                else:
                    print("Product not found, Try Again")

            print("---------------------------------------------")

        elif choice == 8:
            print("Sale Analyse for whole Market Network")

            print("Please Provide Date Range yyyy-mm-dd")
            # from_date = input("From >")
            # to_date = input("To >")
            #
            # from_date = "2023-09-09";
            # to_date = "2024-09-09";
            from_date = ""
            to_date = ""
            c =1;
            while c == 1:
                from_date = input("From >")
                to_date = input("To >")

                if not (validate_date(from_date) and validate_date(to_date)):
                    print("One or both dates are invalid. Please enter the dates in yyyy-mm-dd format.")
                else:
                    c = 0;

            result = salesDB.getSaleFromDateRange(from_date, to_date)
            print("--Branch Wise--")
            sumQty =0
            sumTotAmount =0
            branch_data = ""

            for sale in result:
                sumQty +=sale[0]
                sumTotAmount +=sale[1]

                print("Branch:", sale[2], " Total Amount(Rs):", sale[1],
                      " Total Qty:", sale[0])

                branch_data += f"""
                        <p>Branch: {sale[2]} - Total Sold Qty: {sale[0]}, Total Amount (Rs): {sale[1]}</p>
                    """


            print("\n")
            print("Summery for Market, Total Amount(Rs)", sumTotAmount," Total Qty:",sumTotAmount)


            isReportDownload = input("Do you want to Download report PDF ? (y/n)")

            if isReportDownload == "y":
                html_content = f"""
                    <html>
                    <body>
                    <h1><u>Sales Report</u></h1>
                    <p>From Date: {from_date}   To Date: {to_date}</p>
                    <br><br>
                    {branch_data}
                    <br><br>
                    <p><b>Summary for Market</b></p>
                    <p>Total Sold Qty: {sumQty}</p>
                    <p>Total Amount (Rs): {sumTotAmount}</p>
                    </body>
                    </html>
                    """

                # Parse HTML content
                soup = BeautifulSoup(html_content, 'html.parser')

                # Create PDF with A5 size
                pdf = FPDF(format='A5')
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                for element in soup.stripped_strings:
                    pdf.cell(200, 10, txt=element, ln=True)

                # Generate file path
                pdf_file_path = f"Sale Reports/sales_report_{from_date} to {to_date}.pdf"
                pdf.output(pdf_file_path)

                print(f"PDF Saved to {pdf_file_path}")
            print("---------------------------------------------")

        elif choice == 9:
            print("Trending Product Research")

            trendProduct = saleProductDB.getAllTimeTrendProduct();
            print("All Time Trending Product: ",trendProduct[0][0],", Total Sales Count: ",trendProduct[0][2])
            # print(trendProduct)

            isReportDownload = input("Do you wish to filter Date wise Trending Product ? (y/n)")

            if isReportDownload == "y":
                print("Please Provide Date Range yyyy-mm-dd")
                # from_date = input("From >")
                # to_date = input("To >")
                #
                # from_date = "2023-09-09";
                # to_date = "2024-06-29";
                c = 1;
                from_date = ""
                to_date = ""
                while c == 1:
                    from_date = input("From >")
                    to_date = input("To >")

                    if not (validate_date(from_date) and validate_date(to_date)):
                        print("One or both dates are invalid. Please enter the dates in yyyy-mm-dd format.")
                    else:
                        c = 0;

                result = saleProductDB.getTrendProductFromDateRange(from_date, to_date)

                if result !=None:
                    print("Selected Date Range Trending Product: ", result[0], ", Total Sales Count: ",result[2])
                else:
                    print("No Trend Product For Selected Date Range")

            print("---------------------------------------------")

        elif choice == 10:
            print("Top Product Selling Branch Research")

            trendProduct = saleProductDB.getAllTimeTrendProduct();
            print("All Time Trending Product Selling Branch is: ",trendProduct[0][1])
            # print(trendProduct)

            isReportDownload = input("Do you wish to filter Date wise Trending Product Selling Branch ? (y/n)")

            if isReportDownload == "y":
                print("Please Provide Date Range yyyy-mm-dd")
                # from_date = input("From >")
                # to_date = input("To >")
                #
                # from_date = "2023-09-09";
                # to_date = "2024-06-29";
                c = 1;
                from_date = ""
                to_date = ""
                while c == 1:
                    from_date = input("From >")
                    to_date = input("To >")

                    if not (validate_date(from_date) and validate_date(to_date)):
                        print("One or both dates are invalid. Please enter the dates in yyyy-mm-dd format.")
                    else:
                        c = 0;

                result = saleProductDB.getTrendProductFromDateRange(from_date, to_date)

                if result !=None:
                    print("Selected Date Range Trending Product Selling Branch: ", result[1])
                else:
                    print("No Trend Branch For Selected Date Range")

            print("---------------------------------------------")
        elif choice == 99:
            print("Good Bye........")
            print("---------------------------------------------")


if __name__ == "__main__":
    main()
