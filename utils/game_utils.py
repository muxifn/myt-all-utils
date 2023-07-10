import math
import random


class GameController:

    def __init__(self, device):
        self.device = device

    # 计算中心的坐标
    def get_center_xy(self, top_left, bottom_right):
        x1, y1 = top_left
        x2, y2 = bottom_right
        r_x = (x1 + x2) / 2
        r_y = (y1 + y2) / 2
        return (int(r_x), int(r_y))

    # 坐标随机生成偏移量并点击
    def random_pos_click(self, pos):
        x, y = pos
        x_offset = random.randint(-8, 8)
        y_offset = random.randint(-8, 8)
        x += x_offset
        y += y_offset
        self.device.click(x, y)

    # 矩形框中心坐标随机生成偏移量并点击
    def random_box_click(self, top_left, bottom_right):
        x, y = self.get_center_xy(top_left, bottom_right)
        x_offset = random.randint(-8, 8)
        y_offset = random.randint(-8, 8)
        x += x_offset
        y += y_offset
        self.device.click(x, y)

    # 计算了两个坐标点之间的欧几里德距离
    def distance_between_points(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def 获取终点坐标(self, start_x, start_y, angle, length):
        d = angle % 90  # 计算角度对 90 取余

        angle_rad = math.radians(d)
        x_offset = length * math.cos(angle_rad)
        y_offset = length * math.sin(angle_rad)

        if angle > 270:
            x1 = start_x - x_offset
            y1 = start_y - y_offset
        elif angle > 180:
            x1 = start_x - x_offset
            y1 = start_y + y_offset
        elif angle > 90:
            x1 = start_x + x_offset
            y1 = start_y + y_offset
        else:
            x1 = start_x + y_offset
            y1 = start_y - x_offset

        return (x1, y1)

    def 计算角度(self, x1, y1, x2, y2):
        # 处理斜率为无穷大的情况（x1 - x2 = 0）
        if x1 - x2 == 0:
            if y1 > y2:
                return 180
            else:
                return 1
        # 处理斜率为零的情况（y1 - y2 = 0）
        if y1 - y2 == 0:
            if x1 > x2:
                return 270
            else:
                return 90

        dx = x2 - x1
        dy = y2 - y1
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)

        # 根据象限调整角度
        if dx > 0 and dy < 0:
            angle_deg += 90
        elif dx > 0 and dy > 0:
            angle_deg += 90
        elif dx < 0 and dy > 0:
            angle_deg += 270
        elif dx < 0 and dy < 0:
            angle_deg += 270

        return 360 - int(angle_deg)
