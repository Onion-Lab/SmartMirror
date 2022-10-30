import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *
import urllib.request
import socket

class HomeWidget(QWidget):
    # 위젯 인덱스를 이동할때 방출하는 Signal
    widgetMoveSignal = pyqtSignal(int)

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('HomeWidget.ui', self)
        self.loginButton.clicked.connect(self.loginButtonClickSlot)
        self.registerButton.clicked.connect(self.registerButtonClickSlot)
        self.refreshButton.clicked.connect(self.refreshButtonClickSlot)
        self.refreshButtonClickSlot()

    @pyqtSlot()
    def loginButtonClickSlot(self):
        self.widgetMoveSignal.emit(1)

    @pyqtSlot()
    def registerButtonClickSlot(self):
        self.widgetMoveSignal.emit(2)

    @pyqtSlot()
    def refreshButtonClickSlot(self):
        externalIP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('google.com', 443))
        internelIP = sock.getsockname()[0]
        self.internelIpLabel.setText(internelIP)
        self.externelIpLabel.setText(externalIP)


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    w = HomeWidget()
    w.show()
    # w.ui.showFullScreen()
    sys.exit(app.exec())
