import scrcpy

import adbutils

from threading import Thread

adb = adbutils.AdbClient()


def async_call(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return wrapper


class DeviceController:

    def __init__(self):
        self.connect_tool = None
        self.device_name = None
        self.adb = None
        self.scrcpy_client = None
        self.frame = None

    def device_scrcpy_connect(self, ip):

        def on_frame(frame):
            if frame is not None:
                self.frame = frame

        adb.connect(ip)
        for info in adb.list():
            if ip == info.serial:
                client = scrcpy.Client(device=(adb.device(info.serial)), max_fps=5)
                client.add_listener(scrcpy.EVENT_FRAME, on_frame)
                client.start(threaded=True)
                self.scrcpy_client = client
                self.adb = adb.device(info.serial)
                self.connect_tool = 'scrcpy'
                break

    def device_scrcpy_disconnect(self):
        self.scrcpy_client.stop()

    def get_frame(self):
        if 'scrcpy' == self.connect_tool:
            return self.frame

    def mounted(self, msg):
        if 'click' == msg['action']:
            xy = msg['xy']
            self.click(xy[0], xy[1])
        elif 'touch' == msg['action']:
            xy = msg['xy']
            self.touch(xy[0], xy[1], msg['touch_type'])
        elif 'swipe' == msg['action']:
            xy = msg['xy']
            self.swipe(xy[0], xy[1], xy[2], xy[3], msg['duration'])
        elif 'async_swipe' == msg['action']:
            xy = msg['xy']
            self.swipe(xy[0], xy[1], xy[2], xy[3], msg['duration'])
        elif 'switch_apk' == msg['action']:
            self.switch_apk(msg['pkg_name'])
        elif 'send_key_event' == msg['action']:
            self.send_key_event(msg['key'])

        return True

    def click(self, x, y):
        if 'scrcpy' == self.connect_tool or 'adb' == self.connect_tool:
            self.adb.click(x, y)

    def touch(self, x, y, action='down'):
        if 'scrcpy' == self.connect_tool:
            if 'down' == action:
                self.scrcpy_client.control.touch(x, y, scrcpy.ACTION_DOWN)
            else:
                self.scrcpy_client.control.touch(x, y, scrcpy.ACTION_UP)

    def swipe(self, x, y, x1, y1, duration=0.3):
        if 'scrcpy' == self.connect_tool or 'adb' == self.connect_tool:
            self.adb.swipe(x, y, x1, y1, duration=duration)

    @async_call
    def async_swipe(self, x, y, x1, y1, duration=0.3):
        if 'scrcpy' == self.connect_tool or 'adb' == self.connect_tool:
            self.adb.swipe(x, y, x1, y1, duration=duration)

    def switch_apk(self, pkg_name):
        if 'scrcpy' == self.connect_tool or 'adb' == self.connect_tool:
            cmd = f"am start -n {pkg_name}"
            self.adb.shell(cmd)

    def send_key_event(self, key):
        if 'scrcpy' == self.connect_tool or 'adb' == self.connect_tool:
            self.adb.keyevent(key)

    # 获取当前应用信息
    def get_app_info(self):
        app_info = self.adb.app_current()
        pak = app_info.package + '/' + app_info.activity
        pak = pak.replace('$', '\$')
        return pak
