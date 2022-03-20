import os
import uuid

from PyQt5.QtWidgets import QMainWindow

from core import captureService, powerControl, config
from view.QtDesigner.window import Ui_Form
from view.playerWin import PlayerWin


class MainWin(QMainWindow, Ui_Form):
    def __init__(self, *args, **kwargs):
        self.playerwins = {}
        self.conf = config.getInstance()

        super(MainWin, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('RTMP链接嗅探工具V1.1')
        interfaces = captureService.getAllNetInterfaces()
        for key in interfaces:
            netcard = interfaces[key]
            if netcard.name == netcard.description:
                text = netcard.name
            else:
                text = f"{netcard.name} - {netcard.description}"
            self.comboBox.addItem(text, netcard.description)

        self.checkBox.stateChanged.connect(self.powerCheckBoxChanged)
        self.checkBox.setChecked(True)
        self.startButton.clicked.connect(self.startBtnHandle)
        self.stopButton.clicked.connect(self.stopBtnHandle)
        self.delButton.clicked.connect(self.delBtnHandler)
        self.clearButton.clicked.connect(lambda: self.listWidget.clear())
        self.pushButton.clicked.connect(self.pushBtnHandler)
        self.playButton.clicked.connect(self.playBtnHandler)
        self.stopButton.hide()

    def powerCheckBoxChanged(self):
        if self.checkBox.isChecked():
            powerControl.start_timer()
        else:
            powerControl.end_timer()

    def startBtnHandle(self):
        print(self.comboBox.currentData())
        captureService.start(iface=self.comboBox.currentData(), captured_callback=self.addDateToTable)
        print("capture start!")
        self.startButton.hide()
        self.stopButton.show()

    def stopBtnHandle(self):
        captureService.stop()
        print("capture stop!")
        self.startButton.show()
        self.stopButton.hide()

    def delBtnHandler(self):
        if self.listWidget.count() == 0:
            return
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.isSelected():
                self.listWidget.removeItemWidget(self.listWidget.takeItem(i))
                return

    def addDateToTable(self, data):
        if self.listWidget.count() >= 15:
            self.listWidget.removeItemWidget(self.listWidget.takeItem(0))
        self.listWidget.addItem(data)

    def pushBtnHandler(self):
        if self.listWidget.currentItem():
            data = self.listWidget.currentItem().text()
            cmd = self.conf.get_cmd_template().replace('${player}', self.conf.get_player_path()) \
                .replace('${urlpath}', "\"" + data + "\"")
            print(f"run cmd: {cmd}")
            os.system(cmd)

    def playBtnHandler(self):
        if self.listWidget.currentItem():
            data = self.listWidget.currentItem().text()
            uuidstr = uuid.uuid1()
            pw = PlayerWin(winid=uuidstr, close_callback=self.playerWinClosed)
            pw.show()
            self.playerwins[uuidstr] = pw
            pw.play(data)

    def playerWinClosed(self, winid):
        del self.playerwins[winid]

    def closeEvent(self, event):
        captureService.stop()
        powerControl.end_timer()
        event.accept()
