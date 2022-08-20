import os
from multiprocessing import Pool, Manager

import numpy as np
import psutil
import subprocess
from time import sleep

from models.task_icons.model import TaskIconsModel
from src.base import DeviceHandler, Action
from src.gatherer import GatheringBot
from src.hunter import HuntingBot
from src.waterer import WateringBot
from src.collector import MorningBonusesCollectingBot, EveningBonusesCollectingBot, CollectingBot
from src.logger import logger
from src.settings import Settings

CORE_NUMBER = 4

ADB_PATH = "C:\\Android\\adb.exe"


def exec_runner(func, args):
    result = func(*args)
    return result


def runner(args):
    return exec_runner(*args)


def main():
    # Check if adb server is running
    if "adb.exe" not in (p.name() for p in psutil.process_iter()):
        subprocess.Popen([ADB_PATH, "devices"])
        sleep(15)  # Wait for 15 secs

    settings = Settings.load_settings()
    if Settings.check_enabled(settings):
        if settings["debug"]:
            os.makedirs("screenshots", exist_ok=True)

        task_icons_model = TaskIconsModel(root_dir=os.path.join("models", "task_icons"))

        device_handler = DeviceHandler(settings["devices"])
        device_handler.connect_devices()
        current_devices = device_handler.get_devices(skip_devices=settings["disabledFarms"])

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
            elif action == Action.ACTION_GATHER:
                bot_class = GatheringBot
                pool_size = 1
                sleep(180)  # FIXME: Dirty hack - wait for all troops to return
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
            shared_data["watered_users"] = manager.dict()
            shared_data["models"] = manager.dict()
            shared_data["models"]["task_icons"] = task_icons_model

            func = getattr(bot_class, run_method)
            tasks = [(func, (bot, shared_data)) for bot in list_of_bots]
            with Pool(pool_size) as pool:
                pool.map(runner, tasks)

        logger.info("The job is done! See you soon!")


if __name__ == "__main__":
    main()
