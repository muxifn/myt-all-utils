import time
import json

import kuaishou.answer
from utils import device_utils
from bilibili import bilibili
from kuaishou import answer

if __name__ == '__main__':
    # 读取 JSON 文件
    with open('./config/devices.json', 'r') as f:
        devices = json.load(f)

    for device in devices:
        if device['task_type']:
            a = device_utils.DeviceController()
            a.device_scrcpy_connect(device['ip'])
            a.device_name = device['device_id']
            time.sleep(5)
            b = bilibili.BiliBiliController(a)
            b.reward_index = device['gift_index']
            b.mounted()

