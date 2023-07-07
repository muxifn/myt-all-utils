# 盒子中端控制工具包
集成 easyocr, cv2 , adbutils , scrcpy 的中端控制工具包用于快速开发自动化工具


## 免责声明
本软件是一个开源的自动化工具，旨在模拟人类操作。它被设计成仅通过现有的用户界面和交互进行操作，并且符合相关的法律法规。该软件旨在提供简化用户与功能和游戏之间的交互，并且不打算以任何方式破坏游戏的平衡或提供不公平的优势。该软件不会以任何方式修改游戏文件或游戏代码。请注意，使用本软件可能违反某些游戏或平台的使用条款，使用者需自行承担责任。作者对使用本软件可能导致的任何问题概不负责。

This software is an open-source automation tool designed to simulate human operations. It is designed to operate only through existing user interfaces and interactions, and comply with relevant laws and regulations. The software aims to simplify user interaction with features and games, and is not intended to disrupt the balance of the game in any way or provide unfair advantages. The software will not modify game files or game code in any way. Please note that using this software may violate the terms of use of certain games or platforms, and users are responsible for it themselves. The author is not responsible for any issues that may arise from using this software.

本软件开源、免费，仅供学习交流使用。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。


## 示例
### 小破站红包自动化

只支持720*1280模拟器或者盒子

修改config文件夹内`devices.json`文件

    [
      {
        "device_id": "phone-5003", #设备唯一标识
        "ip": "127.0.0.1:16384", #scrcpy,adb 连接地址和端口号 
        "gift_index": 0, #今日礼物次数
        "task_type": true #该是否开启自动化
      }
    ]



