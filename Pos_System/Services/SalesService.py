from datetime import datetime
from datetime import date

from bs4 import BeautifulSoup
from fpdf import FPDF

from ..Repositories.SalesRepository import SalesRepository
from ..Repositories.BranchRepository import BranchRepository
from ..Repositories.ProductsRepository import ProductsRepository
from ..Repositories.SaleProductsRepository import SaleProductsRepository

class SaleService:
    def __init__(self):
        self.product_repository = ProductsRepository()
        self.sales_repository = SalesRepository()
        self.sale_products_repository = SaleProductsRepository()
        self.branch_repository = BranchRepository()
    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    def date_wise_sales_analyse(self):
        print("----- Date wise Sales Analyse ----------")
        print("Select Branch to Analyse Date wise Sales")
        branches = self.branch_repository.get_all();

        for branch in branches:
            print(branch[0], " - ", branch[2])

        n_location = "";
        getLocationCount = 0;
        while getLocationCount != 2:
            n_location = input("Enter the Branch >>>")

            branch = self.branch_repository.search_branch(n_location);

            if branch:
                getLocationCount = 2;
                # print("Branch found")
                # print(branch[0][2])

                print("Please Provide Date Range yyyy-mm-dd")
                c = 0;
                from_date = ""
                to_date = ""
                while c == 0:
                    from_date = input("From >")
                    to_date = input("To >")

                    if not (self.validate_date(from_date) and self.validate_date(to_date)):
                        print("One or both dates are invalid. Please enter the dates in yyyy-mm-dd format.")
                    else:
                        c = 1;

                # from_date = "2023-09-09";
                # to_date = "2024-09-09";
                result = self.sales_repository.getSaleFromDateRangeAndBranchWise(branch[0][2], from_date, to_date)
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

    def save_Sale(self):
        print("----- Save Sale -----")
        product_data = []
        count = int(input("How many Products?"))
        c = 0
        totalQty = 0;
        totalSaleAmount = 0.0
        branch = ""
        while c != count:
            product_id = input("Enter Product ID >>>")

            product = self.product_repository.findByProductId(product_id)
            if product:
                lastSaleId = self.sales_repository.getLatestId();
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

                self.sale_products_repository.add_Sale_products(lastSaleId, sale_qty, sale_total_amount, product_id, product[0][3])

                print(sale_total_amount)
                c += 1

            else:
                print("Product not found, Try Again")

            product_data.append(product)

        getLocationCount = 0;
        branches = self.branch_repository.get_all();

        for branch in branches:
            print(branch[0], " - ", branch[2])

        while getLocationCount != 2:
            n_location = input("Enter the Branch Location >>>")

            branch = self.branch_repository.search_branch(n_location);

            if branch:
                getLocationCount = 2;
                # print("Branch found")
                # print(branch[0][2])
            else:
                print("Branch not found, Try again")
        self.sales_repository.addSale(totalQty, totalSaleAmount, date.today(), branch[0][2])
        print("Sale Saved!")
        print("---------------------------------------------")

    def getAllBranches(self):
        print("All Branchs...")
        branches = self.branch_repository.get_all()
        for branch in branches:
            print(branch[0], " - ", branch[2])
        print("---------------------------------------------")

    def sale_analyse_whole_market_network(self):
        print("---------- Sale Analyse for whole Market Network  ----------")

        print("Please Provide Date Range yyyy-mm-dd")
        # from_date = input("From >")
        # to_date = input("To >")
        #
        # from_date = "2023-09-09";
        # to_date = "2024-09-09";
        from_date = ""
        to_date = ""
        c = 1;
        while c == 1:
            from_date = input("From >")
            to_date = input("To >")

            if not (self.validate_date(from_date) and self.validate_date(to_date)):
                print("One or both dates are invalid. Please enter the dates in yyyy-mm-dd format.")
            else:
                c = 0;

        result = self.sales_repository.getSaleFromDateRange(from_date, to_date)
        print("--Branch Wise--")
        sumQty = 0
        sumTotAmount = 0
        branch_data = ""

        for sale in result:
            sumQty += sale[0]
            sumTotAmount += sale[1]

            print("Branch:", sale[2], " Total Amount(Rs):", sale[1],
                  " Total Qty:", sale[0])

            branch_data += f"""
                               <p>Branch: {sale[2]} - Total Sold Qty: {sale[0]}, Total Amount (Rs): {sale[1]}</p>
                           """

        print("\n")
        print("Summery for Market, Total Amount(Rs)", sumTotAmount, " Total Qty:", sumTotAmount)

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