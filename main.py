import os
import sys
from configparser import SafeConfigParser

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication

import captureService
import powerControl
from window import Ui_Form


class QtWin(QMainWindow, Ui_Form):
    def __init__(self, *args, **kwargs):
        super(QtWin, self).__init__(*args, **kwargs)
        self.cmdTemp = r"start ${player} ${urlpath}"
        self.playerPath = r"D:\PotPlayer64\PotPlayerMini64.exe"
        self.setupUi(self)
        self.setWindowTitle('RTMP链接嗅探工具V1.0')
        interfaces = captureService.getAllNetInterfaces()
        for key in interfaces:
            netcard = interfaces[key]
            self.comboBox.addItem(f"{netcard.name} - {netcard.description}", netcard.description)
        self.checkBox.stateChanged.connect(self.powerCheckBoxChanged)
        self.checkBox.setChecked(True)

        self.startButton.clicked.connect(self.startBtnHandle)
        self.stopButton.clicked.connect(self.stopBtnHandle)
        self.delButton.clicked.connect(self.delBtnHandler)
        self.clearButton.clicked.connect(lambda: self.listWidget.clear())
        self.pushButton.clicked.connect(self.pushBtnHandler)
        self.stopButton.hide()
        self.initParams()


    def initParams(self):
        current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        f = os.path.join(current_path, "RTMP_config.ini")
        print(f"find ini file at {f}")
        if os.path.exists(f):
            config = SafeConfigParser()
            config.read(f)
            self.playerPath = config.get('main', 'PotplayerPath')
            self.cmdTemp = config.get('main', 'CmdTemp')

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
        data = self.listWidget.currentItem().text()
        cmd = self.cmdTemp.replace('${player}', self.playerPath) \
            .replace('${urlpath}', "\"" + data + "\"")
        print(f"run cmd: {cmd}")
        os.system(cmd)

    def closeEvent(self, event):
        captureService.stop()
        powerControl.end_timer()
        event.accept()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = QtWin()
    win.show()
    sys.exit(app.exec_())
