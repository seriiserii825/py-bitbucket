import csv
import os
from typing import List

from execeptions.AccountException import AccountException
from my_types.account_type import AccountType
from utils import pretty_table, selectOne


class AccountsCsv:
    def __init__(self):
        """
        Initializes the AccountsCsv class,
        setting the root directory and file path for accounts.csv.
        """
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_DIR = os.path.dirname(self.ROOT_DIR)
        self.file_path = os.path.join(self.ROOT_DIR, 'accounts.csv')
        self.accounts: List[AccountType] = []

    def _from_file_to_array(self):
        """
        Reads the accounts.csv file
        and populates the accounts list with AccountType objects.
        Raises AccountException if the file does not exist.
        """
        if not os.path.exists(self.file_path):
            raise AccountException(f"File {self.file_path} does not exist.")
        rows = []
        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["is_private"] = row["is_private"].lower() == "true"
                account = AccountType(
                    email=row["email"],
                    workspace=row["workspace"],
                    project_key=row["project_key"],
                    username=row["username"],
                    app_password=row["app_password"],
                    is_private=row["is_private"],
                )
                rows.append(account)
        self.accounts = rows

    def get_account_by_email(self, email) -> AccountType:
        """
        Retrieves an account by email from the accounts.csv file.
        Raises AccountException if the account is not found.
        """
        if not self.accounts:
            self._from_file_to_array()
        for account in self.accounts:
            if account.email == email:
                return account
        raise AccountException(f"Account with email {email} not found.")

    def print_account_values_by_email(self, email):
        """
        Prints the values of an account by email from the accounts.csv file.
        """
        account = self.get_account_by_email(email)
        table_title = "Account Details"
        table_headers = ["Email", "Workspace", "Project Key",
                         "Username", "App Password", "Is Private"]
        table_rows = [
            account.email,
            account.workspace,
            account.project_key,
            account.username,
            account.app_password,
            str(account.is_private)
        ]
        if account:
            pretty_table(table_title, table_headers, [table_rows])
        else:
            print("Account not found.")

    def _get_all_emails(self) -> List[str]:
        """
        Retrieves all emails from the accounts.csv file.
        """
        if not self.accounts:
            self._from_file_to_array()
        return [account.email for account in self.accounts]

    def choose_account_by_email(self) -> AccountType:
        """
        Prompts the user to select an email from the accounts.csv file
        """
        if not self.accounts:
            self._from_file_to_array()
        emails = self._get_all_emails()
        if not emails:
            raise AccountException("No accounts found in the CSV file.")
        selected_email = selectOne(emails)
        return self.get_account_by_email(selected_email)
