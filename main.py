import os
from multiprocessing import Pool, Lock

import numpy as np
import psutil
import subprocess
from time import sleep

from src.base import DeviceHandler, Action
from src.gatherer import GatheringBot
from src.hunter import HuntingBot
from src.waterer import WateringBot
from src.collector import MorningBonusesCollectingBot, EveningBonusesCollectingBot
from src.logger import logger
from src.settings import Settings

CORE_NUMBER = 4

ADB_PATH = "C:\\Android\\adb.exe"


def init_lock(lock_obj):
    global lock
    lock = lock_obj


def main():
    # Check if adb server is running
    if "adb.exe" not in (p.name() for p in psutil.process_iter()):
        subprocess.Popen([ADB_PATH, "devices"])
        sleep(15)  # Wait for 15 secs

    settings = Settings.load_settings()
    if Settings.check_enabled(settings):
        if settings["debug"]:
            os.makedirs("screenshots", exist_ok=True)

        device_handler = DeviceHandler(settings["devices"])
        device_handler.connect_devices()
        current_devices = device_handler.get_devices(skip_devices=settings["disabledFarms"])

        strategy_num = settings["strategyNum"]
        for action in settings["strategies"][str(strategy_num)]:
            if action == Action.ACTION_WATER:
                bot_class = WateringBot
            elif action == Action.ACTION_MORNING:
                bot_class = MorningBonusesCollectingBot
            elif action == Action.ACTION_EVENING:
                bot_class = EveningBonusesCollectingBot
            elif action == Action.ACTION_GATHER:
                bot_class = GatheringBot
            else:
                # Hunting is default class
                action = Action.ACTION_HUNT
                bot_class = HuntingBot

            list_of_bots = [bot_class(device) for device in current_devices]

            if action == Action.ACTION_HUNT:
                async_run = settings["huntAsyncRun"]
                pool_size = settings["huntPoolSize"]
                if not async_run:
                    # Running bots one by one
                    bot_class.run_bots(list_of_bots)
                else:
                    # Running bots simultaneously
                    with Pool(pool_size) as pool:
                        pool.map(bot_class.run_bots, np.array_split(list_of_bots, pool_size))
            else:
                pool_size = len(list_of_bots)
                lock_obj = Lock()
                with Pool(pool_size, initializer=init_lock, initargs=(lock_obj,)) as pool:
                    pool.map(bot_class.run, list_of_bots)

        logger.info("The job is done! See you soon!")


if __name__ == "__main__":
    main()
