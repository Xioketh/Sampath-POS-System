from ..Repositories.BranchRepository import BranchRepository

class BranchService:
    def __init__(self):
        self.branch_repository = BranchRepository()
    def add_branch(self):
        print("Adding a Branch...")
        nBranch = input("Enter the Branch Name >>>")
        nLocation = input("Enter the Branch Location >>>")
        self.branch_repository.add_branch(nBranch, nLocation)
        print("Branch Saved Success!")
        print("---------------------------------------------")

    def getAllBranches(self):
        print("All Branchs...")
        branches = self.branch_repository.get_all()
        for branch in branches:
            print(branch[0], " - ", branch[2])
        print("---------------------------------------------")