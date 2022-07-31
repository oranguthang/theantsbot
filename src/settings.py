import copy
import json

with open("settings_base.json", "r") as file_base:
    SETTINGS_BASE = json.loads(file_base.read())


class Settings:
    @staticmethod
    def load_settings():
        with open("settings.json", "r") as file:
            settings = json.loads(file.read())
            settings_base = copy.deepcopy(SETTINGS_BASE)
            settings_base.update(settings)
            return settings_base

    @staticmethod
    def check_enabled(settings):
        if not settings:
            settings = Settings.load_settings()

        return settings["enabled"]
