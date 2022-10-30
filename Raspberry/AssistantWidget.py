import sys
import datetime
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *

from managers.AsstantManager import AssistantManager
from managers.MotionManager import MotionManager

class AssistantWidget(QWidget):
    # 위젯 인덱스를 이동할때 방출하는 Signal
    widgetMoveSignal = pyqtSignal(int)

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('AssistantWidget.ui', self)
        self.logoutButton.clicked.connect(self.logoutButtolClickSlot)
        self.assistantWorker = AssistantWorker(self)
        self.assistantWorker.recognitionSignal.connect(self.recognitionSlot)
        self.clockTimer = QTimer()
        self.clockTimer.timeout.connect(self.clockTimerTimeoutSlot)
        self.clockTimer.start(1000)
        self.assistantWorker.start()
        self.motionManager = MotionManager()
        self.motionManager.start()

    @pyqtSlot()
    def logoutButtolClickSlot(self):
        self.widgetMoveSignal.emit(0)

    @pyqtSlot()
    def clockTimerTimeoutSlot(self):
        now = datetime.datetime.now()
        currentTimeStr = now.strftime("%Y-%m-%d %H:%M:%S")
        self.datetimeLabel.setText(currentTimeStr)

    def showEvent(self, event):
        self.assistantWorker.setAssistantMute(False)
        self.motionManager.setPushEnabled(True)
        return super().showEvent(event)

    def hideEvent(self, event):
        self.assistantWorker.setAssistantMute(True)
        self.motionManager.setPushEnabled(False)
        return super().hideEvent(event)


    # 음성 인식 Signal에 대응되는 Slot.
    @pyqtSlot(str, str)
    def recognitionSlot(self, type, text):
        self.statusLabel.setText(type)
        # 뮤트 해제
        if(type == 'ON_MUTED_CHANGED'):
            pass
        # 미디어 IDLE
        elif(type == 'ON_MEDIA_STATE_IDLE'):
            pass
        # 모든 초기화 완료
        elif(type == 'ON_START_FINISHED'):
            pass
        # 사용자의 말하기 시작(핫워드감지)
        elif(type == 'ON_CONVERSATION_TURN_STARTED'):
            self.speechLabel.setText('...')
            self.responseLabel.setText('')
        # 사용자의 말하기 끝
        elif(type == 'ON_END_OF_UTTERANCE'):
            pass
        # 사용자의 말하기!
        elif(type == 'ON_RECOGNIZING_SPEECH_FINISHED'):
            self.speechLabel.setText(text)
        # 어시스턴트가 말하기 시작!
        elif(type == 'ON_RESPONDING_STARTED'):
            pass
        # 어시스턴트의 답변!
        elif(type == 'ON_RENDER_RESPONSE'):
            self.responseLabel.setText(self.responseLabel.text() + '\n'+ text)
        # 어시스턴트 말하기 종료
        elif(type == 'ON_RESPONDING_FINISHED'):
            pass
        # 음성인식 종료
        else:
            pass


class AssistantWorker(QThread):
    # 음성이 인식되면 발생하는 Signal
    recognitionSignal = pyqtSignal(str, str)

    def __init__(self, parent):
        super().__init__(parent)
        self.assistantManager = AssistantManager()

    def run(self):
        self.assistantManager.runGoogleAssistance(self.statusCallback)

    def statusCallback(self, event):
        self.recognitionSignal.emit(event['type'], event['text'])

    def setAssistantMute(self, isMuted):
        self.assistantManager.setMuteEnable(isMuted)


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    w = AssistantWidget()
    w.show()
    # w.showFullScreen()
    sys.exit(app.exec())
