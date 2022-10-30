import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *

import RPi.GPIO as GPIO
import time
from pyfcm import FCMNotification

# Firebase에서 얻은 server key. 알맞게 수정할 것 https://console.firebase.google.com/project/smartmirror-4bf14/settings/cloudmessaging/android:com.example.smartmirror
FIREBASE_APIKEY = "AAAAQd5Gkn0:APA91bHRUsewNt-cjQzmOPgqVB0Vs1BhMXCP2QcN3TRe1zybSMI178SOY6grOSMGogAtiWCgSq5i2Iwft75WeI36es5wjSyf1_t1yRJRL__TlsNxroRxGAjTFLiSFsEPUxqPA4j8z5fT"
# PIR 센서의 GPIO 번호
PIR_GPIO = 23

class MotionManager(QThread):
    # 음성이 인식되면 발생하는 Signal
    recognitionSignal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.pushService = FCMNotification(FIREBASE_APIKEY)
        self.pushEnabled = False
        self.accumulateTime = 20
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIR_GPIO, GPIO.IN)

    def run(self):
        while True:
            if GPIO.input(PIR_GPIO):
                if self.pushEnabled:
                    if self.accumulateTime > 20: # Push 알람을 보내고 20초 이상 경과 후 움직임이 다시 감지되었을때
                        self.sendMessage("Motion", "Motion Detected!!")
                        self.accumulateTime = 0
                        print("Motion Detected. Push Message")
                    else:
                        # print("Motion Detected. But timeout yet.")
                        pass
                else:
                    # print("Motion Detected. But Push Disabled.")
                    pass
            else:
                self.accumulateTime = self.accumulateTime + 1
                # print("Motion Not Detected")
            time.sleep(1)

    def statusCallback(self, event):
        self.recognitionSignal.emit(event['type'], event['text'])

    def sendMessage(self, title, body):
        # 메시지 (data 타입)
        data_message = {
            "body": body,
            "title": title
        }
        # topic을 이용해 다수의 구독자에게 푸시알림을 전송함
        self.pushService.notify_topic_subscribers(topic_name="motion", data_message=data_message)

    def setPushEnabled(self, status):
        self.pushEnabled = status


if __name__ == "__main__":
    mw = MotionManager()
    mw.setPushEnabled(True)
    mw.start()

    time.sleep(1000)

