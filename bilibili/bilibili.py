import math
import random
import re
import time
import requests
from threading import Thread
from utils import cv_utils
from utils import ocr_utils
from utils import game_utils
from utils import base_logger


def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


class BiliBiliController:
    def __init__(self, device):
        self.logger = base_logger.BaseLgoClass().get_logger(device.device_name)
        self.device = device
        self.game = game_utils.GameController(device)
        self.img = cv_utils.CvController(device)
        self.ocr = ocr_utils.OcrController(device)

        self.pkg_name = ''
        self.img_path = 'bilibili/img/'

        self.raffle_type = False
        self.filter_type = True

        self.reward_index = 0


    @async_call
    def filter_task_info(self):
        while self.filter_type:

            # 中奖
            found, _ = self.img.find_img(self.img_path + "filter01.png", 256, 650, 452, 900, 0.8)
            if found:
                self.game.random_pos_click((596, 260))
                self.reward_index += 1
                text = self.ocr.get_text(160, 552, 553, 666)
                self.raffle_type = True
                self.logger.info(f"设备: '{self.device.device_name}', 中奖！{text}。累计中奖次数 {self.reward_index}")

            if self.ocr.find_text('没有抽中', 353, 545, 459, 604):
                self.game.random_pos_click((596, 260))
                self.logger.info(f"设备: '{self.device.device_name}', 未中奖！")

            cc = [
                (205, 570, 353, 610),
                (206, 543, 354, 580),
            ]
            if self.ocr.find_text_area('下次参与抽奖', cc):
                self.game.random_pos_click((596, 260))
                self.logger.info(f"设备: '{self.device.device_name}', 错过抽奖！")

            time.sleep(1)

    @async_call
    def mounted(self):
        if 'tv.danmaku.bili' not in self.device.get_app_info():
            cmd = f"am start -n tv.danmaku.bili/.MainActivityV2"
            self.device.adb.shell(cmd)
            time.sleep(10)

        self.filter_task_info()
        self.pkg_name = self.device.get_app_info()

        while True:

            if self.raffle_type:
                look_video = random.randint(240, 1000)
                self.logger.info(
                    f"设备: '{self.device.device_name}', 红包中奖-观看时间: {look_video}！")
                time.sleep(look_video)
                self.raffle_type = False
                continue

            if self.reward_index >= 20:
                self.logger.info(f"设备: '{self.device.device_name}', 红包获取达到最大值退出任务！")
                self.filter_type = False
                break

            money_datas = self.get_list()
            for room_id in money_datas:
                self.jump_room(room_id)
                if self.check_money():
                    break

            time.sleep(2)

    def get_list(self):
        money_datas = []
        page = random.randint(1, 5)
        numbers = [1, 2, 3, 5, 6, 9, 10]
        for i in range(5):
            url = "https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=" + str(
                random.choice(numbers)) + "&page=" + str(
                i + page)
            # 发送HTTP请求并获取响应
            response = requests.get(url)
            # 解析JSON数据
            json_data = response.json()

            if json_data['code'] == 0:
                data = json_data['data']
                if 'list' in data:
                    for v in data['list']:
                        if 'pendant_info' in v:
                            pendant_info = v['pendant_info']
                            if '2' in pendant_info:
                                money_box = pendant_info["2"]
                                if '红包' == money_box['content']:
                                    money_datas.append(v['roomid'])

        return money_datas

    def jump_room(self, room_id):
        cmd = f"am start -a android.intent.action.VIEW -d 'bilibili://live/{room_id}'"
        self.device.adb.shell(cmd)
        time.sleep(5)

    def check_money(self):
        for i in range(8):
            time.sleep(1)
            if self.img.find_img_click(self.img_path + "money_icon.png", 601, 692, 707, 1146, 0.8):
                time.sleep(3)
                s, ret = self.img.find_img(self.img_path + "battery.png", 250, 635, 480, 710)
                if s:
                    x, y = self.game.get_center_xy(ret[0], ret[1])
                    xy = x + 11, y - 11, 480, y + 13
                    ret = self.ocr.get_text(*xy)
                    if ret:
                        nums = re.findall(r'\d+', ret)
                        if nums:
                            self.logger.info(f"设备: '{self.device.device_name}', 检测到礼物价值: '{int(nums[0])}'")
                            if int(nums[0]) >= 50:
                                if self.ocr.find_text('点点红包抽礼物', 330, 850, 455, 908) or self.img.find_img(
                                        self.img_path + "money_text.png", 114, 645, 603, 896):
                                    self.game.random_pos_click((360, 760))
                                    time.sleep(3)

                                    s, ret = self.img.find_img(self.img_path + "kai_jiang.png", 41, 470, 692, 948)
                                    if s:
                                        x, y = self.game.get_center_xy(ret[0], ret[1])
                                        xy = 250, y - 17, x - 50, y + 15
                                        time_str = self.ocr.get_text(*xy)
                                        if time_str:
                                            if "." in time_str:
                                                minutes, seconds = map(int, time_str.split('.'))
                                            else:
                                                minutes, seconds = map(int, time_str.split(':'))
                                            seconds = minutes * 60 + seconds
                                            self.logger.info(
                                                f"设备: '{self.device.device_name}', 参与了抽奖-开奖时间等待: '{seconds}' 秒")
                                            self.game.random_pos_click((596, 260))
                                            time.sleep(seconds + 5)
                                        else:
                                            time.sleep(random.randint(10, 30) + 5)
                                return True
                            else:
                                self.game.random_pos_click((596, 260))
                                time.sleep(random.randint(1, 30))
                                return False

