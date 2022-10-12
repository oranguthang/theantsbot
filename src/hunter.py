import itertools
import re
from time import sleep

from src.base import TheAntsBot, SLEEP_SHORT, SLEEP_MEDIUM
from src.exceptions import AllUnitsAreBusy, NoMarchUnitScreen
from src.logger import logger
from src.settings import Settings
from src.utils import Colors, THRESHOLD_DIVIDER


class HuntingBot(TheAntsBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_finished = False
        self.is_first_run = True

    def press_search_minus_button(self, settings, sleep_duration=None):
        self.press_position(settings, "searchMinusLevelButton", sleep_duration)

    def press_search_plus_button(self, settings, sleep_duration=None):
        self.press_position(settings, "searchPlusLevelButton", sleep_duration)

    def press_search_screen_first_icon(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "huntGatherScreenFirstIcon", sleep_duration)

    def press_search_screen_second_icon(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "huntGatherScreenSecondIcon", sleep_duration)

    def press_search_screen_third_icon(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "huntGatherScreenThirdIcon", sleep_duration)

    def press_attack_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "attackButton", sleep_duration)

    def swipe_back_search_screen(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.swipe(settings, "swipeBackHuntGatherScreen", duration_ms=1000)
        sleep(settings[sleep_duration])

    def swipe_search_screen(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.swipe(settings, "swipeHuntGatherScreen", duration_ms=1000)
        sleep(settings[sleep_duration])

    def recall_march_units(self, settings):
        # Not working
        march_units_actions = self.get_text_boxes_from_screenshot(
            settings=settings, rectangle_name="marchUnitsDutiesBar",
            char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        )
        for x, y, action_text in march_units_actions:
            action_text = action_text.lower()
            if "back" in action_text.lower():
                self.press_location(
                    x / THRESHOLD_DIVIDER + settings["positions"]["allianceMembersBox"]["x"],
                    y / THRESHOLD_DIVIDER + settings["positions"]["allianceMembersBox"]["y"]
                )

    def set_wild_creature_or_resource_tile_type(self, settings, mode="hunt"):
        if mode == "gather":
            config_name = "farmGatheringConfig"
        else:
            config_name = "farmHuntingConfig"

        if settings.get("resourceType") is not None:
            config = settings
        else:
            config = settings[config_name][str(self.device.number)]

        for _ in range(3):
            self.swipe_back_search_screen(settings)

        # Set type of creature/tile
        if config["resourceType"] == "meat":
            self.press_search_screen_second_icon(settings)
        else:
            self.swipe_search_screen(settings)
            if config["resourceType"] == "leaf":
                self.press_search_screen_first_icon(settings)
            elif config["resourceType"] == "soil":
                self.press_search_screen_second_icon(settings)
            else:
                # Sand
                self.press_search_screen_third_icon(settings)

        # Set level of creature/tile
        if mode == "gather":
            for _ in range(14):
                self.press_search_minus_button(settings)
            for _ in range(config["level"] - 1):
                self.press_search_plus_button(settings)
        else:
            for _ in range(14):
                self.press_search_plus_button(settings)
            for _ in range(15 - config["level"]):
                self.press_search_minus_button(settings)

    def analyze_march_unit(self, is_swiped=False, is_marching_before_swipe=False, mode="hunt"):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        image = self.get_screenshot(settings, rectangle_name="marchUnitsHeading")
        text = self.get_text_from_screenshot(image=image, settings=settings)
        logger.debug(f"Extracted text from march unit heading: {text}")

        if "March" not in text and "Unit" not in text:
            heading_is_gray = self.check_pixel_color(
                image, settings, "marchUnitsHeadingColorPick", Colors.GRAY
            )
            if heading_is_gray:
                # If we stuck in the march unit screen, and it's blurred
                self.press_back_button(settings)
                self.press_back_button(settings)

            logger.error("Something is wrong, couldn't select a march unit!")
            raise NoMarchUnitScreen

        # Get only part of image which contains stamina
        text = self.get_text_from_screenshot(settings=settings, rectangle_name="marchUnitsStamina",
                                             char_whitelist="0123456789/")
        logger.debug(f"Extracted text: {text}")

        stamina_values = re.findall(r"(\d{1,3}/100)", text)
        stamina_text = ",".join(stamina_values)
        logger.debug(f"Stamina values: {stamina_text}")

        found = False
        number = 0
        is_marching = False
        min_stamina = settings["minStamina"] if mode == "hunt" else 10
        for stamina in stamina_values:
            number += 1
            stamina_value = list(map(int, stamina.split("/")))[0]
            if stamina_value > 100:
                logger.warning(f"Stamina value {stamina_value} is more than 100, get last two digits")
                stamina_value %= 100
            if stamina_value >= min_stamina:
                self.press_location(
                    settings["positions"]["centerScreen"]["x"],
                    settings["marchScreenTopBarHeight"]
                    + settings["marchUnitHeight"] * number
                    - settings["marchUnitHeight"] / 3
                )
                sleep(settings[SLEEP_SHORT])

                image = self.get_screenshot(settings)
                button_is_gray = self.check_pixel_color(
                    image, settings, "marchButtonColorPick", Colors.GRAY
                )
                if not button_is_gray:
                    found = True
                    break
                else:
                    is_marching = True

        if found:
            logger.info(f"Found a unit, go!")
            self.press_march_button(settings)
        else:
            if is_swiped:
                if is_marching:
                    self.press_back_button(settings)
                    raise AllUnitsAreBusy
                else:
                    self.press_back_button(settings)
                    if not is_marching_before_swipe:
                        # If we don't have marching units before swipe too, the stamina is exceeded
                        self.is_finished = True
                        logger.info(f"The hunt on {self.device.name} is finished!")
            else:
                self.swipe(settings, "swipeMarchScreen", duration_ms=500)
                sleep(settings[SLEEP_SHORT])
                self.analyze_march_unit(is_swiped=True, is_marching_before_swipe=is_marching, mode=mode)

    def do_hunt(self):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        if self.is_first_run:
            self.is_first_run = False
            self.press_world_button(settings)
            # TODO: Fix with button image recognition
            # self.recall_march_units(settings)
            self.press_search_button(settings)
            self.press_search_wild_creatures_button(settings)
            self.set_wild_creature_or_resource_tile_type(settings)
            self.press_back_button(settings)

        text = self.get_text_from_screenshot(settings=settings, rectangle_name="marchUnitsCount",
                                             char_whitelist="0123456789/")
        logger.debug(f"Extracted text from march units count: {text}")

        march_units_value = re.findall(r"(\d/\d)", text)
        if march_units_value:
            march_units_value = march_units_value[0]
            units_busy, units_total = map(int, march_units_value.split("/"))
            if units_busy >= units_total:
                logger.info("All units are busy, return")
                raise AllUnitsAreBusy
        else:
            logger.warning("Something is wrong, couldn't find march units count!")

        sleep(settings[SLEEP_SHORT])
        try:
            self.press_search_button(settings)
            self.press_search_go_button(settings)
            self.press_center_screen(settings)
            self.press_attack_button(settings)
            # no need to pass settings, because this function reloads it
            self.analyze_march_unit()
        except NoMarchUnitScreen:
            # if we got an error or creature is missing, trying to run the loop again
            return

    def run(self, shared):
        self.do_hunt()

    @staticmethod
    def run_bots(bots, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        logger.info(f"Ready to run the hunting bot on {', '.join(bot.device.name for bot in bots)}")

        for bot in itertools.cycle(bots):
            if bot.is_finished:
                continue

            try:
                while True:
                    if bot.is_finished:
                        # When the hunt is finished, return to anthill
                        bot.press_world_button(settings)
                        break
                    bot.do_hunt()

            except AllUnitsAreBusy:
                sleep(settings[SLEEP_MEDIUM] * 5)
                continue

            if all([bot.is_finished for bot in bots]):
                break
