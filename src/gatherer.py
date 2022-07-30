from src.base import TheAntsBot
from src.logger import logger
from src.settings import Settings


class GatheringBot(TheAntsBot):
    def do_gather(self):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.press_world_button(settings)
        # TODO: Wait for all units to finish
        self.press_search_button(settings)
        self.press_search_resource_tiles_button(settings)
        # TODO: Check resource tile type and level
        self.press_back_button(settings)

        # TODO: Loop through all units
        # TODO: Critical section
        self.press_search_button(settings)
        self.press_search_go_button(settings)
        self.press_center_screen(settings)
        # TODO: Analyze total amount of resources
        # TODO: self.press_gathering_icon(settings)
        self.press_march_button(settings)

    def run(self):
        logger.info(f"Ready to run the gathering bot on {self.device.name}")

        self.do_gather()
