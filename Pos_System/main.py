from Repositories.UserRepository import UserRepository

from Pos_System.Services.BranchService import BranchService
from Pos_System.Services.SalesService import SaleService
from Pos_System.Services.ProductListService import ProductsService

from Utills.DB_Connection import init_db


def main():
    init_db()

    user_repo = UserRepository()
    branch_repo = BranchService()
    sale_repo = SaleService()
    product_repo = ProductsService()

    print("---------------------------------------------")
    print("         Sampath Food City (PVT) Ltd         ")
    print("---------------------------------------------")

    print("Please Enter Username and Password to continue:")

    looping = 0

    while looping != 1:
        userName = input("Enter Username >>")
        password = input("Enter Password >>")

        user = user_repo.getUser(userName)

        if user and password == user[0][2]:
            print("Login Success!")
            print("---------------------------------------------")
            print("\n")

            print("*** Welcome To Sampath POS System ***")
            looping = 1;
        else:
            print("Invalid Password or User, Try Again!")

    choice = 0
    while choice != 99:
        print("\n")
        print("1) View all Branches")
        print("2) Add New Branch")
        print("3) View all Products")
        print("4) Change Product price")
        print("5) Add a Sale")
        print("6) Date wise Sales Analyse for each Branch")
        print("7) Analyse Product Sales")
        print("8) Analyse Sales of whole market")
        print("9) Trending Product Research")
        print("10) Top Product Selling Branch Research")
        print("99) Exit")
        choice = int(input())

        if choice == 1:
            branch_repo.getAllBranches()

        elif choice == 2:
            branch_repo.add_branch()

        elif choice == 3:
            product_repo.get_all_Products()

        elif choice == 4:
            product_repo.price_update()

        elif choice == 5:
            sale_repo.save_Sale()

        elif choice == 6:
            sale_repo.date_wise_sales_analyse()

        elif choice == 7:
            product_repo.product_sale_analyse()

        elif choice == 8:
            sale_repo.sale_analyse_whole_market_network()

        elif choice == 9:
            product_repo.trending_products_research()

        elif choice == 10:
            product_repo.top_product_selling_branch_research()

        elif choice == 99:
            print("Good Bye !!")
            print("---------------------------------------------")


if __name__ == "__main__":
    main()
