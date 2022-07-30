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


class ExtractText:
    @staticmethod
    def run(image, char_whitelist=None, custom_config=None):
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
    def threshold(image):
        if not isinstance(image, np.ndarray):
            image = np.frombuffer(image, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_resized = cv2.resize(image, (0, 0), fx=2.5, fy=2.5)
        ret, thresh = cv2.threshold(img_resized, 80, 255, cv2.THRESH_BINARY)
        return thresh

    @staticmethod
    def check_pixel_is_gray(image, x, y):
        if not isinstance(image, np.ndarray):
            image = np.frombuffer(image, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        b, g, r = image[y, x]
        # if std of colors less than 4.0, the pixel is near black or gray
        return np.std([b, g, r]) < 4.0

    @staticmethod
    def check_pixel_is_blue(image, x, y):
        if not isinstance(image, np.ndarray):
            image = np.frombuffer(image, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        b, g, r = image[y, x]
        # if blue channel is more than green and red, the pixel is near blue
        return b > g and b > r

    @staticmethod
    def crop_image(image, x, y, h, w):
        if not isinstance(image, np.ndarray):
            image = np.frombuffer(image, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        img_cropped = image[y:y + h, x:x + w]
        return img_cropped