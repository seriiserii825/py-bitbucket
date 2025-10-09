import os


class Notification:
    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message

    @staticmethod
    def notify(title, message):
        os.system(f'notify-send "{title}" "{message}"')
