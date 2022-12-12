import os
import uuid
from enum import Enum

from pytesseract import pytesseract, Output
import cv2
import numpy as np

pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
DEFAULT_CONFIG = (
    r"--oem 3 "
    r"--psm 6 "
)
WITH_WHITELIST = (
    r"-c tessedit_char_whitelist={char_whitelist} "
)
DEFAULT_CHAR_WHITELIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/"

THRESHOLD_DIVIDER = 2.5


class Colors:
    BLACK = "black"
    GRAY = "gray"
    BLUE = "blue"
    RED = "red"


class BaseTemplates(Enum):
    def get_path(self):
        if hasattr(self.__class__, "_folder_name"):
            return os.path.join(self.__class__._folder_name.value, self.value)
        else:
            raise Exception(f"Class {self.__class__} should contain '_folder_name' value")


class CommonTemplates(BaseTemplates):
    _folder_name = ""

    CROSS = "cross_icon.png"
    VISIT_ANTHILL = "visit_anthill.png"
    RECOMMENDED_ALLIANCE = "recommended_alliance.png"
    WILD_HUNT = "wild_hunt.png"
    THRIVING_ANTHILL = "thriving_anthill.png"
    COLONY_LEADER = "colony_leader.png"
    MASS_DEVELOPMENT = "mass_development.png"
    PROJECT_GUARDIAN = "project_guardian.png"
    GRANARY_ENRICHMENT = "granary_enrichment.png"
    HELP = "help.png"
    GIFTS = "gifts.png"
    SOLDIER_ANTS = "soldier_ants.png"
    SPEEDUP = "speedup.png"
    HATCH_ANTS_SPEEDUP = "hatch_ants_speedup.png"
    FIND_EXOTIC_PEA = "find_exotic_pea.png"
    INSECT_STAR_UP = "insect_star_up.png"
    CELL_FLUID = "cell_fluid.png"
    CELL_NUCLEUS = "cell_nucleus.png"
    GENETIC_FACTOR_I = "genetic_factor_i.png"
    GENETIC_FACTOR_II = "genetic_factor_ii.png"
    GENETIC_FACTOR_III = "genetic_factor_iii.png"
    DNA = "DNA.png"
    ADVANCED_DNA = "advanced_DNA.png"
    GERM = "germ.png"
    INDUCIBLE_ENZYME = "inducible_enzyme.png"
    FUNGUS_NUTRIENT_I = "fungus_nutrient_i.png"
    FUNGUS_NUTRIENT_II = "fungus_nutrient_ii.png"
    HYPHA = "hypha.png"
    SPECIAL_HYPHA = "special_hypha.png"
    DUEL_STORE = "duel_store_icon.png"


class HeaderTemplates(BaseTemplates):
    _folder_name = "headers"

    MARCH_TROOPS = "march_troops.png"
    TROOP_CAMP = "troop_camp.png"
    WORKER_ANTS = "worker_ants.png"


class ButtonTemplates(BaseTemplates):
    _folder_name = "buttons"

    TRANSPORT_PAUSE = "transport_pause.png"
    SPEEDUP = "speedup.png"
    EXPLORE = "explore.png"
    EXPLORE_CLAIM = "explore_claim.png"
    BENEFITS_CLAIM = "benefits_claim.png"


class EventTemplates(BaseTemplates):
    _folder_name = "events"

    FORCE_OF_TIDES = "force_of_tides.png"
    VIP_STORE = "vip_store.png"


class ExtractText:
    @staticmethod
    def image_to_string(image, char_whitelist=None, custom_config=None):
        if custom_config:
            config = custom_config
        else:
            config = DEFAULT_CONFIG
        if char_whitelist:
            config += WITH_WHITELIST.format(char_whitelist=char_whitelist)

        return pytesseract.image_to_string(image, config=config)

    @staticmethod
    def image_to_boxes(image, char_whitelist=None, custom_config=None):
        if custom_config:
            config = custom_config
        else:
            config = DEFAULT_CONFIG
        if char_whitelist:
            config += WITH_WHITELIST.format(char_whitelist=char_whitelist)

        d = pytesseract.image_to_data(image, output_type=Output.DICT, config=config)
        n_boxes = len(d['level'])
        results = []

        if n_boxes <= 1:
            return results

        x_p, y_p, t_p = d['left'][0], d['top'][0], d['text'][0]
        for i in range(1, n_boxes):
            x, y, t = d['left'][i], d['top'][i], d['text'][i]
            if x > x_p and y_p - 10 < y < y_p + 10:
                t = t_p + ' ' + t
            else:
                results.append((x_p, y_p, t_p))
            x_p, y_p, t_p = x, y, t

        return results


class ImageHandler:
    @staticmethod
    def decode_image(image):
        if not isinstance(image, np.ndarray):
            image = np.frombuffer(image, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image

    @staticmethod
    def save_to_file(image, filename=None):
        image = ImageHandler.decode_image(image)
        if not filename:
            filename = f"{str(uuid.uuid4())}.jpg"
        cv2.imwrite(os.path.join("screenshots", filename), image)

    @staticmethod
    def threshold(image, debug):
        if not isinstance(image, np.ndarray):
            image = np.frombuffer(image, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        img_resized = cv2.resize(image, (0, 0), fx=2.5, fy=2.5)
        ret, thresh = cv2.threshold(img_resized, 80, 255, cv2.THRESH_BINARY)

        if debug:
            ImageHandler.save_to_file(thresh)

        return thresh

    @staticmethod
    def check_pixel_color(image, x, y, color, threshold=10):
        image = ImageHandler.decode_image(image)

        b, g, r = image[y, x]
        if color in (Colors.GRAY, Colors.BLACK):
            # if std of colors less than 4.0, the pixel is near black or gray
            return np.std([b, g, r]) < 4.0
        elif color == Colors.BLUE:
            # if blue channel is more than green and red, the pixel is near blue
            return b > g and b > r and (2 * b - g - r) > threshold
        elif color == Colors.RED:
            # if red channel is more than green and blue, the pixel is near red
            return r > g and r > b and (2 * r - g - b) > threshold

    @staticmethod
    def check_pixel_color_exact(image, x, y, color, threshold=10):
        image = ImageHandler.decode_image(image)

        b, g, r = image[y, x]
        b1, g1, r1 = color
        t = threshold
        return b1 - t < b < b1 + t and g1 - t < g < g1 + t and r1 - t < r < r1 + t

    @staticmethod
    def crop_image(image, x, y, h, w):
        image = ImageHandler.decode_image(image)

        img_cropped = image[y:y + h, x:x + w]
        return img_cropped

    @staticmethod
    def get_circles(image, hough_blur_radius=5, output_blur_radius=3, min_dist=50,
                    hough_param1=50, hough_param2=50, min_radius=20, max_radius=40, new_size=None):
        image = ImageHandler.decode_image(image)

        img_output = cv2.medianBlur(image, output_blur_radius)
        img_output_gray = cv2.cvtColor(img_output, cv2.COLOR_BGR2GRAY)

        img_hough = cv2.medianBlur(image, hough_blur_radius)
        img_hough_gray = cv2.cvtColor(img_hough, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(
            img_hough_gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=min_dist,
            param1=hough_param1,
            param2=hough_param2,  # Smaller value -> more false circles
            minRadius=min_radius,
            maxRadius=max_radius
        )

        if circles is None:
            return []

        circles = np.uint16(np.around(circles))
        results = []
        for circle in circles[0, :]:
            x = circle[0]
            y = circle[1]
            r = circle[2]
            rect_x = x - r
            rect_y = y - r
            img_circle = img_output_gray[rect_y:(rect_y + 2 * r), rect_x:(rect_x + 2 * r)]

            if isinstance(new_size, (list, tuple)) and len(new_size) == 2:
                img_circle = cv2.resize(img_circle, new_size, interpolation=cv2.INTER_AREA)

            results.append({
                "x": x,
                "y": y,
                "image": img_circle,
            })

        return results

    @staticmethod
    def match_template(img_rgb, template, threshold=0.8):
        img_rgb = ImageHandler.decode_image(img_rgb)
        # Convert image to grayscale
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # Read the template
        template = cv2.imread(os.path.join("data", template.get_path()), 0)
        # Store width and height of template in w and h
        w, h = template.shape[::-1]
        # Perform match operations
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        # Store the coordinates of matched area in a numpy array
        loc = np.where(res >= threshold)

        # Get rectangles containing matched regions
        rectangles = []
        for pt in zip(*loc[::-1]):
            rectangles.append({"x": pt[0], "y": pt[1], "w": w, "h": h})

        return rectangles
