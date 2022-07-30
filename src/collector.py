import re
from time import sleep

from src.base import TheAntsBot, SLEEP_SHORT, SLEEP_MEDIUM, SLEEP_LONG
from src.logger import logger
from src.settings import Settings
from src.utils import ExtractText, ImageHandler


class MorningBonusesCollectingBot(TheAntsBot):
    def press_alliance_evolution_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "allianceEvolutionButton", sleep_duration)

    def press_alliance_evolution_develop_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "allianceEvolutionDevelopButton", sleep_duration)

    def press_alliance_evolution_combat_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "allianceEvolutionCombatButton", sleep_duration)

    def press_alliance_evolution_donate_resources_button(self, settings, sleep_duration=None):
        self.press_position(settings, "allianceEvolutionDonateResourceButton", sleep_duration)

    def press_alliance_evolution_donate_diamonds_button(self, settings, sleep_duration=None):
        self.press_position(settings, "allianceEvolutionDonateDiamondButton", sleep_duration)

    def press_vip_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "VIPButton", sleep_duration)

    def press_vip_check_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "VIPCheckButton", sleep_duration)

    def press_vip_claim_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "VIPClaimButton", sleep_duration)

    def press_vip_signup_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "VIPSignUpButton", sleep_duration)

    def press_pack_shop_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "packShopButton", sleep_duration)

    def press_pack_shop_one_time_offer_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "packShopOneTimeOfferButton", sleep_duration)

    def press_pack_shop_time_limited_offer_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "packShopTimeLimitedOfferButton", sleep_duration)

    def press_pack_shop_free_bonus_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "packShopFreeBonusButton", sleep_duration)

    def press_hatch_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "hatchButton", sleep_duration)

    def press_hatch_free_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "hatchFreeButton", sleep_duration)

    def press_hatch_cross_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "hatchCrossButton", sleep_duration)

    def press_leaf_cutter_supply_button(self, settings, sleep_duration=SLEEP_LONG):
        self.press_position(settings, "leafCutterSupplyButton", sleep_duration)

    def press_feeding_ground(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "feedingGround", sleep_duration)

    def press_feeding_ground_supply_icon(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "feedingGroundSupplyIcon", sleep_duration)

    def press_feeding_ground_supply_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "feedingGroundSupplyButton", sleep_duration)

    def swipe_pack_shop_heading(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipePackShopHeading", duration_ms=500)
        sleep(settings[sleep_duration])

    def swipe_pack_shop_content(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipePackShopContent", duration_ms=500)
        sleep(settings[sleep_duration])

    def swipe_hatch_screen(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeHatchScreen", duration_ms=500)
        sleep(settings[sleep_duration])

    def fill_leaf_cutters(self, settings):
        cutters_positions = settings["leafCutterPositions"]
        for position in cutters_positions:
            # Press the cutter
            self.press_location(
                position["x"],
                position["y"]
            )
            sleep(settings[SLEEP_MEDIUM])

            # Press supply icon
            self.press_location(
                position["x1"],
                position["y1"]
            )
            sleep(settings[SLEEP_MEDIUM])
            self.press_leaf_cutter_supply_button(settings)

        # Get out and return to reset screen position
        self.press_world_button(settings)
        self.press_world_button(settings)

    def fill_feeding_ground(self, settings):
        self.press_feeding_ground(settings)
        self.press_feeding_ground_supply_icon(settings)
        self.press_feeding_ground_supply_button(settings)

        # Get out and return to reset screen position
        self.press_world_button(settings)
        self.press_world_button(settings)

    def get_bonuses(self, settings):
        # Get VIP bonuses
        self.press_vip_button(settings)

        self.press_vip_check_button(settings)
        self.press_vip_claim_button(settings)
        self.press_back_button(settings)

        self.press_vip_signup_button(settings)
        self.press_back_button(settings)

        self.press_back_button(settings)

        # Get Pack Shop bonuses
        self.press_pack_shop_button(settings)
        for _ in range(3):
            self.swipe_pack_shop_heading(settings)

        self.press_pack_shop_one_time_offer_button(settings)
        self.swipe_pack_shop_content(settings)
        self.press_pack_shop_free_bonus_button(settings)
        self.press_back_button(settings)

        self.press_pack_shop_time_limited_offer_button(settings)
        self.swipe_pack_shop_content(settings)
        self.press_pack_shop_free_bonus_button(settings)
        self.press_back_button(settings)

        self.press_back_button(settings)

    def hatch_special_ants(self, settings):
        # Free hatch Special Ants
        self.press_hatch_button(settings)

        # Supreme hatch
        self.press_hatch_free_button(settings)
        self.press_hatch_free_button(settings)
        self.press_hatch_cross_button(settings)
        self.swipe_hatch_screen(settings)

        # Advanced hatch
        self.press_hatch_free_button(settings)
        self.press_hatch_free_button(settings)
        self.press_hatch_cross_button(settings)
        self.swipe_hatch_screen(settings)

        # Normal hatch
        self.press_hatch_free_button(settings)
        self.press_hatch_free_button(settings)
        self.press_hatch_cross_button(settings)

        self.press_back_button(settings)

    def process_evolutions(self, settings, donate_resources=True, donate_diamonds=True):
        # Not working properly
        divider = 2.5

        image = self.get_screenshot()
        members = ImageHandler.crop_image(
            image,
            settings["positions"]["allianceEvolutionTopBar"]["x"],
            settings["positions"]["allianceEvolutionTopBar"]["y"],
            settings["positions"]["allianceEvolutionTopBar"]["h"],
            settings["positions"]["allianceEvolutionTopBar"]["w"]
        )
        image_threshold = ImageHandler.threshold(members)
        boxes = ExtractText.image_to_boxes(image_threshold, char_whitelist="0123456789/")
        for x, y, text in boxes:
            filtered_value = re.findall(r"(\d*/\d*)", text)
            if filtered_value:
                # Found an evolution block
                self.press_location(
                    x / divider + settings["positions"]["allianceEvolutionTopBar"]["x"],
                    y / divider + settings["positions"]["allianceEvolutionTopBar"]["y"]
                )
                sleep(settings[SLEEP_MEDIUM])

                if donate_resources:
                    for _ in range(25):
                        self.press_alliance_evolution_donate_resources_button(settings)
                    donate_resources = False

                if donate_diamonds:
                    for _ in range(10):
                        self.press_alliance_evolution_donate_diamonds_button(settings)

                self.press_back_button(settings)

    def process_evolutions_by_coordinates(self, settings, tab_name, donate_resources=True, donate_diamonds=True):
        evolutions_config = settings["allianceEvolutions"][tab_name]
        evolutions_positions = settings["allianceEvolutionsPositions"][evolutions_config]
        for position in evolutions_positions:
            self.press_location(
                position["x"],
                position["y"]
            )
            sleep(settings[SLEEP_MEDIUM])

            if donate_resources:
                for _ in range(25):
                    self.press_alliance_evolution_donate_resources_button(settings)
                donate_resources = False

            if donate_diamonds:
                for _ in range(10):
                    self.press_alliance_evolution_donate_diamonds_button(settings)

            self.press_back_button(settings)

    def donate_to_evolution(self, settings, donate_diamonds=True):
        self.press_alliance_button(settings)
        self.press_alliance_evolution_button(settings)
        self.press_alliance_evolution_develop_button(settings)
        self.process_evolutions_by_coordinates(settings, tab_name="develop",
                                               donate_diamonds=donate_diamonds)
        # self.process_evolutions(settings, donate_diamonds=donate_diamonds)

        self.press_alliance_evolution_combat_button(settings)
        self.process_evolutions_by_coordinates(settings, tab_name="combat", donate_resources=False,
                                               donate_diamonds=donate_diamonds)
        # self.process_evolutions(settings, donate_resources=False, donate_diamonds=donate_diamonds)

        self.press_back_button(settings)
        self.press_back_button(settings)

    def do_collect(self):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.fill_leaf_cutters(settings)
        self.fill_feeding_ground(settings)
        self.get_bonuses(settings)
        self.hatch_special_ants(settings)
        self.donate_to_evolution(settings)

    def run(self):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect()


class EveningBonusesCollectingBot(MorningBonusesCollectingBot):
    def press_exotic_pea_reward(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "exoticPeaReward", sleep_duration)

    def press_exotic_pea_reward_claim_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "exoticPeaRewardClaimButton", sleep_duration)

    def press_alliance_salary_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "allianceSalaryButton", sleep_duration)

    def press_alliance_salary_active_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "allianceSalaryActiveButton", sleep_duration)

    def press_alliance_salary_attendance_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "allianceSalaryAttendanceButton", sleep_duration)

    def press_alliance_salary_contribution_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "allianceSalaryContributionButton", sleep_duration)

    def press_mail_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "mailButton", sleep_duration)

    def press_mail_mark_as_read_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "mailMarkAsReadButton", sleep_duration)

    def claim_exotic_pea(self, settings):
        self.press_exotic_pea_reward(settings)
        self.press_exotic_pea_reward_claim_button(settings)

        self.press_back_button(settings)
        self.press_back_button(settings)

        # Get out and return to reset screen position
        self.press_world_button(settings)
        self.press_world_button(settings)

    def claim_rewards_by_positions(self, settings, position_name):
        positions = settings[position_name]
        for position in positions:
            # Press the reward
            self.press_location(
                position["x"],
                position["y"]
            )
            sleep(settings[SLEEP_SHORT])
            self.press_back_button(settings)

    def claim_rewards(self, settings):
        # Get alliance rewards
        self.press_alliance_button(settings)
        self.press_alliance_salary_button(settings)

        self.press_alliance_salary_active_button(settings)
        self.claim_rewards_by_positions(settings, "allianceSalaryActiveRewardsPositions")
        self.press_alliance_salary_attendance_button(settings)
        self.claim_rewards_by_positions(settings, "allianceSalaryAttendanceRewardsPositions")
        self.press_alliance_salary_contribution_button(settings)
        self.claim_rewards_by_positions(settings, "allianceSalaryContributionRewardsPositions")

        self.press_back_button(settings)
        self.press_back_button(settings)

    def read_mail(self, settings):
        self.press_mail_button(settings)

        x = settings["screenWidth"] // 2
        positions = settings["mailBoxesPositionsY"]
        for y in positions:
            # Press an option
            self.press_location(x, y)
            sleep(settings[SLEEP_SHORT])
            self.press_mail_mark_as_read_button(settings)
            self.press_back_button(settings)

            image = self.get_screenshot()
            # Make sure that we returned to mail root
            returned_to_mail = ImageHandler.check_pixel_is_blue(
                image,
                settings["positions"]["messagesButtonColorPick"]["x"],
                settings["positions"]["messagesButtonColorPick"]["y"]
            )
            if not returned_to_mail:
                # If we claimed a reward from mail, we need to press back button again
                self.press_back_button(settings)

        self.press_back_button(settings)

    def do_collect(self):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.fill_leaf_cutters(settings)
        self.fill_feeding_ground(settings)
        self.donate_to_evolution(settings, donate_diamonds=False)
        self.claim_exotic_pea(settings)
        self.claim_rewards(settings)
        self.read_mail(settings)

    def run(self):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect()
