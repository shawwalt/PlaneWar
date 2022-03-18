import sys
import resources
from MainScene import Ui_Form
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

'''
来源：pyqtjson解析：https://blog.csdn.net/u011218356/article/details/108708510
      qt案例_飞机大战：https://www.bilibili.com/video/BV1xy4y1m794?p=3
'''


def jsonParse(data):
    error = QJsonParseError()
    json = QJsonDocument().fromJson(data, error)
    return json.object()


class FrontEnd(QMainWindow, Ui_Form):
    def __init__(self, *args, **kwargs):
        super(FrontEnd, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.init_scene()
        self.show()

    def init_scene(self):
        f = QFile(':/settings/config.json')
        f.open(QFile.ReadOnly | QFile.Text)
        if f.isOpen() == 1:
            config = f.readAll()
            j = jsonParse(config)
            width = j["SCENE_WIDTH"].toInt()
            height = j["SCENE_HEIGHT"].toInt()
            title = j["WIN_TITLE"].toString()
            self.resize(width, height)
            self.setWindowTitle(title)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = FrontEnd()
    sys.exit(app.exec_())