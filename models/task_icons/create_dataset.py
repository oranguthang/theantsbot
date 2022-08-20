import os
import cv2

from src.utils import ImageHandler


def create_dataset(path_to_screenshots, output_path):
    from src.settings import Settings

    settings = Settings.load_settings()

    idx = 0
    for filename in os.listdir(path_to_screenshots):
        if filename.endswith(".png"):
            img_orig = cv2.imread(os.path.join(path_to_screenshots, filename))
            for rectangle_name in ("anthillTasksIconsBar", "anotherAnthillFindExoticPeaIcon"):
                img_crop = ImageHandler.crop_image(
                    img_orig,
                    settings["rectangles"][rectangle_name]["x"],
                    settings["rectangles"][rectangle_name]["y"],
                    settings["rectangles"][rectangle_name]["h"],
                    settings["rectangles"][rectangle_name]["w"]
                )
                circles = ImageHandler.get_circles(
                    img_crop, hough_blur_radius=5, output_blur_radius=3, min_dist=50,
                    hough_param1=50, hough_param2=50, min_radius=20, max_radius=40, new_size=(64, 64)
                )

                if not circles:
                    continue

                for circle in circles:
                    cv2.imwrite(os.path.join(output_path, f"{idx}.jpg"), circle["image"])
                    idx += 1


if __name__ == "__main__":
    # Go to the project root directory
    os.chdir('../..')
    folder_path = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(folder_path, "images")

    os.makedirs(output_folder, exist_ok=True)

    create_dataset(
        path_to_screenshots=os.path.join("screenshots", "tmp"),
        output_path=output_folder
    )
