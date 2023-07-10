import logging



# 通用的基类
class BaseLgoClass:
    def __init__(self):
        self.loggers = {}

    def get_logger(self, device_no):
        if device_no not in self.loggers:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S')
            logger = logging.getLogger(device_no)
            logger.setLevel(logging.DEBUG)

            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # 创建文件处理器
            file_handler = logging.FileHandler('logs/' + device_no + '.log', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            self.loggers[device_no] = logger

        return self.loggers[device_no]

