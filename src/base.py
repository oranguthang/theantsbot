from time import sleep
from ppadb.client import Client

from src.logger import logger
from src.utils import ExtractText, ImageHandler

SLEEP_SHORT = "sleepShort"
SLEEP_MEDIUM = "sleepMedium"
SLEEP_LONG = "sleepLong"


class Action:
    ACTION_COLLECTING = "collecting"
    ACTION_MORNING = "morning"
    ACTION_WATER = "water"
    ACTION_HUNT = "hunt"
    ACTION_GATHER = "gather"
    ACTION_EVENING = "evening"
    ACTION_FORCE_EVENT = "force"
    ACTION_TASKS = "tasks"


class DeviceHandler:
    def __init__(self, devices_hosts):
        self.devices_hosts = [device.split(":") for device in devices_hosts]
        self.client = Client(host="127.0.0.1", port=5037)
        logger.info(f"Client version: {self.client.version()}")

    def connect_devices(self):
        for host, port in self.devices_hosts:
            self.client.remote_connect(host, int(port))
            self.client.device(f"{host}:{port}")

    def get_devices(self, skip_devices=()):
        connected_devices = []
        for idx, (host, port) in enumerate(self.devices_hosts):
            try:
                device = self.client.device(f"{host}:{port}")
                if device:
                    number = idx + 1
                    if number in skip_devices:
                        continue
                    device.number = number
                    name = f"Farm {number}"
                    device.name = name
                    logger.info(f"Connected device {name} {host}:{port}")
                    connected_devices.append(device)
            except RuntimeError:
                logger.warning(f"Skipped device {host}:{port}")

        if len(connected_devices) == 0:
            msg = "No devices attached"
            raise Exception(msg)

        logger.info(f"All devices are connected: {len(self.devices_hosts) == len(connected_devices)}")

        return connected_devices


class TheAntsBot:
    def __init__(self, device):
        self.device = device
        self.closed_less_active_alert = False

    def get_screenshot(self, settings=None, rectangle_name=None):
        image = self.device.screencap()
        logger.debug("Successfully get screenshot")

        if settings and rectangle_name:
            image = ImageHandler.crop_image(
                image,
                settings["rectangles"][rectangle_name]["x"],
                settings["rectangles"][rectangle_name]["y"],
                settings["rectangles"][rectangle_name]["h"],
                settings["rectangles"][rectangle_name]["w"]
            )

        debug = settings["debug"] if settings else False
        if debug:
            ImageHandler.save_to_file(image)

        return image

    def get_text_from_screenshot(self, image=None, settings=None, rectangle_name=None, char_whitelist=None):
        if image is None:
            image = self.get_screenshot(settings, rectangle_name)
        debug = settings["debug"] if settings else False
        image_threshold = ImageHandler.threshold(image, debug=debug)
        text = ExtractText.image_to_string(image_threshold, char_whitelist=char_whitelist)
        return text

    def get_text_boxes_from_screenshot(self, image=None, settings=None, rectangle_name=None, char_whitelist=None):
        if image is None:
            image = self.get_screenshot(settings, rectangle_name)
        debug = settings["debug"] if settings else False
        image_threshold = ImageHandler.threshold(image, debug=debug)
        boxes = ExtractText.image_to_boxes(image_threshold, char_whitelist=char_whitelist)
        return boxes

    def check_pixel_color(self, image, settings, position, color):
        if image is None:
            image = self.get_screenshot(settings)

        if isinstance(position, str):
            x = settings["positions"][position]["x"]
            y = settings["positions"][position]["y"]
        else:
            x = position["x"]
            y = position["y"]

        return ImageHandler.check_pixel_color(image, x, y, color)

    def type_text(self, text):
        self.device.shell(f'input text "{text}"')

    def type_backspace(self):
        self.device.shell("input keyevent 67")

    def press_location(self, x, y):
        self.device.shell(f"input tap {x} {y}")

    def press_location_and_type(self, x, y, text, backspace_count=0):
        self.press_location(x, y)
        for _ in range(backspace_count):
            self.type_backspace()
        self.type_text(text)

    def swipe_location(self, start_x, start_y, end_x, end_y, duration_ms=300):
        self.device.shell(f"input swipe {start_x} {start_y} {end_x} {end_y} {duration_ms}")

    def swipe(self, settings, swipe_name, duration_ms):
        self.swipe_location(
            settings["swipes"][swipe_name]["x1"], settings["swipes"][swipe_name]["y1"],
            settings["swipes"][swipe_name]["x2"], settings["swipes"][swipe_name]["y2"],
            duration_ms=duration_ms
        )

    def press_position(self, settings, position_name, sleep_duration, multiplier=1):
        self.press_location(settings["positions"][position_name]["x"], settings["positions"][position_name]["y"])
        if sleep_duration:
            sleep(settings[sleep_duration] * multiplier)

    def press_center_screen(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "centerScreen", sleep_duration)

    def press_back_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "backButton", sleep_duration)

    def press_free_space_bottom(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "freeSpaceBottom", sleep_duration)

    def press_alliance_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "allianceButton", sleep_duration)
        if not self.closed_less_active_alert:
            self.press_position(settings, "allianceLessActiveDontShowAgainCheck", sleep_duration=SLEEP_SHORT)
            self.press_position(settings, "allianceLessActiveCancelButton", sleep_duration=SLEEP_SHORT)
            self.closed_less_active_alert = True

    def press_world_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "worldButton", sleep_duration, multiplier=3)

    def press_search_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "searchButton", sleep_duration)

    def press_search_go_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "searchGoButton", sleep_duration)

    def press_search_wild_creatures_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "searchWildCreaturesButton", sleep_duration)

    def press_search_resource_tiles_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "searchResourceTilesButton", sleep_duration)

    def press_search_coords_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "searchCoordsButton", sleep_duration)

    def press_search_coords_go_button(self, settings, sleep_duration=SLEEP_SHORT):
        self.press_position(settings, "searchCoordsGoButton", sleep_duration)

    def press_march_button(self, settings, sleep_duration=SLEEP_MEDIUM):
        self.press_position(settings, "marchButton", sleep_duration)

    def run(self, shared):
        raise NotImplementedError("This method should be implemented")
