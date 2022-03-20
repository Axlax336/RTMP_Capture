from PyQt5.QtWidgets import QMainWindow
from vlc import EventType

from core.vlc import Player
from view.QtDesigner.player import Ui_Form


class PlayerWin(QMainWindow, Ui_Form):
    def __init__(self, winid, close_callback, *args, **kwargs):
        super(PlayerWin, self).__init__(*args, **kwargs)
        self.winid = winid
        self.close_callback = close_callback
        self.setupUi(self)
        self.player = Player()
        self.player.set_window(self.frame.winId())
        self.volumeSlider.valueChanged.connect(self.volumeChange)
        self.volumeSlider.setValue(25)
        self.player.add_callback(EventType.MediaPlayerTimeChanged, self.timeUpdate)

    def play(self, rtmp_url):
        self.player.play(rtmp_url)

    def timeUpdate(self, event):
        m, s = divmod(self.player.get_time() / 1000, 60)
        h, m = divmod(m, 60)
        self.timeLabel.setText("%02d:%02d:%02d" % (h, m, s))

    def volumeChange(self):
        self.player.set_volume(self.volumeSlider.value())

    def closeEvent(self, event):
        self.player.stop()
        self.player.release()
        self.close_callback(self.winid)
        event.accept()
