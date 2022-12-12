import random
import re
from datetime import datetime
from time import sleep

from models.task_icons.model import TaskIconTypes
from src.base import TheAntsBot, SLEEP_SHORT, SLEEP_MEDIUM, SLEEP_LONG
from src.logger import logger
from src.settings import Settings
from src.utils import (THRESHOLD_DIVIDER, Colors, ImageHandler, CommonTemplates,
                       ButtonTemplates, HeaderTemplates, EventTemplates)


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

    def press_workers_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "workersButton", sleep_duration)

    def press_exploration_queue(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "explorationQueueBar", sleep_duration)

    def press_first_ant_explore_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "firstAntExploreButton", sleep_duration)

    def press_start_exploration_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "startExplorationButton", sleep_duration)

    def press_events_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "eventsButton", sleep_duration)

    def press_todo_list_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "todoListButton", sleep_duration)

    def press_todo_list_left_tab(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "todoListLeftTab", sleep_duration)

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

    def press_leaf_cutter_supply_button(self, settings, sleep_duration=SLEEP_MEDIUM):
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

    def swipe_benefits_rewards_down(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeBenefitsRewardsDown", duration_ms=500)
        sleep(settings[sleep_duration])

    def swipe_events_screen_down(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeEventsScreenDown", duration_ms=1000)
        sleep(settings[sleep_duration])

    def swipe_events_screen_up(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeEventsScreenUp", duration_ms=1000)
        sleep(settings[sleep_duration])

    def swipe_todo_list_down(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeTodoListDown", duration_ms=1000)
        sleep(settings[sleep_duration])

    def swipe_todo_list_up(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeTodoListUp", duration_ms=1000)
        sleep(settings[sleep_duration])

    def find_event(self, settings, event_templates):
        self.press_events_button(settings)

        for _ in range(2):
            self.swipe_events_screen_up(settings)

        found_event = False
        for _ in range(3):
            for template in event_templates:
                found_event = self.find_and_press_template(settings, template, "eventsScreen")
                if found_event:
                    break
            if found_event:
                break
            else:
                self.swipe_events_screen_down(settings)

        if not found_event:
            self.press_back_button(settings)

        return found_event

    def find_todo_task(self, settings, task_template):
        self.press_todo_list_button(settings)
        self.press_todo_list_left_tab(settings)

        found_task = False
        for _ in range(3):
            found_task = self.find_and_press_template(settings, task_template, "todoListScreen", shift_x=405)
            if found_task:
                break
            else:
                self.swipe_todo_list_down(settings)

        if not found_task:
            self.press_back_button(settings)

        return found_task

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

    def do_duel(self, settings, duel_name):
        self.press_position(settings, f"{duel_name}Bar", sleep_duration=SLEEP_SHORT)
        self.do_duel_deploy_troops(settings)

        # Close alert, if we are promoted to higher league
        self.press_free_space_bottom(settings)

        opponents_positions = settings[f"{duel_name}OpponentPositions"]
        is_first_step = True
        while True:
            self.press_position(settings, "duelChallengeButton", sleep_duration=SLEEP_SHORT)
            image = self.get_screenshot(settings)
            is_button_gray = self.check_pixel_color(image, settings, f"{duel_name}OpponentButtonColorPick", Colors.GRAY)
            if is_button_gray:
                self.press_back_button(settings)
                break

            position = random.choice(opponents_positions)
            self.press_position_by_coordinates(settings, position, sleep_duration=SLEEP_SHORT)
            if is_first_step:
                self.do_duel_deploy_troops(settings, press_back_button=False)
                is_first_step = False
            self.press_position(settings, "duelDepartButton", sleep_duration=SLEEP_SHORT)
            self.press_position(settings, "duelSkipButton", sleep_duration=SLEEP_SHORT)
            self.press_back_button(settings)

        self.press_position(settings, "duelRewardsButton", sleep_duration=SLEEP_SHORT)
        # It's the same position for Claim rewards Button
        self.press_position(settings, "duelDepartButton", sleep_duration=SLEEP_SHORT)
        self.press_position(settings, "duelRewardsClaimButton", sleep_duration=SLEEP_SHORT)
        # Close Claim rewards window
        self.press_position(settings, "duelDepartButton", sleep_duration=SLEEP_SHORT)

        self.press_back_button(settings)
        self.press_back_button(settings)

    def do_duel_of_queens(self, settings):
        if settings["duelOfQueensEnabled"] is True:
            self.do_duel(settings, "duelOfQueens")
        if settings["duelOfSpecialAntsEnabled"] is True:
            self.do_duel(settings, "duelOfSpecialAnts")

        self.press_back_button(settings)

    def do_get_duel_of_queens_reward(self, settings):
        if settings["duelOfQueensEnabled"] is True:
            self.press_position(settings, "duelOfQueensBar", sleep_duration=SLEEP_SHORT)
            # Close alert, if we are promoted to higher league
            self.press_free_space_bottom(settings)

            self.press_position(settings, "duelRewardsButton", sleep_duration=SLEEP_SHORT)
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
        i = 0
        position = cutters_positions[i]
        while True:
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

            # Check if all workers are busy
            found_header = self.find_template(settings, HeaderTemplates.WORKER_ANTS, "workerAntsHeaderArea")
            if found_header:
                self.press_back_button(settings)
                sleep(settings[SLEEP_MEDIUM])
                position["x"] = 360
            else:
                i += 1
                if i >= len(cutters_positions):
                    break
                position = cutters_positions[i]

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

    def process_help_and_gifts(self, settings):
        rectangle_name = "helpAndGiftsArea"
        self.find_and_press_template(settings, CommonTemplates.HELP, rectangle_name)

        if self.find_and_press_template(settings, CommonTemplates.GIFTS, rectangle_name):
            self.press_position(settings, "giftsClaimButton", sleep_duration=SLEEP_SHORT)
            self.press_back_button(settings)
            self.press_back_button(settings)

    def get_benefits_bonuses(self, settings):
        self.press_position(settings, "benefitsIcon", sleep_duration=SLEEP_SHORT)
        rectangle_name = "benefitsTopBar"

        templates = [
            CommonTemplates.WILD_HUNT,
            CommonTemplates.THRIVING_ANTHILL,
            CommonTemplates.COLONY_LEADER,
            CommonTemplates.MASS_DEVELOPMENT,
            CommonTemplates.PROJECT_GUARDIAN,
            CommonTemplates.GRANARY_ENRICHMENT,
        ]
        for template in templates:
            rectangle = self.find_and_press_template(settings, template, rectangle_name)
            if rectangle:
                self.swipe_benefits_rewards_down(settings)

                for _ in range(8):
                    # self.press_position(settings, "benefitsClaimButton", sleep_duration=SLEEP_SHORT)
                    found = self.find_and_press_template(settings, ButtonTemplates.EXPLORE_CLAIM, "benefitsButtons")
                    if not found:
                        break
                    self.press_position(settings, "benefitsEmptySpace", sleep_duration=SLEEP_SHORT)

        self.press_back_button(settings)

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

    def mutate_ants(self, settings):
        if not settings["hatchAnts"]:
            return
        config = settings["farmHatchingConfig"][str(self.device.number)]

        self.swipe_screen_to_troop_camp(settings)

        found_speedup = self.find_template(settings, CommonTemplates.SPEEDUP, "troopCampIconsArea")
        if not found_speedup:
            found_icon = self.find_and_press_template(settings, CommonTemplates.SOLDIER_ANTS, "troopCampIconsArea")
            if found_icon:
                found_header = self.find_template(settings, HeaderTemplates.TROOP_CAMP, "screenMenuHeading")
                if found_header:
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

                    self.press_location_and_type(settings, "troopCampInputAmountField", config["mutation_amount"],
                                                 backspace_count=6)
                    self.press_position(settings, "troopCampStartMutationButton", sleep_duration=SLEEP_SHORT)
                    self.press_back_button(settings)
                    self.press_back_button(settings)

        self.press_world_button(settings)
        self.press_world_button(settings)

    def hatch_ants(self, settings):
        if not settings["hatchAnts"]:
            return
        config = settings["farmHatchingConfig"][str(self.device.number)]

        hatching_nests = settings["hatchNestPositions"]
        for nest_position in hatching_nests:
            # Press nest location
            self.press_location(nest_position["x"], nest_position["y"])
            sleep(settings[SLEEP_SHORT])

            found_speedup = self.find_template(settings, CommonTemplates.HATCH_ANTS_SPEEDUP, "hatchNestIconsArea")
            if not found_speedup:
                # Press hatch icon
                self.press_location(nest_position["x1"], nest_position["y1"])
                sleep(settings[SLEEP_MEDIUM])

                self.press_location_and_type(settings, "hatchAntsInputAmountField", config["hatch_amount"],
                                             backspace_count=6)
                self.press_position(settings, "hatchAntsStartButton", sleep_duration=SLEEP_SHORT)
                self.press_back_button(settings)

        self.press_world_button(settings)
        self.press_world_button(settings)

    def hatch_special_ants(self, settings):
        if not settings["hatchSpecialAnts"]:
            return

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
        if not settings["hatchSpecialAnts"]:
            return

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

        # Process right farms
        self.swipe_screen_to_hatch_insects(settings)
        right_farms = positions[7:10]
        self.process_termite_farms(settings, right_farms)
        self.press_world_button(settings)
        self.press_world_button(settings)

        if not settings["hatchInsects"]:
            return

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

            is_collected_insect = self.find_template(settings, CommonTemplates.INSECT_STAR_UP, "insectScreenBottomBar")
            if is_collected_insect:
                # If we collected a hatched insect, then we need to return
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

    def explore(self, settings):
        self.press_workers_button(settings)
        self.press_exploration_queue(settings)

        workers_count = settings["farmWorkersCount"][str(self.device.number)]
        # Claim rewards
        for _ in range(workers_count):
            found = self.find_and_press_template(settings, ButtonTemplates.EXPLORE_CLAIM,
                                                 "workerAntsScreen", threshold=0.8)
            if not found:
                break
            # self.press_first_ant_explore_button(settings)
            self.press_back_button(settings)

        # Start new exploration
        for _ in range(workers_count):
            # self.press_first_ant_explore_button(settings)
            found = self.find_and_press_template(settings, ButtonTemplates.EXPLORE,
                                                 "workerAntsScreen", threshold=0.8)
            if not found:
                break
            self.press_start_exploration_button(settings)

        self.press_back_button(settings)

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

        recommended_evolution = settings["allianceEvolutionsPriority"][tab_name]
        if recommended_evolution - 1 > len(evolutions_positions):
            recommended_evolution = len(evolutions_positions)
        evolutions_positions.insert(0, evolutions_positions.pop(recommended_evolution - 1))

        resources_completed = False
        diamonds_completed = False
        for position in evolutions_positions:
            if resources_completed and diamonds_completed:
                break

            self.press_location(
                position["x"],
                position["y"]
            )
            sleep(settings[SLEEP_MEDIUM])

            image = self.get_screenshot(settings)
            if donate_resources and not resources_completed:
                button_is_gray = self.check_pixel_color(
                    image, settings, "allianceEvolutionDonateResourceButtonColorPick", Colors.GRAY
                )
                if not button_is_gray:
                    for _ in range(25):
                        self.press_alliance_evolution_donate_resources_button(settings)

                # if button is gray, donation is completed; if not, the same
                resources_completed = True

            if donate_diamonds and not diamonds_completed:
                button_is_gray = self.check_pixel_color(
                    image, settings, "allianceEvolutionDonateDiamondButtonColorPick", Colors.GRAY
                )
                if not button_is_gray:
                    for _ in range(10):
                        self.press_alliance_evolution_donate_diamonds_button(settings)
                else:
                    diamonds_completed = True

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
        self.process_help_and_gifts(settings)
        self.explore(settings)
        self.do_tasks(settings, shared["models"]["task_icons"])
        self.process_resource_factory(settings)
        self.fill_leaf_cutters(settings)
        self.fill_feeding_ground(settings)
        self.get_bonuses(settings)
        self.hatch_special_ants(settings)
        self.donate_to_evolution(settings)
        self.mutate_ants(settings)
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
        self.process_help_and_gifts(settings)
        self.explore(settings)
        self.do_tasks(settings, shared["models"]["task_icons"])
        self.get_benefits_bonuses(settings)
        self.process_resource_factory(settings)
        self.fill_leaf_cutters(settings)
        self.fill_feeding_ground(settings)
        self.donate_to_evolution(settings, donate_diamonds=False)
        self.mutate_ants(settings)
        self.hatch_ants(settings)
        self.claim_rewards(settings)
        self.read_mail(settings)
        self.hatch_insects(settings)

    def run(self, shared):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect(shared)


class ForceEventBonusesCollectingBot(MorningBonusesCollectingBot):
    def press_force_event_tasks_tab(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "forceEventTasksTab", sleep_duration)

    def press_force_event_transport_tab(self, settings, sleep_duration=SLEEP_SHORT, multiplier=1):
        self.press_position(settings, "forceEventTransportTab", sleep_duration, multiplier)

    def press_force_event_transport_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position_and_hold(settings, "forceEventTransportButton", sleep_duration, duration_ms=5000)

    def press_force_event_task_reward_claim_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "forceEventTaskRewardClaimButton", sleep_duration)

    def press_force_event_task_empty_field(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "forceEventTaskEmptyField", sleep_duration)

    def swipe_task_rewards_screen(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeForceEventRewardsScreen", duration_ms=1000)
        sleep(settings[sleep_duration])

    def swipe_normal_rewards_screen(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeForceEventNormalRewards", duration_ms=500)
        sleep(settings[sleep_duration])

    def claim_force_event_rewards_by_positions(self, settings):
        self.press_force_event_tasks_tab(settings)

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

        self.press_force_event_transport_tab(settings, sleep_duration=SLEEP_MEDIUM, multiplier=3)
        self.press_force_event_transport_button(settings)

        while True:
            # Wait for all fragments to be transferred
            sleep(settings[SLEEP_LONG])
            found_button = self.find_template(settings, ButtonTemplates.TRANSPORT_PAUSE,
                                              "forceEventTransportArea", threshold=0.8)
            if not found_button:
                break

        # Claim normal rewards from 1 to 20
        rewards_positions = settings["forceEventNormalRewardsPositions"]
        for _ in range(10):
            for position in rewards_positions:
                # Press the reward
                self.press_location(
                    position["x"],
                    position["y"]
                )
                sleep(settings[SLEEP_SHORT])
                self.press_force_event_transport_tab(settings)

            self.swipe_normal_rewards_screen(settings)

    def do_collect(self, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        found_event = self.find_event(settings, [EventTemplates.FORCE_OF_TIDES])
        if not found_event:
            return

        self.claim_force_event_rewards_by_positions(settings)

    def run(self, shared):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect(shared)


class TasksBot(MorningBonusesCollectingBot):
    def do_collect(self, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        self.press_close_banner_button(settings)
        self.process_help_and_gifts(settings)
        self.do_tasks(settings, shared["models"]["task_icons"])
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

        self.press_world_button(settings)
        self.press_world_button(settings)

        self.mutate_ants(settings)
        self.hatch_ants(settings)

    def run(self, shared):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect(shared)


class VIPStoreBot(MorningBonusesCollectingBot):
    def swipe_vip_store_screen_down(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeVIPStoreScreenDown", duration_ms=500)
        sleep(settings[sleep_duration])

    def swipe_vip_store_slider(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeVIPStoreSlider", duration_ms=500)
        sleep(settings[sleep_duration])

    def buy_vip_store(self, settings):
        level = settings["farmVIPLevels"][str(self.device.number)]
        plates_sequence = settings["VIPStorePlatesSequence"][str(level)]
        plates_positions = settings["VIPStorePlatesPositions"]

        for plate_number in plates_sequence:
            position = plates_positions[plate_number - 1]
            self.press_location(position["x"], position["y"])
            sleep(settings[SLEEP_SHORT])

            # Move slider
            self.swipe_vip_store_slider(settings)

            # Purchase item
            self.press_position(settings, "VIPStorePurchaseButton", sleep_duration=SLEEP_SHORT)
            self.press_position(settings, "VIPStorePurchaseConfirmButton", sleep_duration=SLEEP_SHORT)
            self.press_back_button(settings)

    def do_collect(self, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        found_event = self.find_event(settings, [EventTemplates.VIP_STORE])
        if not found_event:
            return

        self.buy_vip_store(settings)

    def run(self, shared):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect(shared)


class StoreBot(MorningBonusesCollectingBot):
    ITEMS_MAPPING = {
        "cell_fluid": CommonTemplates.CELL_FLUID,
        "cell_nucleus": CommonTemplates.CELL_NUCLEUS,
        "genetic_factor_i": CommonTemplates.GENETIC_FACTOR_I,
        "genetic_factor_ii": CommonTemplates.GENETIC_FACTOR_II,
        "genetic_factor_iii": CommonTemplates.GENETIC_FACTOR_III,
        "dna": CommonTemplates.DNA,
        "advanced_dna": CommonTemplates.ADVANCED_DNA,
        "germ": CommonTemplates.GERM,
        "inducible_enzyme": CommonTemplates.INDUCIBLE_ENZYME,
        "fungus_nutrient_i": CommonTemplates.FUNGUS_NUTRIENT_I,
        "fungus_nutrient_ii": CommonTemplates.FUNGUS_NUTRIENT_II,
        "hypha": CommonTemplates.HYPHA,
        "special_hypha": CommonTemplates.SPECIAL_HYPHA
    }

    def press_left_tab(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "storeLeftTab", sleep_duration)

    def press_right_tab(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "storeLeftTab", sleep_duration)

    def swipe_store_screen_down(self, settings, sleep_duration=SLEEP_SHORT):
        self.swipe(settings, "swipeStoreScreenDown", duration_ms=500)
        sleep(settings[sleep_duration])

    def do_store(self, settings, store_name):
        icon_name = f"{store_name}Icon"
        self.press_position(settings, icon_name, sleep_duration=SLEEP_SHORT)

        if store_name in ("epopticFungiStore", "duelStore"):
            self.press_left_tab(settings)

        for _ in range(2):
            self.swipe_store_screen_down(settings)

        item_names = settings["storeBuyItems"][store_name]
        for item_name in item_names:
            item_template = self.ITEMS_MAPPING[item_name]
            found = self.find_and_press_template(settings, item_template, "storeItemsArea", threshold=0.8, shift_y=170)
            if found:
                self.press_position(settings, "storeItemClaimButton", sleep_duration=SLEEP_SHORT)
                self.press_position(settings, "storeItemClaimConfirmButton", sleep_duration=SLEEP_SHORT)
                self.press_position(settings, icon_name, sleep_duration=SLEEP_SHORT)

    def do_collect(self, shared):
        settings = Settings.load_settings()

        if not Settings.check_enabled(settings):
            return

        found_task = self.find_todo_task(settings, CommonTemplates.DUEL_STORE)
        if not found_task:
            return

        self.do_store(settings, "epopticFungiStore")
        self.do_store(settings, "duelStore")
        self.do_store(settings, "mineStore")
        self.do_store(settings, "specialAntDuelStore")
        self.press_back_button(settings)

    def run(self, shared):
        logger.info(f"Ready to run the collecting bot on {self.device.name}")

        self.do_collect(shared)
