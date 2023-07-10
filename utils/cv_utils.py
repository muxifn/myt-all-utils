import cv2

from utils import game_utils


class CvController:
    def __init__(self, device):
        self.device = device
        self.game = game_utils.GameController(device)

    def find_img(self, img_path, x1, y1, x2, y2, threshold=0.8):
        frame = self.device.get_frame()
        max_threshold = 0.0
        if not type(img_path) == list:
            img_path = [
                img_path]
        for element in img_path:
            template = cv2.imread(element)
            frame_new = frame[y1:y2, x1:x2]
            result = cv2.matchTemplate(frame_new, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            max_threshold=max_val
            if max_val > threshold:
                top_left = (
                    max_loc[0] + x1, max_loc[1] + y1)
                bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
                return True, (top_left, bottom_right, max_val)
        return False, (0, 0, max_threshold)

    def find_img_click(self, img_path, x1, y1, x2, y2, threshold=0.8):
        s, ret = self.find_img(img_path, x1, y1, x2, y2, threshold)
        if s:
            self.game.random_box_click(ret[0], ret[1])
            return True
        return False

    def find_img_area(self, img_path, area_xy, threshold=0.8):
        frame = self.device.get_frame()
        template = cv2.imread(img_path)
        max_threshold = 0.0
        for element in area_xy:
            x1, x2, y1, y2 = (
                element[0], element[2], element[1], element[3])
            frame_new = frame[y1:y2, x1:x2]
            result = cv2.matchTemplate(frame_new, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > threshold:
                top_left = (
                    max_loc[0] + x1, max_loc[1] + y1)
                bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
                return True, (top_left, bottom_right, max_val)
            max_threshold = max_val
        else:
            return (
                False, (0, 0, max_threshold))

    def find_img_area_click(self, img_path, area_xy, threshold=0.8):
        s, ret = self.find_img_area(img_path, area_xy, threshold)
        if s:
            self.game.random_box_click(ret[0], ret[1])
            return True
        return False
