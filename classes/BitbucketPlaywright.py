import os
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page

SESSION_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "session.json"
)


class BitbucketPlaywright:
    def __init__(self):
        self._playwright: Playwright = sync_playwright().start()
        self.browser: Browser = self._playwright.chromium.launch(headless=False)
        self.context: BrowserContext = self._make_context()
        self.page: Page = self.context.new_page()

    def _make_context(self) -> BrowserContext:
        if os.path.exists(SESSION_PATH):
            return self.browser.new_context(storage_state=SESSION_PATH)
        return self.browser.new_context()

    def ensure_logged_in(self):
        self.page.goto("https://bitbucket.org/dashboard/overview")
        if "id.atlassian.com" in self.page.url or "signin" in self.page.url:
            print("Please log in to Bitbucket in the browser, then press Enter here...")
            input()
            self._save_session()
            print("Session saved to session.json")

    def _save_session(self):
        self.context.storage_state(path=SESSION_PATH)

    def close(self):
        self._save_session()
        self.browser.close()
        self._playwright.stop()
