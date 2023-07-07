import easyocr, re
from utils import game_utils

# 设置模型所在的目录路径
model_folder = 'model'

ocr_reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, model_storage_directory=model_folder)


class OcrController:

    def __init__(self, device):
        self.device = device
        self.game = game_utils.GameController(device)
        self.reader = ocr_reader

    def find_text(self, text, x1, y1, x2, y2):
        frame = self.device.get_frame()
        frame = frame[y1:y2, x1:x2]
        result = self.reader.readtext(frame, batch_size=4)
        if result:
            for detection in result:
                text_all = detection[1]
                if text in text_all:
                    coords = detection[0]
                    left = min(coords, key=(lambda x: x[0]))[0]
                    top = min(coords, key=(lambda x: x[1]))[1]
                    right = max(coords, key=(lambda x: x[0]))[0]
                    bottom = max(coords, key=(lambda x: x[1]))[1]
                    text_range = (
                        left, top, right, bottom)
                    top_left = (
                        text_range[0] + x1, text_range[1] + y1)
                    bottom_right = (text_range[2] + x1, text_range[3] + y1)
                    return (top_left, bottom_right)

    def find_text_click(self, text, x1, y1, x2, y2):
        ret = self.find_text(text, x1, y1, x2, y2)
        if ret:
            self.game.random_box_click(ret[0], ret[1])
            return True
        return False

    def find_pattern_text(self, pattern_text, x1, y1, x2, y2):
        search_region = self.device.get_frame()
        search_region = search_region[y1:y2, x1:x2]
        result = self.reader.readtext(search_region, batch_size=4)
        if result:
            for detection in result:
                text_all = detection[1]
                match = re.search(pattern_text, text_all)
                if match:
                    coords = detection[0]
                    left = min(coords, key=(lambda x: x[0]))[0]
                    top = min(coords, key=(lambda x: x[1]))[1]
                    right = max(coords, key=(lambda x: x[0]))[0]
                    bottom = max(coords, key=(lambda x: x[1]))[1]
                    text_range = (
                        left, top, right, bottom)
                    top_left = (
                        text_range[0] + x1, text_range[1] + y1)
                    bottom_right = (text_range[2] + x1, text_range[3] + y1)
                    return (text_all, top_left, bottom_right)

    def find_pattern_text_click(self, pattern_text, x1, y1, x2, y2):
        ret = self.find_pattern_text(pattern_text, x1, y1, x2, y2)
        if ret:
            self.game.random_box_click(ret[1], ret[2])
            return True
        return False

    def find_area_text(self, texts, x1, y1, x2, y2):
        search_region = self.device.get_frame()
        search_region = search_region[y1:y2, x1:x2]
        result = self.reader.readtext(search_region, batch_size=4)
        if result:
            for detection in result:
                text_all = detection[1]

                for text in texts:
                    if text in text_all:
                        coords = detection[0]
                        left = min(coords, key=(lambda x: x[0]))[0]
                        top = min(coords, key=(lambda x: x[1]))[1]
                        right = max(coords, key=(lambda x: x[0]))[0]
                        bottom = max(coords, key=(lambda x: x[1]))[1]
                        text_range = (
                            left, top, right, bottom)
                        top_left = (
                            text_range[0] + x1, text_range[1] + y1)
                        bottom_right = (text_range[2] + x1, text_range[3] + y1)
                        return (top_left, bottom_right)

    def find_area_text_click(self, texts, x1, y1, x2, y2):
        ret = self.find_area_text(texts, x1, y1, x2, y2)
        if ret:
            self.game.random_box_click(ret[1], ret[2])
            return True
        return False

    def find_text_area(self, text, area):
        frame = self.device.get_frame()
        for element in area:
            x1, x2, y1, y2 = (
                element[0], element[2], element[1], element[3])
            search_region = frame[y1:y2, x1:x2]
            result = self.reader.readtext(search_region, batch_size=4)
            if result:
                for detection in result:
                    text_all = detection[1]
                    if text in text_all:
                        coords = detection[0]
                        left = min(coords, key=(lambda x: x[0]))[0]
                        top = min(coords, key=(lambda x: x[1]))[1]
                        right = max(coords, key=(lambda x: x[0]))[0]
                        bottom = max(coords, key=(lambda x: x[1]))[1]
                        text_range = (
                            left, top, right, bottom)
                        top_left = (
                            text_range[0] + x1, text_range[1] + y1)
                        bottom_right = (text_range[2] + x1, text_range[3] + y1)
                        return (top_left, bottom_right)

    def find_text_area_click(self, text, area):
        ret = self.find_text_area(text, area)
        if ret:
            self.game.random_box_click(ret[1], ret[2])
            return True
        return False

    def get_text(self, x1, y1, x2, y2):
        search_region = self.device.get_frame()
        search_region = search_region[y1:y2, x1:x2]
        result = self.reader.readtext(search_region)
        if result:
            return result[0][1]

    def get_all_by_text(self, text, x1, y1, x2, y2):
        all_xy = []
        search_region = self.device.get_frame()
        search_region = search_region[y1:y2, x1:x2]
        result = self.reader.readtext(search_region, batch_size=4)
        if result:
            for detection in result:
                text_all = detection[1]
                if text in text_all:
                    coords = detection[0]
                    left = min(coords, key=(lambda x: x[0]))[0]
                    top = min(coords, key=(lambda x: x[1]))[1]
                    right = max(coords, key=(lambda x: x[0]))[0]
                    bottom = max(coords, key=(lambda x: x[1]))[1]
                    text_range = (
                        left, top, right, bottom)
                    top_left = (
                        text_range[0] + x1, text_range[1] + y1)
                    bottom_right = (text_range[2] + x1, text_range[3] + y1)
                    all_xy.append((top_left, bottom_right))
            return all_xy

    def get_all_by_pattern(self, pattern_text, x1, y1, x2, y2):
        all_xy = []
        search_region = self.device.get_frame()
        search_region = search_region[y1:y2, x1:x2]
        result = self.reader.readtext(search_region, batch_size=4)
        if result:
            for detection in result:
                text_all = detection[1]
                match = re.search(pattern_text, text_all)
                if match:
                    coords = detection[0]
                    left = min(coords, key=(lambda x: x[0]))[0]
                    top = min(coords, key=(lambda x: x[1]))[1]
                    right = max(coords, key=(lambda x: x[0]))[0]
                    bottom = max(coords, key=(lambda x: x[1]))[1]
                    text_range = (
                        left, top, right, bottom)
                    top_left = (
                        text_range[0] + x1, text_range[1] + y1)
                    bottom_right = (text_range[2] + x1, text_range[3] + y1)
                    all_xy.append((top_left, bottom_right))
            return all_xy
