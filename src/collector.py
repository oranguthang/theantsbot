import re
from datetime import datetime
from time import sleep

from models.task_icons.model import TaskIconTypes
from src.base import TheAntsBot, SLEEP_SHORT, SLEEP_MEDIUM, SLEEP_LONG
from src.logger import logger
from src.settings import Settings
from src.utils import THRESHOLD_DIVIDER, Colors, ImageHandler


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

    def press_pack_shop_free_space_bottom(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "packShopFreeSpaceBottom", sleep_duration)

    def press_hatch_menu_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "hatchMenuButton", sleep_duration)

    def press_hatch_special_ant_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "hatchSpecialAntButton", sleep_duration)

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

    def press_termite_farm_breed_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "hatchInsectsBreedFodderButton", sleep_duration)

    def press_hatch_insects_hatch_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "hatchInsectsHatchButton", sleep_duration)

    def press_hatch_insects_free_space_bottom(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "hatchInsectsFreeSpaceBottom", sleep_duration)

    def press_insect_habitat(self, settings, sleep_duration=SLEEP_SHORT, relative=False):
        if relative:
            position_name = "insectHabitatRelativeFromNests"
        else:
            position_name = "insectHabitat"
        self.press_position(settings, position_name, sleep_duration)

    def press_insect_habitat_insects_icon(self, settings, sleep_duration=SLEEP_SHORT, relative=False):
        if relative:
            position_name = "insectHabitatInsectsIconRelativeFromNests"
        else:
            position_name = "insectHabitatInsectsIcon"
        self.press_position(settings, position_name, sleep_duration)

    def swipe_pack_shop_heading(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipePackShopHeading", duration_ms=500)
        sleep(settings[sleep_duration])

    def swipe_pack_shop_heading_right(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipePackShopHeadingRight", duration_ms=1000)
        sleep(settings[sleep_duration])

    def swipe_pack_shop_content(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipePackShopContent", duration_ms=500)
        sleep(settings[sleep_duration])

    def swipe_hatch_screen(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeHatchScreen", duration_ms=500)
        sleep(settings[sleep_duration])

    def swipe_screen_to_hatch_insects(self, settings, sleep_duration=SLEEP_SHORT):
        swipe_name = "swipeScreenToHatchInsects"
        self.swipe(settings, swipe_name, duration_ms=3000)

        for _ in range(2):
            self.press_location(settings["swipes"][swipe_name]["x2"], settings["swipes"][swipe_name]["y2"])

        sleep(settings[sleep_duration])

    def swipe_screen_to_troop_camp(self, settings, sleep_duration=SLEEP_SHORT):
        positions = settings["troopCampRelativePath"]
        for position in positions:
            # Click to buildings to find way to Troop Camp
            self.press_location(
                position["x"],
                position["y"]
            )
            sleep(settings[sleep_duration])

    def swipe_cave_challenge_screen_up(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeCaveChallengeScreenUp", duration_ms=1000)
        sleep(settings[sleep_duration])

    def swipe_cave_challenge_screen_down(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeCaveChallengeScreenDown", duration_ms=1000)
        sleep(settings[sleep_duration])

    def do_duel_deploy_troops(self, settings, press_back_button=True):
        image = self.get_screenshot(settings)
        need_to_deploy_troops = self.check_pixel_color(
            image, settings, "duelOfQueensFillTroopsConfirmColorPick", Colors.BLUE
        )
        if need_to_deploy_troops:
            # If this is a new season, and we need to deploy the troops
            self.press_position(settings, "duelOfQueensFillTroopsConfirmColorPick", sleep_duration=SLEEP_SHORT)
            if press_back_button:
                self.press_back_button(settings)

    def do_duel(self, settings, duel_name, challenges_count=10):
        self.press_position(settings, f"{duel_name}Bar", sleep_duration=SLEEP_SHORT)
        self.do_duel_deploy_troops(settings)

        # Close alert, if we are promoted to higher league
        self.press_free_space_bottom(settings)
        for i in range(challenges_count):
            self.press_position(settings, "duelOfQueensChallengeButton", sleep_duration=SLEEP_SHORT)
            self.press_position(settings, f"{duel_name}FirstOpponentButton", sleep_duration=SLEEP_SHORT)
            if i == 0:
                self.do_duel_deploy_troops(settings, press_back_button=False)
            self.press_position(settings, "duelOfQueensDepartButton", sleep_duration=SLEEP_SHORT)
            self.press_position(settings, "duelOfQueensSkipButton", sleep_duration=SLEEP_SHORT)
            self.press_back_button(settings)

        self.press_position(settings, "duelOfQueensRewardsButton", sleep_duration=SLEEP_SHORT)
        # It's the same position for Claim rewards Button
        self.press_position(settings, "duelOfQueensDepartButton", sleep_duration=SLEEP_SHORT)
        self.press_position(settings, "duelOfQueensRewardsClaimButton", sleep_duration=SLEEP_SHORT)
        # Close Claim rewards window
        self.press_position(settings, "duelOfQueensDepartButton", sleep_duration=SLEEP_SHORT)

        self.press_back_button(settings)
        self.press_back_button(settings)

    def do_duel_of_queens(self, settings):
        if settings["duelOfQueensEnabled"] is True:
            self.do_duel(settings, "duelOfQueens", challenges_count=10)
        if settings["duelOfSpecialAntsEnabled"] is True:
            self.do_duel(settings, "duelOfSpecialAnts", challenges_count=5)

        self.press_back_button(settings)

    def do_get_duel_of_queens_reward(self, settings):
        if settings["duelOfQueensEnabled"] is True:
            self.press_position(settings, "duelOfQueensBar", sleep_duration=SLEEP_SHORT)
            # Close alert, if we are promoted to higher league
            self.press_free_space_bottom(settings)

            self.press_position(settings, "duelOfQueensRewardsButton", sleep_duration=SLEEP_SHORT)
            self.press_position(settings, "duelOfQueensRewardsRankingButton", sleep_duration=SLEEP_SHORT)

            for i in range(5):
                self.press_position(settings, "duelOfQueensRewardsRankingClaimButton", sleep_duration=SLEEP_SHORT)
                self.press_position(settings, "duelOfQueensRewardsRankingButton", sleep_duration=SLEEP_SHORT)

            self.press_back_button(settings)
            self.press_back_button(settings)

        self.press_back_button(settings)

    def do_crystal_mine(self, settings):
        self.press_position(settings, "crystalMineEnterButton", sleep_duration=SLEEP_SHORT)

        levels_positions = settings["crystalMineLevelsPositions"]
        for level_position in reversed(levels_positions):
            image = self.get_screenshot(settings)
            is_level_available = self.check_pixel_color(image, settings, level_position, Colors.BLUE)
            next_position = {"x": level_position["x"], "y": level_position["y"] + 150}
            is_next_button_blue = self.check_pixel_color(image, settings, next_position, Colors.BLUE)
            if is_level_available and is_next_button_blue:
                # Press the button of level
                self.press_location(
                    level_position["x"],
                    level_position["y"]
                )
                sleep(settings[SLEEP_SHORT])
                break

        self.press_position(settings, "crystalMineRapidOccupyButton", sleep_duration=SLEEP_SHORT)
        self.press_position(settings, "crystalMineRapidOccupyConfirmButton", sleep_duration=SLEEP_SHORT)
        self.press_position(settings, "crystalMineDepartButton", sleep_duration=SLEEP_SHORT)

        self.press_back_button(settings)
        self.press_back_button(settings)

    def do_cave_challenge_duel(self, settings, plate_position, challenges_count=10):
        self.press_location(
            plate_position["x1"],
            plate_position["y1"]
        )
        sleep(settings[SLEEP_SHORT])
        for i in range(challenges_count):
            self.press_position(settings, "caveChallengeAttackButton", sleep_duration=SLEEP_SHORT)
            self.press_position(settings, "caveChallengeAttackButton", sleep_duration=SLEEP_MEDIUM)
            self.press_position(settings, "caveChallengeSkipButton", sleep_duration=SLEEP_SHORT)
            self.press_position(settings, "caveChallengeAttackButton", sleep_duration=SLEEP_SHORT)
        self.press_back_button(settings)

    def do_cave_challenge_claim_reward(self, settings, plate_position):
        self.press_location(
            plate_position["x"],
            plate_position["y"]
        )
        sleep(settings[SLEEP_SHORT])
        self.press_position(settings, "caveChallengeClaimRewardButton", sleep_duration=SLEEP_SHORT)
        self.press_position(settings, "caveChallengeFreeSpaceBottom", sleep_duration=SLEEP_SHORT)

    def do_cave_challenge(self, settings):
        weekday = datetime.today().weekday()

        plates_positions = settings["caveChallengePlatesPositions"]
        if weekday == 0:
            # if Monday, we need to claim reward from Sunday
            self.swipe_cave_challenge_screen_down(settings)
            self.do_cave_challenge_claim_reward(settings, plates_positions[3])
            self.swipe_cave_challenge_screen_up(settings)
            self.do_cave_challenge_duel(settings, plates_positions[weekday])
        elif weekday in (1, 2):
            self.swipe_cave_challenge_screen_up(settings)
            self.do_cave_challenge_claim_reward(settings, plates_positions[weekday - 1])
            self.do_cave_challenge_duel(settings, plates_positions[weekday])
        elif weekday == 3:
            # if Thursday, we need to claim reward from Wednesday
            self.swipe_cave_challenge_screen_up(settings)
            self.do_cave_challenge_claim_reward(settings, plates_positions[weekday - 1])
            self.swipe_cave_challenge_screen_down(settings)
            self.do_cave_challenge_duel(settings, plates_positions[weekday - 3])
        elif weekday in (4, 5, 6):
            self.swipe_cave_challenge_screen_up(settings)
            self.swipe_cave_challenge_screen_down(settings)
            self.do_cave_challenge_claim_reward(settings, plates_positions[weekday - 4])
            self.do_cave_challenge_duel(settings, plates_positions[weekday - 3])

        self.press_back_button(settings)

    def do_trade_with_ladybug(self, settings):
        # TODO: Not implemented yet
        self.press_position(settings, "tradeWithLadybugButton", sleep_duration=SLEEP_SHORT)
        self.press_back_button(settings)

    def do_claim_exotic_pea(self, settings):
        self.press_position(settings, "exoticPeaRewardIcon", sleep_duration=SLEEP_SHORT)
        self.press_position(settings, "exoticPeaRewardClaimButton", sleep_duration=SLEEP_SHORT)
        self.press_back_button(settings)
        self.press_back_button(settings)

    def process_task(self, settings, x, y, task_function):
        self.press_location(x, y)
        sleep(settings[SLEEP_SHORT])
        if callable(task_function):
            task_function(settings)

    def do_tasks(self, settings, icons_model):
        found_new_task = True
        while found_new_task:
            found_new_task = False
            image = self.get_screenshot(settings, "anthillTasksIconsBar")
            image = ImageHandler.decode_image(image)
            circles = ImageHandler.get_circles(
                image, hough_blur_radius=5, output_blur_radius=3, min_dist=50,
                hough_param1=50, hough_param2=50, min_radius=20, max_radius=40
            )
            for circle in circles:
                x, y, image = circle["x"], circle["y"], circle["image"]
                x_shifted = x + settings["rectangles"]["anthillTasksIconsBar"]["x"]
                y_shifted = y + settings["rectangles"]["anthillTasksIconsBar"]["y"]
                predicted = icons_model.predict_single(image)

                if predicted in (
                    TaskIconTypes.FIND_EXOTIC_PEA,
                    TaskIconTypes.LACK_OF_FUNGUS,
                    TaskIconTypes.SOLDIERS_REFORM,  # TODO
                    TaskIconTypes.PATH_TO_BUILDINGS,
                    TaskIconTypes.WARZONE_CUSTOMIZATION,
                    TaskIconTypes.HATCH_ANTS,  # Skip because of separate handler
                ):
                    # TODO: Not implemented yet
                    continue

                found_new_task = True
                if predicted == TaskIconTypes.DUEL_OF_QUEENS:
                    self.process_task(settings, x_shifted, y_shifted, self.do_duel_of_queens)

                if predicted == TaskIconTypes.GET_DUEL_OF_QUEENS_REWARD:
                    self.process_task(settings, x_shifted, y_shifted, self.do_get_duel_of_queens_reward)

                elif predicted == TaskIconTypes.MINE_CAVE:
                    self.process_task(settings, x_shifted, y_shifted, self.do_crystal_mine)

                elif predicted == TaskIconTypes.CAVE_CHALLENGE:
                    self.process_task(settings, x_shifted, y_shifted, self.do_cave_challenge)

                elif predicted == TaskIconTypes.LADYBUG:
                    self.process_task(settings, x_shifted, y_shifted, self.do_trade_with_ladybug)

                elif predicted == TaskIconTypes.GET_EXOTIC_PEA_REWARD:
                    self.process_task(settings, x_shifted, y_shifted, self.do_claim_exotic_pea)

                elif predicted in (
                    TaskIconTypes.EVOLUTION,
                    TaskIconTypes.HATCH_INSECTS,
                    TaskIconTypes.HATCH_INSECT_FODDER
                ):
                    # Just close icon
                    self.process_task(settings, x_shifted, y_shifted, task_function=None)

                break

        # Get out and return to reset screen position
        self.press_world_button(settings)
        self.press_world_button(settings)

    def fill_leaf_cutters(self, settings):
        cutters_count = settings["leafCuttersCount"]
        cutters_positions = settings["leafCutterPositions"][:cutters_count]
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
        self.press_free_space_bottom(settings)

        self.press_vip_signup_button(settings)
        self.press_free_space_bottom(settings)
        # Close alert about promotion to next VIP level
        self.press_free_space_bottom(settings)

        self.press_back_button(settings)

        # Get Pack Shop bonuses
        self.press_pack_shop_button(settings)
        for _ in range(3):
            self.swipe_pack_shop_heading(settings)

        self.press_pack_shop_one_time_offer_button(settings)
        self.swipe_pack_shop_content(settings)
        self.press_pack_shop_free_bonus_button(settings)
        self.press_pack_shop_free_space_bottom(settings)

        self.press_pack_shop_time_limited_offer_button(settings)
        self.swipe_pack_shop_content(settings)
        self.press_pack_shop_free_bonus_button(settings)
        self.press_pack_shop_free_space_bottom(settings)

        rewards_positions = settings["packShopTimeLimitedOfferProgressRewards"]
        for position in rewards_positions:
            # Press the reward
            self.press_location(
                position["x"],
                position["y"]
            )
            sleep(settings[SLEEP_MEDIUM])
            self.press_back_button(settings)

        # Click all other boxes to clear red dots with alerts
        basic_position = settings["positions"]["packShopOneTimeOfferButton"]
        mutation_positions = settings["packShopMutationPositions"]
        for start_position in (2, 0, 0):
            for i in range(start_position, 5):
                self.press_location(
                    basic_position["x"] + 135 * i,
                    basic_position["y"]
                )
                sleep(settings[SLEEP_SHORT])
                # TODO: Fix with icon recognition
                # Dirty hack - we don't know the position of mutation packs and try to click everywhere
                for position in mutation_positions:
                    self.press_location(
                        position["x"],
                        position["y"]
                    )
            self.swipe_pack_shop_heading_right(settings)

        self.press_back_button(settings)

    def process_resource_factory(self, settings):
        positions = settings["resourceFactoryRelativePath"]
        for position in positions:
            # Click to buildings to find way to Resource Factory
            self.press_location(
                position["x"],
                position["y"]
            )
            sleep(settings[SLEEP_SHORT])
        self.press_position(settings, "resourceFactoryProcessIcon", sleep_duration=SLEEP_MEDIUM)

        image = self.get_screenshot(settings)
        is_button_gray = self.check_pixel_color(image, settings, "resourceFactoryProcessButton", Colors.GRAY)
        if not is_button_gray:
            self.press_position(settings, "resourceFactoryProcessButton", sleep_duration=SLEEP_MEDIUM)

            image = self.get_screenshot(settings)
            is_overflow = self.check_pixel_color(image, settings, "resourceFactoryOverflowConfirmButton", Colors.BLUE)
            if is_overflow:
                # If this is a new season, and we need to deploy the troops
                self.press_position(settings, "resourceFactoryOverflowConfirmButton", sleep_duration=SLEEP_MEDIUM)

        else:
            self.press_back_button(settings)

        self.press_world_button(settings)
        self.press_world_button(settings)

    def hatch_ants(self, settings):
        config = settings["farmHatchingConfig"][str(self.device.number)]

        # Mutate ants
        self.swipe_screen_to_troop_camp(settings)
        self.press_position(settings, "troopCampSoldiersButton", sleep_duration=SLEEP_MEDIUM)

        image = self.get_screenshot(settings, rectangle_name="marchUnitsHeading")
        text = self.get_text_from_screenshot(image=image, settings=settings)
        logger.debug(f"Extracted text from Troop Camp heading: {text}")

        if "Troop" not in text and "Camp" not in text:
            self.press_back_button(settings)
        else:
            mutation_upgrade_button_align_left = 45
            mutation_upgrade_button_align_top = 175
            mutation_plates = settings["troopCampPlatesPositions"]
            position = mutation_plates[config["plate"] - 1]
            self.press_location(position["x"], position["y"])
            sleep(settings[SLEEP_SHORT])
            # Align of Upgrade button, it could be center or left
            if config["align"] == "left":
                self.press_location(
                    position["x"] - mutation_upgrade_button_align_left,
                    position["y"] + mutation_upgrade_button_align_top
                )
            elif config["align"] == "center":
                self.press_location(
                    position["x"],
                    position["y"] + mutation_upgrade_button_align_top
                )
            sleep(settings[SLEEP_SHORT])

            self.press_location_and_type(settings, "troopCampInputAmountField", config["amount"], backspace_count=6)
            self.press_position(settings, "troopCampStartMutationButton", sleep_duration=SLEEP_SHORT)
            self.press_back_button(settings)
            self.press_back_button(settings)

            image = self.get_screenshot(settings, rectangle_name="marchUnitsHeading")
            text = self.get_text_from_screenshot(image=image, settings=settings)
            if "Troop" in text or "Camp" in text:
                # if mutation was already started, and we still in Troop Camp, go back
                self.press_back_button(settings)

        self.press_world_button(settings)
        self.press_world_button(settings)

        # Hatch ants
        hatching_nests = settings["hatchNestPositions"]
        for nest_position in hatching_nests:
            # Press nest location
            self.press_location(nest_position["x"], nest_position["y"])
            sleep(settings[SLEEP_SHORT])
            # Press hatch icon
            self.press_location(nest_position["x1"], nest_position["y1"])
            sleep(settings[SLEEP_MEDIUM])

            self.press_location_and_type(settings, "hatchAntsInputAmountField", config["amount"], backspace_count=6)
            self.press_position(settings, "hatchAntsStartButton", sleep_duration=SLEEP_SHORT)
            self.press_back_button(settings)

        self.press_world_button(settings)
        self.press_world_button(settings)

    def hatch_special_ants(self, settings):
        # Free hatch Special Ants
        self.press_hatch_menu_button(settings)

        # Supreme hatch
        self.press_hatch_special_ant_button(settings)
        self.press_hatch_special_ant_button(settings)
        self.press_hatch_cross_button(settings)
        self.swipe_hatch_screen(settings)

        # Advanced hatch
        self.press_hatch_special_ant_button(settings)
        self.press_hatch_special_ant_button(settings)
        self.press_hatch_cross_button(settings)
        self.swipe_hatch_screen(settings)

        # Normal hatch
        self.press_hatch_special_ant_button(settings)
        self.press_hatch_special_ant_button(settings)
        self.press_hatch_cross_button(settings)

        self.press_back_button(settings)

    def check_and_hatch_free_special_ant(self, settings):
        image = self.get_screenshot(settings)
        # TODO: Dirty hack - check for specific color
        found_red_dot = self.check_pixel_color(
            image, settings, "hatchSpecialAntButtonColorPick", (10, 22, 149), threshold=5, exact=True
        )
        if found_red_dot:
            # If we have red dot with numbers, we can hatch free special ant
            self.press_hatch_menu_button(settings)
            self.press_hatch_special_ant_button(settings)
            self.press_hatch_special_ant_button(settings)
            self.press_hatch_cross_button(settings)
            self.press_back_button(settings)

    def process_termite_farms(self, settings, positions):
        for position in positions:
            image = self.get_screenshot(settings)
            image = ImageHandler.crop_image(image, position["x"] - 50, position["y"] - 100, 100, 100)
            image = ImageHandler.decode_image(image)
            circles = ImageHandler.get_circles(
                image, hough_blur_radius=3, output_blur_radius=3, min_dist=50,
                hough_param1=50, hough_param2=50, min_radius=20, max_radius=40
            )
            # TODO: Change to image recognition
            if circles:
                # Press the farm to collect fodder
                self.press_location(position["x"], position["y"])
                sleep(settings[SLEEP_SHORT])

            # Press the farm
            self.press_location(position["x"], position["y"])
            sleep(settings[SLEEP_SHORT])

            # Press breed icon
            self.press_location(
                position["x2"],
                position["y2"]
            )
            sleep(settings[SLEEP_SHORT])
            self.press_termite_farm_breed_button(settings)

    def hatch_insects(self, settings):
        positions = settings["termiteFarmsAndInsectNestsPositions"]

        # Process left farms
        self.swipe_screen_to_hatch_insects(settings)
        left_farms = positions[0:3]
        self.process_termite_farms(settings, left_farms)
        self.press_world_button(settings)
        self.press_world_button(settings)

        # Process the nests
        self.swipe_screen_to_hatch_insects(settings)
        nests = positions[3:7]
        for position in nests:
            # Press the nest
            self.press_location(position["x"], position["y"])
            sleep(settings[SLEEP_SHORT])

            # Press hatch icon
            self.press_location(position["x1"], position["y1"])
            sleep(settings[SLEEP_SHORT])
            self.press_hatch_insects_hatch_button(settings)

            image = self.get_screenshot(settings)
            panel_is_gray = self.check_pixel_color(image, settings, "hatchInsectsBottomPanelColorPick", Colors.GRAY)
            if not panel_is_gray:
                # If panel is brown, we collected a hatched insect and need to return
                self.press_back_button(settings)
                self.press_hatch_insects_hatch_button(settings)

            # Click to free space to close alert, if we don't have resources or clicked to unhatch
            self.press_hatch_insects_free_space_bottom(settings)
            self.press_back_button(settings)

        self.press_insect_habitat(settings, relative=True)
        self.press_insect_habitat_insects_icon(settings, relative=True)
        self.press_back_button(settings)

        self.press_world_button(settings)
        self.press_world_button(settings)

        # Process right farms
        self.swipe_screen_to_hatch_insects(settings)
        right_farms = positions[7:10]
        self.process_termite_farms(settings, right_farms)
        self.press_world_button(settings)
        self.press_world_button(settings)

    def process_evolutions(self, settings, donate_resources=True, donate_diamonds=True):
        # Not working properly
        boxes = self.get_text_boxes_from_screenshot(settings=settings, rectangle_name="marchUnits",
                                                    char_whitelist="0123456789/")
        for x, y, text in boxes:
            filtered_value = re.findall(r"(\d*/\d*)", text)
            if filtered_value:
                # Found an evolution block
                self.press_location(
                    x / THRESHOLD_DIVIDER + settings["positions"]["allianceEvolutionTopBar"]["x"],
                    y / THRESHOLD_DIVIDER + settings["positions"]["allianceEvolutionTopBar"]["y"]
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

            image = self.get_screenshot(settings)
            if donate_resources:
                button_is_gray = self.check_pixel_color(
                    image, settings, "allianceEvolutionDonateResourceButtonColorPick", Colors.GRAY
                )
                if not button_is_gray:
                    for _ in range(25):
                        self.press_alliance_evolution_donate_resources_button(settings)

            if donate_diamonds:
                button_is_gray = self.check_pixel_color(
                    image, settings, "allianceEvolutionDonateDiamondButtonColorPick", Colors.GRAY
                )
                if not button_is_gray:
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
        self.process_evolutions_by_coordinates(settings, tab_name="combat",
                                               donate_diamonds=donate_diamonds)
        # self.process_evolutions(settings, donate_resources=False, donate_diamonds=donate_diamonds)

        self.press_back_button(settings)
        self.press_back_button(settings)

    def do_collect(self, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.press_close_banner_button(settings)
        self.do_tasks(settings, shared["models"]["task_icons"])
        self.process_resource_factory(settings)
        self.fill_leaf_cutters(settings)
        self.fill_feeding_ground(settings)
        self.get_bonuses(settings)
        self.hatch_special_ants(settings)
        self.donate_to_evolution(settings)
        self.hatch_ants(settings)
        self.hatch_insects(settings)

    def run(self, shared):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect(shared)


class EveningBonusesCollectingBot(MorningBonusesCollectingBot):
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

    def claim_rewards_by_positions(self, settings, position_name, press_back_button=True):
        positions = settings[position_name]
        for position in positions:
            # Press the reward
            self.press_location(
                position["x"],
                position["y"]
            )
            sleep(settings[SLEEP_SHORT])
            if press_back_button:
                self.press_back_button(settings)
            else:
                self.press_free_space_bottom(settings)

    def claim_rewards(self, settings):
        # Get alliance rewards
        self.press_alliance_button(settings)
        self.press_alliance_salary_button(settings)

        self.press_alliance_salary_active_button(settings)
        self.claim_rewards_by_positions(settings, "allianceSalaryActiveRewardsPositions")
        self.press_alliance_salary_attendance_button(settings)
        self.claim_rewards_by_positions(settings, "allianceSalaryAttendanceRewardsPositions", press_back_button=False)
        self.press_alliance_salary_contribution_button(settings)
        self.claim_rewards_by_positions(settings, "allianceSalaryContributionRewardsPositions", press_back_button=False)

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

            image = self.get_screenshot(settings)
            # Make sure that we returned to mail root
            returned_to_mail = self.check_pixel_color(
                image, settings, "messagesButtonColorPick", Colors.BLUE
            )
            if not returned_to_mail:
                # If we claimed a reward from mail, we need to press back button again
                self.press_back_button(settings)

        self.press_back_button(settings)

    def do_collect(self, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.press_close_banner_button(settings)
        self.do_tasks(settings, shared["models"]["task_icons"])
        self.process_resource_factory(settings)
        self.fill_leaf_cutters(settings)
        self.fill_feeding_ground(settings)
        self.donate_to_evolution(settings, donate_diamonds=False)
        self.claim_rewards(settings)
        self.read_mail(settings)
        self.hatch_insects(settings)

    def run(self, shared):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect(shared)


class ForceEventBonusesCollectingBot(MorningBonusesCollectingBot):
    def press_force_event_tasks_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "forceEventTasksButton", sleep_duration)

    def press_force_event_transport_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "forceEventTransportButton", sleep_duration)

    def press_force_event_task_reward_claim_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "forceEventTaskRewardClaimButton", sleep_duration)

    def press_force_event_task_empty_field(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "forceEventTaskEmptyField", sleep_duration)

    def swipe_task_rewards_screen(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeForceEventRewardsScreen", duration_ms=1000)
        sleep(settings[sleep_duration])

    def claim_force_event_rewards_by_positions(self, settings):
        self.press_force_event_tasks_button(settings)

        days_positions = settings["forceEventDaysBoxesPositions"]
        for day_position in days_positions:
            # Press the day
            self.press_location(
                day_position["x"],
                day_position["y"]
            )
            sleep(settings[SLEEP_SHORT])

            tasks_positions = settings["forceEventTasksBoxesPositions"]
            for tasks_position in tasks_positions:
                # Press the task group
                self.press_location(
                    tasks_position["x"],
                    tasks_position["y"]
                )
                sleep(settings[SLEEP_SHORT])

                for _ in range(2):
                    self.swipe_task_rewards_screen(settings)

                for _ in range(8):
                    self.press_force_event_task_reward_claim_button(settings)
                    self.press_force_event_task_empty_field(settings)

        shells_positions = settings["forceEventShellsPositions"]
        for shell_position in shells_positions:
            # Press the shell
            self.press_location(
                shell_position["x"],
                shell_position["y"]
            )
            sleep(settings[SLEEP_SHORT])
            self.press_force_event_task_empty_field(settings)

        self.press_force_event_transport_button(settings)

    def do_collect(self, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.claim_force_event_rewards_by_positions(settings)

    def run(self, shared):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect(shared)


class CollectingBot(EveningBonusesCollectingBot):
    def do_collect(self, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.press_close_banner_button(settings)
        self.do_tasks(settings, shared["models"]["task_icons"])
        self.process_resource_factory(settings)
        self.fill_leaf_cutters(settings)
        self.fill_feeding_ground(settings)
        self.hatch_special_ants(settings)
        self.get_bonuses(settings)
        self.donate_to_evolution(settings)
        self.hatch_ants(settings)
        self.claim_rewards(settings)
        self.read_mail(settings)
        self.hatch_insects(settings)

    def run(self, shared):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect(shared)


class TasksBot(MorningBonusesCollectingBot):
    def do_collect(self, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.press_close_banner_button(settings)
        self.do_tasks(settings, shared["models"]["task_icons"])
        self.process_resource_factory(settings)
        self.check_and_hatch_free_special_ant(settings)
        self.hatch_insects(settings)

    def run(self, shared):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect(shared)


class HatchingSpecialAntsBot(MorningBonusesCollectingBot):
    def hatch_special_ants_mass(self, settings):
        self.press_hatch_menu_button(settings)

        for _ in range(3):
            while True:
                self.press_hatch_special_ant_button(settings)
                image = self.get_screenshot(settings)
                cannot_hatch_egg = self.check_pixel_color(
                    image, settings, "hatchSpecialAntScreenColorPick", Colors.GRAY
                )
                if cannot_hatch_egg:
                    self.press_back_button(settings)
                    self.swipe_hatch_screen(settings)
                    break
                else:
                    self.press_hatch_special_ant_button(settings)
                    self.press_hatch_cross_button(settings)

        self.press_back_button(settings)

    def do_collect(self, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.hatch_special_ants_mass(settings)

    def run(self, shared):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect(shared)


class HatchingBot(MorningBonusesCollectingBot):
    def do_collect(self, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.hatch_ants(settings)

    def run(self, shared):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect(shared)
