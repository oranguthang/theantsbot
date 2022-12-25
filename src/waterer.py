import random
from time import sleep

from src.base import TheAntsBot, SLEEP_SHORT, SLEEP_MEDIUM
from src.exceptions import UserWateringCompleted
from src.logger import logger
from src.settings import Settings
from src.utils import THRESHOLD_DIVIDER, CommonTemplates


class WateringBot(TheAntsBot):
    def press_alliance_members_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "allianceMembersButton", sleep_duration)

    def press_find_exotic_pea_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "findExoticPeaButton", sleep_duration)

    def press_water_exotic_pea_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "waterExoticPeaButton", sleep_duration)

    def press_return_from_anthill_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "returnFromAnthillButton", sleep_duration)

    def press_visit_another_alliance_anthill_icon(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "visitAnotherAllianceAnthillIcon", sleep_duration)

    def do_water_in_alliance(self, watered_users, bar_num, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        found_new_user = True
        while found_new_user:
            self.press_close_banner_button(settings)
            self.press_alliance_button(settings)
            self.press_alliance_members_button(settings)

            # Unbox R1-R4 bar
            self.press_location(
                settings["positions"]["allianceMembersR1Button"]["x"],
                settings["positions"]["allianceMembersR1Button"]["y"] -
                settings["allianceMembersBarHeight"] * bar_num
            )
            sleep(settings[SLEEP_SHORT])

            # Scan text
            found_new_user = False
            current_users = set()
            try:
                found_new_current_user = True
                while found_new_current_user:
                    found_new_current_user = False
                    boxes = self.get_text_boxes_from_screenshot(settings=settings, rectangle_name="allianceMembersBox")
                    for x, y, text in boxes:
                        text_lower = text.lower()
                        if settings["serverNumber"] in text_lower and text_lower not in current_users:
                            current_users.add(text_lower)
                            found_new_current_user = True

                            if text_lower not in shared["watered_users"]:
                                shared["watered_users"][text_lower] = False

                            if shared["watered_users"][text_lower] is True:
                                continue

                            if text_lower in watered_users:
                                continue

                            found_new_user = True
                            watered_users.add(text_lower)
                            # Click nickname
                            self.press_location(
                                x / THRESHOLD_DIVIDER + settings["rectangles"]["allianceMembersBox"]["x"],
                                y / THRESHOLD_DIVIDER + settings["rectangles"]["allianceMembersBox"]["y"]
                            )
                            sleep(settings[SLEEP_MEDIUM])

                            # Scan profile bottom bar
                            found_icon = self.find_and_press_template(
                                settings, CommonTemplates.VISIT_ANTHILL, "allianceMemberProfileBottomBar",
                                sleep_duration=SLEEP_MEDIUM, multiplier=3
                            )
                            if found_icon:
                                found_exotic_pea = self.find_and_press_template(
                                    settings, CommonTemplates.FIND_EXOTIC_PEA, "anotherAnthillFindExoticPeaIcon"
                                )
                                if found_exotic_pea:
                                    self.press_water_exotic_pea_button(settings)
                                else:
                                    shared["watered_users"][text_lower] = True

                                self.press_return_from_anthill_button(settings)

                                raise UserWateringCompleted

                            # If didn't water pea, probably it's my account
                            self.press_back_button(settings)

                    if not found_new_current_user:
                        break

                    # Scroll users list
                    self.swipe(settings, "swipeAllianceMembers", duration_ms=1000)
                    sleep(settings[SLEEP_SHORT])

            except UserWateringCompleted:
                # User successfully watered, continue watering
                sleep(settings[SLEEP_MEDIUM] * 3)

        self.press_back_button(settings)

    def run(self, shared):
        logger.info(f"Ready to run the watering bot on {self.device.name}")

        # Wait random seconds to prevent race of workers
        sleep(random.randint(1, 30))

        watered_users = set()
        for bar_num in range(4):
            self.do_water_in_alliance(watered_users, bar_num, shared)

        logger.info(f"Total watered users: {watered_users}")
