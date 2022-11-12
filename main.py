import os
import numpy as np
from multiprocessing import Pool, Manager

from models.task_icons.model import TaskIconsModel
from src.base import DeviceHandler, Action
from src.gatherer import GatheringBot
from src.hunter import HuntingBot
from src.waterer import WateringBot
from src.collector import (MorningBonusesCollectingBot, EveningBonusesCollectingBot,
                           CollectingBot, ForceEventBonusesCollectingBot, TasksBot,
                           HatchingBot, HatchingSpecialAntsBot)
from src.logger import logger
from src.settings import Settings


def exec_runner(func, args):
    result = func(*args)
    return result


def runner(args):
    return exec_runner(*args)


def main():
    settings = Settings.load_settings()
    if Settings.check_enabled(settings):
        device_handler = DeviceHandler(settings, skip_devices=settings["disabledFarms"])
        device_handler.connect_devices()
        current_devices = device_handler.get_devices()

        if settings["debug"]:
            os.makedirs("screenshots", exist_ok=True)

        task_icons_model = TaskIconsModel(root_dir=os.path.join("models", "task_icons"))

        strategy_num = settings["strategyNum"]
        for action in settings["strategies"][str(strategy_num)]:
            run_method = "run"
            pool_size = len(current_devices)
            if action == Action.ACTION_WATER:
                bot_class = WateringBot
            elif action == Action.ACTION_MORNING:
                bot_class = MorningBonusesCollectingBot
            elif action == Action.ACTION_EVENING:
                bot_class = EveningBonusesCollectingBot
            elif action == Action.ACTION_COLLECTING:
                bot_class = CollectingBot
            elif action == Action.ACTION_FORCE_EVENT:
                bot_class = ForceEventBonusesCollectingBot
            elif action == Action.ACTION_TASKS:
                bot_class = TasksBot
            elif action == Action.ACTION_HATCH_SPECIAL:
                bot_class = HatchingSpecialAntsBot
            elif action == Action.ACTION_HATCH:
                bot_class = HatchingBot
            elif action == Action.ACTION_GATHER:
                pool_size = settings["gatherPoolSize"]
                bot_class = GatheringBot
            else:
                # Hunting is default class
                action = Action.ACTION_HUNT
                bot_class = HuntingBot
                run_method = "run_bots"
                pool_size = settings["huntPoolSize"]

            list_of_bots = [bot_class(device) for device in current_devices]
            if action == Action.ACTION_HUNT:
                list_of_bots = np.array_split(list_of_bots, pool_size)

            manager = Manager()
            shared_data = manager.dict()
            shared_data["models"] = manager.dict()
            shared_data["models"]["task_icons"] = task_icons_model

            func = getattr(bot_class, run_method)
            tasks = [(func, (bot, shared_data)) for bot in list_of_bots]
            with Pool(pool_size) as pool:
                pool.map(runner, tasks)

        logger.info("The job is done! See you soon!")


if __name__ == "__main__":
    main()
