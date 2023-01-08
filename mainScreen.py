from PyQt5.QtWidgets import QApplication, QFrame, QGridLayout, QHBoxLayout, QLabel, QLayout, QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout, QWidget
from PyQt5 import uic
import sys
import subprocess
import os

class QaiseoApp(QMainWindow):
    def __init__(self):
        super(QaiseoApp, self).__init__()

        cwd = os.getcwd()
        yagnaPath = os.path.join(cwd, "yagna.exe")
        jqPath = os.path.join(cwd, "jq.exe")
        YagnaAppKey = None


        subprocess.Popen([yagnaPath, "service", "run"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        uic.loadUi("mainScreen.ui", self)
        self.show()

        self.homeContent = self.findChild(QStackedWidget, "homeContent")
        self.homeButton = self.findChild(QPushButton, "homeButton")
        self.tasksButton = self.findChild(QPushButton, "tasksButton")
        self.walletButton = self.findChild(QPushButton, "walletButton")
        self.swapButton = self.findChild(QPushButton, "swapButton")
        self.marketButton = self.findChild(QPushButton, "marketButton")
        self.settingsButton = self.findChild(QPushButton, "settingsButton")
        self.golemTokenPrice = self.findChild(QLabel, "golemTokenPrice")


        self.homeButton.clicked.connect(lambda: self.ContentChange(0))
        self.tasksButton.clicked.connect(lambda: self.ContentChange(1))
        self.walletButton.clicked.connect(lambda: self.ContentChange(2))
        self.swapButton.clicked.connect(lambda: self.ContentChange(3))
        self.marketButton.clicked.connect(lambda: self.ContentChange(4))
        self.settingsButton.clicked.connect(lambda: self.ContentChange(5))

    def ContentChange(self, index):
        self.homeContent.setCurrentIndex(index)
    

app = QApplication(sys.argv)
Window = QaiseoApp()
app.exec_()