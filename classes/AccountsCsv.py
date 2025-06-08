import csv
import os
from typing import List

from my_types.account_type import AccountType


class AccountsCsv:
    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_DIR = os.path.dirname(self.ROOT_DIR)
        self.file_path = os.path.join(self.ROOT_DIR, 'accounts.csv')
        self.accounts: List[AccountType] = []

    def from_file_to_array(self):
        rows = []
        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["is_private"] = row["is_private"].lower() == "true"
                rows.append(row)
        self.accounts = rows

    def get_account_by_email(self, email):
        if not self.accounts:
            self.from_file_to_array()
        for account in self.accounts:
            if account.email == email:
                return account
        return None


#
#
# def getRepoData(ROOT_DIR):
#     filename = f"{ROOT_DIR}/accounts.csv"
#     rows = []
#     with open(filename, newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             row["is_private"] = row["is_private"].lower() == "true"
#             rows.append(row)
#     return rows
