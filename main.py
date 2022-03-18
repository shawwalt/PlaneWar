import sys
import resources_rc
from Ui_MainScene import Ui_Form
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
'''
来源：pyqtjson解析：https://blog.csdn.net/u011218356/article/details/108708510
      qt案例_飞机大战：https://www.bilibili.com/video/BV1xy4y1m794?p=3
      qt_centralwidget设置布局：https://blog.csdn.net/h84121599/article/details/111084982
'''


# 通用函数区
def json_parse(data):
    error = QJsonParseError()
    json = QJsonDocument().fromJson(data, error)
    return json.object()


def load_json(filepath):
    f = QFile(filepath)
    f.open(QFile.ReadOnly | QFile.Text)
    if f.isOpen() == 1:
        config = f.readAll()
        return json_parse(config)


# 类区
class FrontEnd(QMainWindow, Ui_Form):
    def __init__(self, *args, **kwargs):
        super(FrontEnd, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowIcon(QIcon(':/images/windowicon.png'))
        self.config = load_json(':/settings/config.json')
        self.init_scene()
        self.init_background()
        self.show()

    def init_background(self):
        width = self.config["SCENE_WIDTH"].toInt()
        height = self.config["SCENE_HEIGHT"].toInt()
        self.lb_background_1 = QLabel("", self)
        self.lb_background_2 = QLabel("", self)
        background_map = Map(':/images/background.png')
        self.lb_background_1.setPixmap(background_map)
        self.lb_background_2.setPixmap(background_map)
        self.lb_background_1.setGeometry(0, -700, width, height)
        self.lb_background_2.setGeometry(0, 0, width, height)

    def init_scene(self):
        width = self.config["SCENE_WIDTH"].toInt()
        height = self.config["SCENE_HEIGHT"].toInt()
        title = self.config["WIN_TITLE"].toString()
        self.resize(width, height)
        self.setWindowTitle(title)


class Map(QPixmap):
    def __init__(self, filepath, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        self.load(filepath)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = FrontEnd()
    sys.exit(app.exec_())