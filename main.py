from multiprocessing import Pool

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

DEVICES_LIST = [
    ("Farm 1", "localhost", 5555),
    ("Farm 2", "localhost", 5565),
    ("Farm 3", "localhost", 5615),
    ("Farm 4", "localhost", 5625),
    ("Farm 5", "localhost", 5575),
    ("Farm 6", "localhost", 5635),
    ("Farm 7", "localhost", 5645),
    ("Farm 8", "localhost", 5655),
]


if __name__ == "__main__":
    # Check if adb server is running
    if "adb.exe" not in (p.name() for p in psutil.process_iter()):
        adb = subprocess.Popen([ADB_PATH, "devices"])
        sleep(15)  # Wait for 15 secs

    device_handler = DeviceHandler(DEVICES_LIST)
    device_handler.connect_devices()
    current_devices = device_handler.get_devices()

    settings = Settings.load_settings()
    if Settings.check_enabled(settings):
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
                with Pool(pool_size) as pool:
                    pool.map(bot_class.run, list_of_bots)

        logger.info("The job is done! See you soon!")
