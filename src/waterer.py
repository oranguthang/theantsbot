from time import sleep

from src.base import TheAntsBot, SLEEP_SHORT, SLEEP_MEDIUM
from src.exceptions import UserWateringCompleted
from src.logger import logger
from src.settings import Settings
from src.utils import ExtractText, ImageHandler


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

    def do_water_by_coordinates(self):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.press_world_button(settings)

        positions = settings["waterExoticPeasByHillsPositions"]
        for position in positions:
            self.press_search_button(settings)
            self.press_search_coords_button(settings)

            self.press_location_and_type(
                settings["positions"]["searchCoordXField"]["x"],
                settings["positions"]["searchCoordXField"]["y"],
                position["X"],
                backspace_count=4
            )
            self.press_back_button(settings)
            sleep(settings[SLEEP_SHORT])

            self.press_location_and_type(
                settings["positions"]["searchCoordYField"]["x"],
                settings["positions"]["searchCoordYField"]["y"],
                position["Y"],
                backspace_count=4
            )
            self.press_back_button(settings)

            self.press_search_coords_go_button(settings)
            self.press_center_screen(settings)
            self.press_visit_another_alliance_anthill_icon(settings)

            self.press_find_exotic_pea_button(settings)
            self.press_water_exotic_pea_button(settings)
            self.press_return_from_anthill_button(settings)

        self.press_world_button(settings)

    def do_water_in_alliance(self):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        divider = 2.5
        watered_users = set()

        found_new_user = True
        while found_new_user:
            self.press_alliance_button(settings)
            self.press_alliance_members_button(settings)

            # Unbox R1-R4 bars
            for i in range(0, 4):
                self.press_location(
                    settings["positions"]["allianceMembersR1Button"]["x"],
                    settings["positions"]["allianceMembersR1Button"]["y"] -
                    settings["allianceMembersBarHeight"] * i
                )
                sleep(settings[SLEEP_SHORT])

            # Scan text
            found_new_user = False
            current_users = set()
            try:
                found_new_current_user = True
                while found_new_current_user:
                    found_new_current_user = False
                    image = self.get_screenshot()
                    members = ImageHandler.crop_image(
                        image,
                        settings["positions"]["allianceMembersBox"]["x"],
                        settings["positions"]["allianceMembersBox"]["y"],
                        settings["positions"]["allianceMembersBox"]["h"],
                        settings["positions"]["allianceMembersBox"]["w"]
                    )
                    image_threshold = ImageHandler.threshold(members)
                    boxes = ExtractText.image_to_boxes(image_threshold)
                    for x, y, text in boxes:
                        text_lower = text.lower()
                        if settings["serverNumber"] in text_lower and text_lower not in current_users:
                            current_users.add(text_lower)
                            found_new_current_user = True
                        if settings["serverNumber"] in text_lower and text_lower not in watered_users:
                            watered_users.add(text_lower)
                            found_new_user = True
                            # Click nickname
                            self.press_location(
                                x / divider + settings["positions"]["allianceMembersBox"]["x"],
                                y / divider + settings["positions"]["allianceMembersBox"]["y"]
                            )
                            sleep(settings[SLEEP_MEDIUM])
                            # Scan profile bottom bar
                            image = self.get_screenshot()
                            bottom_bar = ImageHandler.crop_image(
                                image,
                                settings["positions"]["allianceMemberProfileBottomBar"]["x"],
                                settings["positions"]["allianceMemberProfileBottomBar"]["y"],
                                settings["positions"]["allianceMemberProfileBottomBar"]["h"],
                                settings["positions"]["allianceMemberProfileBottomBar"]["w"]
                            )
                            image_threshold = ImageHandler.threshold(bottom_bar)
                            profile_actions = ExtractText.image_to_boxes(
                                image_threshold,
                                char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                            )
                            for x1, y1, action_text in profile_actions:
                                if "visit" in action_text.lower():
                                    # Click Visit button
                                    self.press_location(
                                        x1 / divider + settings["positions"]["allianceMemberProfileBottomBar"]["x"],
                                        y1 / divider + settings["positions"]["allianceMemberProfileBottomBar"]["y"]
                                    )
                                    sleep(settings[SLEEP_MEDIUM] * 1.5)

                                    self.press_find_exotic_pea_button(settings)
                                    self.press_water_exotic_pea_button(settings)
                                    self.press_return_from_anthill_button(settings)

                                    raise UserWateringCompleted

                            # If didn't water pea, probably it's my account
                            self.press_back_button(settings)

                    if not found_new_current_user:
                        break

                    # Scroll users list
                    self.swipe(settings, "swipeAllianceMembers", duration_ms=1000)
                    sleep(settings[SLEEP_MEDIUM] * 1.5)

            except UserWateringCompleted:
                # User successfully watered, continue watering
                sleep(settings[SLEEP_MEDIUM] * 1.5)

        logger.info(f"Users, watered by {self.device.name}: {', '.join(watered_users)}")
        self.press_back_button(settings)

    def run(self):
        logger.info(f"Ready to run the watering bot on {self.device.name}")

        self.do_water_by_coordinates()
        self.do_water_in_alliance()
