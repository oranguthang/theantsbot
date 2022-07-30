import itertools
import re
from time import sleep

from src.base import TheAntsBot, SLEEP_SHORT, SLEEP_MEDIUM
from src.exceptions import AllUnitsAreBusy, NoMarchUnitScreen
from src.logger import logger
from src.settings import Settings
from src.utils import ExtractText, ImageHandler


class HuntingBot(TheAntsBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_finished = False
        self.is_first_run = False

    def press_attack_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "attackButton", sleep_duration)

    def analyze_march_unit(self, is_swiped=False, is_marching_before_swipe=False):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        image = self.get_screenshot()
        march_unit_heading = ImageHandler.crop_image(
            image,
            settings["positions"]["marchUnitHeading"]["x"],
            settings["positions"]["marchUnitHeading"]["y"],
            settings["positions"]["marchUnitHeading"]["h"],
            settings["positions"]["marchUnitHeading"]["w"]
        )
        text = ExtractText.run(march_unit_heading)
        logger.debug(f"Extracted text from march unit heading: {text}")

        if "March" not in text and "Unit" not in text:
            heading_is_gray = ImageHandler.check_pixel_is_gray(
                image,
                settings["positions"]["marchUnitHeadingColorPick"]["x"],
                settings["positions"]["marchUnitHeadingColorPick"]["y"]
            )
            if heading_is_gray:
                # If we stuck in the march unit screen, and it's blurred
                self.press_back_button(settings)
                self.press_back_button(settings)

            logger.error("Something is wrong, couldn't select a march unit!")
            raise NoMarchUnitScreen

        # Get only part of image which contains stamina
        image_stamina = ImageHandler.crop_image(
            image,
            settings["screenWidth"] // 2,
            settings["positions"]["marchUnitHeading"]["y"],
            settings["screenHeight"],
            settings["screenWidth"] // 2,
        )

        image_threshold = ImageHandler.threshold(image_stamina)
        text = ExtractText.run(image_threshold, char_whitelist="0123456789/")
        logger.debug(f"Extracted text: {text}")

        stamina_values = re.findall(r"(\d{1,3}/100)", text)
        stamina_text = ",".join(stamina_values)
        logger.debug(f"Stamina values: {stamina_text}")

        found = False
        number = 0
        is_marching = False
        for stamina in stamina_values:
            number += 1
            stamina_value = list(map(int, stamina.split("/")))[0]
            if stamina_value > 100:
                logger.warning(f"Stamina value {stamina_value} is more than 100, get last two digits")
                stamina_value %= 100
            if stamina_value >= settings["minStamina"]:
                self.press_location(
                    settings["positions"]["centerScreen"]["x"],
                    settings["marchScreenTopBarHeight"]
                    + settings["marchUnitHeight"] * number
                    - settings["marchUnitHeight"] / 3
                )
                sleep(settings[SLEEP_SHORT])

                image = self.get_screenshot()
                button_is_gray = ImageHandler.check_pixel_is_gray(
                    image,
                    settings["positions"]["marchButtonColorPick"]["x"],
                    settings["positions"]["marchButtonColorPick"]["y"]
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
                self.analyze_march_unit(is_swiped=True, is_marching_before_swipe=is_marching)

    def do_hunt(self):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        if self.is_first_run:
            self.is_first_run = False
            self.press_world_button(settings)
            # TODO: Return all march units
            self.press_search_button(settings)
            self.press_search_wild_creatures_button(settings)
            # TODO: Check wild creature type and level
            self.press_back_button(settings)

        image = self.get_screenshot()
        march_units = ImageHandler.crop_image(
            image,
            settings["positions"]["marchUnits"]["x"],
            settings["positions"]["marchUnits"]["y"],
            settings["positions"]["marchUnits"]["h"],
            settings["positions"]["marchUnits"]["w"]
        )
        image_threshold = ImageHandler.threshold(march_units)
        text = ExtractText.run(image_threshold, char_whitelist="0123456789/")
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

    def run(self):
        self.do_hunt()

    @staticmethod
    def run_bots(bots):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        logger.info(f"Ready to run the hunting bot on {', '.join(bot.device.name for bot in bots)}")

        for bot in itertools.cycle(bots):
            try:
                while True:
                    if bot.is_finished:
                        # When the hunt is finished, return to anthill
                        bot.press_world_button(settings)
                        break
                    bot.do_hunt()

            except AllUnitsAreBusy:
                continue

            if all([bot.is_finished for bot in bots]):
                break
