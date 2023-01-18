from PyQt5.QtWidgets import QApplication, QFrame, QGridLayout, QHBoxLayout, QLabel, QLayout, QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout, QWidget
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QEventLoop, QObject, pyqtSignal, QThread
import sys
import subprocess
import os
import asyncio
import json
import requests
import aiohttp
import asyncqt

class UpdatePriceThread(QThread):
    cpuHourPrice = pyqtSignal(str)

    async def update_price(self):
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.stats.golem.network/v1/network/pricing/median", ssl=False) as resp:
                    data = await resp.json()
                    price = round(data["cpuhour"], 3)
                    self.cpuHourPrice.emit("$" + str(price))
            self.sleep(10)

    def run(self):
        while True:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.update_price())

class QaiseoApp(QMainWindow):
    def __init__(self):
        super(QaiseoApp, self).__init__()

        uic.loadUi("mainScreen.ui", self)
        self.show()

        self.homeContent = self.findChild(QStackedWidget, "homeContent")
        self.homeButton = self.findChild(QPushButton, "homeButton")
        self.tasksButton = self.findChild(QPushButton, "tasksButton")
        self.walletButton = self.findChild(QPushButton, "walletButton")
        self.swapButton = self.findChild(QPushButton, "swapButton")
        self.marketButton = self.findChild(QPushButton, "marketButton")
        self.settingsButton = self.findChild(QPushButton, "settingsButton")

        self.cpuPerHourPrice = self.findChild(QLabel, "cpuPerHourPrice")

        self.NavButtonHandler()
    
    def ContentChange(self, index):
        self.homeContent.setCurrentIndex(index)

    def NavButtonHandler(self):
        self.homeButton.clicked.connect(lambda: self.ContentChange(0))
        self.tasksButton.clicked.connect(lambda: self.ContentChange(1))
        self.walletButton.clicked.connect(lambda: self.ContentChange(2))
        self.swapButton.clicked.connect(lambda: self.ContentChange(3))
        self.marketButton.clicked.connect(lambda: self.ContentChange(4))
        self.settingsButton.clicked.connect(lambda: self.ContentChange(5))
    
    def CpuPriceUpdate(self, price):
        self.cpuPerHourPrice.setText(price)

def main():
    ApiCallLoop = UpdatePriceThread()
    app = QApplication(sys.argv)
    Window = QaiseoApp()
    ApiCallLoop.cpuHourPrice.connect(lambda price: Window.CpuPriceUpdate(price))
    ApiCallLoop.start()
    app.exec_()

main()
""" cwd = os.getcwd()
        yagnaPath = os.path.join(cwd, "yagna.exe")
        jqPath = os.path.join(cwd, "jq.exe")
        YagnaAppKey = None


        subprocess.Popen([yagnaPath, "service", "run"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) """