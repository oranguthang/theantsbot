import json


class Settings:
    @staticmethod
    def load_settings(path="settings.json"):
        with open(path, "r") as file:
            settings = json.loads(file.read())
            return settings

    @staticmethod
    def check_enabled(settings):
        if not settings:
            settings = Settings.load_settings()

        return settings["enabled"]
