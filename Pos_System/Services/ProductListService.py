from datetime import datetime
from datetime import date

from ..Repositories.ProductsRepository import ProductsRepository
from ..Repositories.ProductActivityRepository import ProductActivityRepository
from ..Repositories.SaleProductsRepository import SaleProductsRepository

class ProductsService:
    def __init__(self):
        self.product_repository = ProductsRepository()
        self.product_activity_repository = ProductActivityRepository()
        self.sale_products_repository = SaleProductsRepository()
    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    def get_all_Products(self):
        print("----- All Products -----")
        products = self.product_repository.getAllProducts()
        for product in products:
            print("Id:", product[0], "/Product Name:", product[1], "/Product Qty:", product[2],
                  "/Product Price(Rs):", product[3])
        print("---------------------------------------------")

    def price_update(self):
        print("----- Update Product price -----")
        print("Active Product List")

        products = self.product_repository.getAllProducts()
        for product in products:
            print("Id:", product[0], "/Product Name:", product[1],
                  "/Product Price(Rs):", product[3])

        productId = int(input("Please Enter the ID of Product that need to Price change:"))
        selectedProduct = self.product_repository.findByProductId(productId)

        c = 0
        while c != 1:
            if selectedProduct:
                productHistory = self.product_activity_repository.getProductHistoryByProductID(productId);
                newPrice = input("Please Enter productId " + str(productId) + " New price>>")

                if productHistory:
                    oldHistoryPriceChanges = productHistory[0][2];
                    newhistoryPriceChanges = oldHistoryPriceChanges + "," + str(float(newPrice))
                    self.product_activity_repository.updateProductHistory(productId, newhistoryPriceChanges)
                    self.product_repository.updateProductPrice(productId, float(newPrice))
                else:
                    newhistoryPriceChanges = str(float(newPrice))
                    self.product_activity_repository.saveProductHistory(productId, newhistoryPriceChanges)
                    self.product_repository.updateProductPrice(productId, float(newPrice))

                c = 1
                print("Price Update Successfully!")

            else:
                print("Product not found, Try Again")

        print("---------------------------------------------")

    def product_sale_analyse(self):
        print("---------- Product Sales Analyse ----------")

        products = self.product_repository.getAllProducts()
        for product in products:
            print("Id:", product[0], "/Product Name:", product[1],
                  "/Product Price(Rs):", product[3])

        productId = int(input("Please Enter the ID of Product that need to Analyse Sales:"))
        selectedProduct = self.product_repository.findByProductId(productId)
        # print(selectedProduct)

        c = 0
        while c != 1:
            if selectedProduct:
                productHistory = self.product_activity_repository.getProductHistoryByProductID(productId);

                if productHistory:
                    # print(productHistory)
                    values = productHistory[0][2].split(',')
                    currentPrice = values[-1]
                    priceBeforeCurrentPrice = values[-2]

                    lastUpdateDate = productHistory[0][3]
                    # print(lastUpdateDate)

                    productSale = self.sale_products_repository.getSaleProductByProID(productId);

                    # print(productSale)

                    beforeSales = [];
                    currentPriceSales = [];

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
                            currentPriceSales.append(sale)
                            totalCurrentPriceSalesAmount += sale[2]
                            totalCurrentPriceSalesQty += sale[3]
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

                    print("Selected Item: ", selectedProduct[0][1])
                    print("Current Selling Price: Rs.", currentPrice)
                    print("Last Price Update Date: ", lastUpdateDate)
                    print("Previous Price: Rs.", priceBeforeCurrentPrice)
                    print("Current Price Total Sold Amount: Rs.", totalCurrentPriceSalesAmount)
                    print("Current Price Total Sold Qty: ", totalCurrentPriceSalesQty)
                    print("Previous Price Total Sold Amount: Rs.", totalBeforePriceSalesAmount)
                    print("Previous Price Total Sold Qty: ", totalBeforePriceSalesQty)
                    if (len(beforeSales) > 0):
                        print(lastUpdateDate, "-", date.today(),
                              " Product Qty Sold Percentage Relevent to Previous Price: ",
                              (totalCurrentPriceSalesQty / totalBeforePriceSalesQty) * 100)

                c = 1

            else:
                print("Product not found, Try Again")

        print("---------------------------------------------")

    def trending_products_research(self):
        print("---------- Trending Product Research ----------")

        trendProduct = self.sale_products_repository.getAllTimeTrendProduct();
        print("All Time Trending Product: ", trendProduct[0][0], ", Total Sales Count: ", trendProduct[0][2])
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

                if not (self.validate_date(from_date) and self.validate_date(to_date)):
                    print("One or both dates are invalid. Please enter the dates in yyyy-mm-dd format.")
                else:
                    c = 0;

            result = self.sale_products_repository.getTrendProductFromDateRange(from_date, to_date)

            if result != None:
                print("Selected Date Range Trending Product: ", result[0], ", Total Sales Count: ", result[2])
            else:
                print("No Trend Product For Selected Date Range")

        print("---------------------------------------------")

    def top_product_selling_branch_research(self):
        print("---------- Top Product Selling Branch Research ----------")

        trendProduct = self.sale_products_repository.getAllTimeTrendProduct();
        print("All Time Trending Product Selling Branch is: ", trendProduct[0][1])
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

                if not (self.validate_date(from_date) and self.validate_date(to_date)):
                    print("One or both dates are invalid. Please enter the dates in yyyy-mm-dd format.")
                else:
                    c = 0;

            result = self.sale_products_repository.getTrendProductFromDateRange(from_date, to_date)

            if result != None:
                print("Selected Date Range Trending Product Selling Branch: ", result[1])
            else:
                print("No Trend Branch For Selected Date Range")

        print("---------------------------------------------")