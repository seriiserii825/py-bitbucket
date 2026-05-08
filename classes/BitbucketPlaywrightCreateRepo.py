from classes.Bitbucket import Bitbucket
from classes.BitbucketPlaywright import BitbucketPlaywright
from classes.BitbucketPlaywrightGroupAccess import BitbucketPlaywrightGroupAccess
from playwright.sync_api import Page
from utils import pretty_print, selectOne


class BitbucketPlaywrightCreateRepo:
    def __init__(self):
        self.start()

    def start(self):
        repo_name = self._set_repo_name()
        workspace = self._select_workspace()

        pw = BitbucketPlaywright()
        try:
            pw.ensure_logged_in()
            self._create_repo(pw.page, workspace, repo_name)
        finally:
            pw.close()

    def _set_repo_name(self) -> str:
        pretty_print("Set repo name")
        bb = Bitbucket()
        return bb.set_repo_name()

    def _select_workspace(self) -> str:
        pretty_print("Select workspace")
        bb = Bitbucket()
        return bb.select_workspace()

    def _create_repo(self, page: Page, workspace: str, repo_name: str):
        page.goto(f"https://bitbucket.org/{workspace}/workspace/create/repository")
        page.wait_for_load_state("networkidle")

        project = self._pick_project(page)
        if not project:
            return

        self._fill_repo_name(page, repo_name)

        page.click('button[type="submit"]')
        page.wait_for_url(f"**/{repo_name}/**", timeout=15000)
        pretty_print(f"Repository '{repo_name}' created successfully!")
        BitbucketPlaywrightGroupAccess(page, workspace, repo_name)

    def _fill_repo_name(self, page: Page, repo_name: str):
        page.fill("input#id_name", repo_name)
        pretty_print(f"Repo name set: {repo_name}")

    def _pick_project(self, page: Page) -> str | None:
        # открываем дропдаун и ждём пока появятся пункты
        page.click("#s2id_id_project a.select2-choice")
        page.wait_for_selector(
            "#select2-drop ul.select2-results li.select2-result", state="visible"
        )

        labels = page.query_selector_all(
            "#select2-drop ul li:not(.project-dropdown--create-trigger) .project-dropdown--label"
        )
        projects = [label.inner_text().strip() for label in labels]

        # закрываем перед терминальным меню (иначе дропдаун закроется сам при потере фокуса)
        page.keyboard.press("Escape")
        page.wait_for_selector("#select2-drop", state="hidden")

        if not projects:
            pretty_print("No projects found", error=True)
            return None

        pretty_print("Select a project:")
        selected = selectOne(projects)

        # открываем снова и кликаем нужный пункт
        page.click("#s2id_id_project a.select2-choice")
        page.wait_for_selector(
            "#select2-drop ul.select2-results li.select2-result", state="visible"
        )
        page.click(f'#select2-drop ul li .project-dropdown--label:text("{selected}")')

        pretty_print(f"Project selected: {selected}")
        return selected
