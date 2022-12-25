import itertools
import re
from datetime import datetime
from time import sleep

from src.base import TheAntsBot, SLEEP_SHORT, SLEEP_MEDIUM, SLEEP_LONG
from src.collector import MorningBonusesCollectingBot
from src.exceptions import AllUnitsAreBusy, NoMarchUnitScreen
from src.logger import logger
from src.settings import Settings
from src.utils import Colors, THRESHOLD_DIVIDER, HeaderTemplates, EventTemplates, AlertTemplates


class SoldierTypes:
    GUARDIANS = "guardians"
    SHOOTERS = "shooters"
    CARRIERS = "carriers"
    DEFAULT = "default"


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

    def press_march_troops_icon(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "marchTroopsIcon", sleep_duration)

    def press_march_troops_switch_formation_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "marchTroopsSwitchFormationButton", sleep_duration)

    def press_march_troops_switch_formation_confirm_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "marchTroopsSwitchFormationConfirmButton", sleep_duration)

    def swipe_back_search_screen(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.swipe(settings, "swipeBackHuntGatherScreen", duration_ms=1000)
        sleep(settings[sleep_duration])

    def swipe_search_screen(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.swipe(settings, "swipeHuntGatherScreen", duration_ms=1000)
        sleep(settings[sleep_duration])

    def swipe_march_screen_down(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeMarchScreenDown", duration_ms=500)
        sleep(settings[sleep_duration])

    def swipe_march_screen_up(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeMarchScreenUp", duration_ms=500)
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

    def set_formation_type(self, settings, soldiers_type):
        if soldiers_type is None:
            return

        self.press_march_troops_icon(settings)
        formation_number = settings[f"{soldiers_type}FormationNumber"]

        number_position = settings["troopFormationsPositions"][formation_number - 1]
        self.press_location(number_position["x"], number_position["y"])
        sleep(settings[SLEEP_SHORT])

        while True:
            self.press_march_troops_switch_formation_button(settings)
            found_alert = self.find_template(settings, AlertTemplates.CANNOT_SWITCH_FORMATION,
                                             rectangle_name="alertsScreenArea", threshold=0.9)
            if found_alert:
                self.press_back_button(settings, sleep_duration=SLEEP_LONG)
            else:
                break

        self.press_march_troops_switch_formation_confirm_button(settings)

        self.press_back_button(settings)

    def march_pro_troop(self, settings):
        image = self.get_screenshot(settings, rectangle_name="screenMenuHeading")
        found_menu = self.find_template(settings, HeaderTemplates.MARCH_TROOPS, image=image)
        if not found_menu:
            # Insufficient attack times or something is wrong
            return False

        self.swipe_march_screen_up(settings)

        troop_number = 1
        self.press_location(
            settings["positions"]["centerScreen"]["x"],
            settings["marchScreenTopBarHeight"]
            + settings["marchUnitHeight"] * troop_number
            - settings["marchUnitHeight"] / 3
        )
        sleep(settings[SLEEP_SHORT])

        button_is_gray = True
        while button_is_gray:
            image = self.get_screenshot(settings)
            button_is_gray = self.check_pixel_color(image, settings, "marchButtonColorPick", Colors.GRAY)
            if button_is_gray:
                sleep(settings[SLEEP_LONG])

        logger.info(f"Pro Troop is ready, go!")
        self.press_march_button(settings)
        return True

    def analyze_march_unit(self, is_swiped=False, is_marching_before_swipe=False, mode="hunt"):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        image = self.get_screenshot(settings, rectangle_name="screenMenuHeading")
        found_menu = self.find_template(settings, HeaderTemplates.MARCH_TROOPS, image=image)
        if not found_menu:
            heading_is_gray = self.check_pixel_color(
                image, settings, "screenMenuHeadingColorPick", Colors.GRAY
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
                self.swipe_march_screen_down(settings)
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


class PangolinBot(MorningBonusesCollectingBot, HuntingBot):
    def press_pangolin_challenge_button(self, settings, sleep_duration=SLEEP_MEDIUM, multiplier=3):
        self.press_position(settings, "pangolinChallengeButton", sleep_duration, multiplier=multiplier)

    def press_pangolin_location(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "pangolinLocation", sleep_duration)

    def press_pangolin_invade_icon(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "pangolinInvadeIcon", sleep_duration)

    def do_pangolin(self):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.press_alliance_button(settings)
        self.press_alliance_events_button(settings)
        found_event = self.find_event(settings, [EventTemplates.PANGOLIN], press_events_button=False)
        if not found_event:
            self.press_back_button(settings)
            self.press_back_button(settings)
            return

        self.press_pangolin_challenge_button(settings)

        weekday = datetime.today().weekday()
        soldier_types_by_weekdays = {
            2: SoldierTypes.GUARDIANS,
            3: SoldierTypes.SHOOTERS,
            4: SoldierTypes.CARRIERS,
        }
        self.set_formation_type(settings, soldier_types_by_weekdays.get(weekday))

        for _ in range(15):
            self.press_pangolin_location(settings)
            self.press_pangolin_invade_icon(settings)

            # Use only Pro Troop to attack pangolin
            success = self.march_pro_troop(settings)
            if not success:
                break

        # Return formation type to default
        self.set_formation_type(settings, SoldierTypes.DEFAULT)

        # Go home
        self.press_world_button(settings)

    def run(self, shared):
        logger.info(f"Ready to run the pangolin bot on {self.device.name}")

        self.do_pangolin()


class GroundhogBot(MorningBonusesCollectingBot, HuntingBot):
    def press_groundhog_location(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "groundhogLocation", sleep_duration)

    def press_groundhog_invade_icon(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "groundhogInvadeIcon", sleep_duration)

    def do_groundhog(self):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.press_world_button(settings)
        self.press_world_button(settings)

        self.get_advanced_raspberry_bonus(settings)
        found_event = self.find_event(settings, [EventTemplates.STRONGEST_WARZONE])
        if not found_event:
            self.press_back_button(settings)

        self.press_strongest_warzone_go_button(settings, sleep_duration=SLEEP_MEDIUM, multiplier=3)
        self.set_formation_type(settings, SoldierTypes.SHOOTERS)

        for _ in range(20):
            self.press_groundhog_location(settings)
            self.press_groundhog_invade_icon(settings)

            # Use only Pro Troop to attack groundhog
            success = self.march_pro_troop(settings)
            if not success:
                break

        # Return formation type to default
        self.set_formation_type(settings, SoldierTypes.DEFAULT)

        # Go home
        self.press_world_button(settings)

    def run(self, shared):
        logger.info(f"Ready to run the groundhog bot on {self.device.name}")

        self.do_groundhog()
