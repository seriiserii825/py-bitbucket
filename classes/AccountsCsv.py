import csv
import os
from typing import List

from execeptions.AccountException import AccountException
from my_types.account_type import AccountType


class AccountsCsv:
    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_DIR = os.path.dirname(self.ROOT_DIR)
        self.file_path = os.path.join(self.ROOT_DIR, 'accounts.csv')
        self.accounts: List[AccountType] = []

    def from_file_to_array(self):
        if not os.path.exists(self.file_path):
            raise AccountException(f"File {self.file_path} does not exist.")
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
        raise AccountException(f"Account with email {email} not found.")

    def print_account_values_by_email(self, email):
        account = self.get_account_by_email(email)
        if account:
            print(f"Email: {account.email}")
            print(f"Workspace: {account.workspace}")
            print(f"Project Key: {account.project_key}")
            print(f"Username: {account.username}")
            print(f"App Password: {account.app_password}")
            print(f"Is Private: {account.is_private}")
        else:
            print("Account not found.")


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
