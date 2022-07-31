from time import sleep

from src.base import SLEEP_SHORT, SLEEP_LONG
from src.exceptions import NoMarchUnitScreen, AllUnitsAreBusy
from src.hunter import HuntingBot
from src.logger import logger
from src.settings import Settings


class GatheringBot(HuntingBot):
    def press_gather_resource_tile_icon(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "gatherResourceTileIcon", sleep_duration)

    def check_units_returned(self, settings):
        # Not working
        march_units_actions = self.get_text_boxes_from_screenshot(
            settings=settings, rectangle_name="marchUnitsDutiesBar",
            char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        )
        is_all_units_returned = True
        for x, y, action_text in march_units_actions:
            action_text = action_text.lower()
            if "back" in action_text or "speed" in action_text:
                is_all_units_returned = False
                break
        return is_all_units_returned

    def check_resource_count(self, settings):
        resources_count = self.get_text_boxes_from_screenshot(
            settings=settings, rectangle_name="resourceTileDataWindow",
            char_whitelist="0123456789"
        )
        for _, _, count in resources_count:
            try:
                if int(count) >= settings["resourceTileMinAmount"]:
                    return True
            except ValueError:
                continue
        return False

    def do_gather(self):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.press_world_button(settings)
        self.recall_march_units(settings)

        # Wait for all units to finish
        while True:
            is_all_units_returned = self.check_units_returned(settings)
            if is_all_units_returned:
                break
            else:
                sleep(settings[SLEEP_LONG])

        self.press_search_button(settings)
        self.press_search_resource_tiles_button(settings)
        self.set_wild_creature_or_resource_tile_type(settings, mode="gather")
        self.press_back_button(settings)

        # Loop through all units
        trials = 0
        while True:
            if trials > settings["trialsToFindResourceTile"]:
                logger.error("Something is wrong, couldn't find a resource tile!")
                break

            trials += 1
            # lock.acquire()

            self.press_search_button(settings)
            self.press_search_go_button(settings)
            self.press_center_screen(settings)

            is_enough_resources = self.check_resource_count(settings)
            if not is_enough_resources:
                # lock.release()
                continue

            self.press_gather_resource_tile_icon(settings)

            try:
                self.analyze_march_unit(settings, mode="gather")
            except NoMarchUnitScreen:
                continue
            except AllUnitsAreBusy:
                break
            finally:
                # lock.release()
                pass

        self.press_world_button(settings)

    def run(self):
        logger.info(f"Ready to run the gathering bot on {self.device.name}")

        self.do_gather()
