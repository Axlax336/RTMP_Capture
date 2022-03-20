import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from core import config
from view.mainWin import MainWin

if __name__ == '__main__':
    config.getInstance()
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWin().show()
    sys.exit(app.exec_())
