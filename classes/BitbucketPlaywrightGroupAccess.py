from playwright.sync_api import Page
from utils import pretty_print


class BitbucketPlaywrightGroupAccess:
    def __init__(self, page: Page, workspace: str, repo_name: str):
        self.page = page
        self.workspace = workspace
        self.repo_name = repo_name
        self.start()

    def start(self):
        self.page.goto(
            f"https://bitbucket.org/{self.workspace}/{self.repo_name}/admin/permissions"
        )
        self.page.wait_for_load_state("networkidle")
        self._add_group()

    def _add_group(self):
        self.page.click('button:has-text("Add users or groups")')
        self.page.wait_for_selector('[role="dialog"]', state="visible")

        self._select_write_permission()
        pretty_print("Write selected. Fill in the group and click Confirm in the browser.")
        input("Press Enter to close browser...")

    def _select_write_permission(self):
        trigger = self.page.locator(
            '[data-testid="modal-dialog--body"] [data-testid="privilegesDropdown--trigger"]'
        )
        trigger.click()
        self.page.wait_for_selector(
            '[data-testid="modal-dialog--body"] [data-testid="privilegesDropdown--trigger"][aria-expanded="true"]'
        )
        self.page.locator('button[role="menuitem"]').filter(
            has=self.page.locator('span[data-item-title="true"]', has_text="Write")
        ).click()
