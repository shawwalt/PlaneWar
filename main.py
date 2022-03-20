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
Config = load_json(':/settings/config.json')


class FrontEnd(QMainWindow, Ui_Form):
    def __init__(self, *args, **kwargs):

        super(FrontEnd, self).__init__(*args, **kwargs)

        self.setupUi(self)

        self.setWindowIcon(QIcon(':/images/windowicon.png'))

        self.width = Config["SCENE_WIDTH"].toInt()

        self.height = Config["SCENE_HEIGHT"].toInt()

        self.move_step = Config["BACKGROUND_ROLL_STEP"].toInt()

        self.flash_rate = Config["FLASH_RATE"].toInt()
        self.init_scene()
        self.start_game()

        self.show()

    # 界面初始化

    def init_scene(self):

        title = Config["WIN_TITLE"].toString()

        self.resize(self.width, self.height)

        self.setWindowTitle(title)

        self.init_background()

        self.init_objects()

    def init_background(self):

        self.lb_background_1 = Map(Config["PATH_BACKGROUND_MAP"].toString(),
                                   self)

        self.lb_background_2 = Map(Config["PATH_BACKGROUND_MAP"].toString(),
                                   self)

        self.lb_background_1.setGeometry(0, -700, self.width, self.height)

        self.lb_background_2.setGeometry(0, 0, self.width, self.height)

    def init_objects(self):

        self.lb_hero = HeroPlane(Config["PATH_HEROPLANE_PIC"].toString(), self)

        self.init_hero_param = (Config["HERO_INIT_POSX"].toInt(),
                                Config["HERO_INIT_POSY"].toInt(),
                                Config['PLANE_WIDTH'].toInt(),
                                Config["PLANE_HEIGHT"].toInt())

        self.lb_hero.setGeometry(
            self.init_hero_param[0] - int(self.init_hero_param[2] / 2),
            self.init_hero_param[1], self.init_hero_param[2],
            self.init_hero_param[3])

    # 响应方法区

    def start_game(self):

        self.timer = QTimer()

        self.timer.timeout.connect(self.flash_screen)

        self.timer.setInterval(self.flash_rate)
        self.timer.start()

    def flash_screen(self):

        self.updata_background_map()

    def updata_background_map(self):

        y1 = self.lb_background_1.pos().y()

        y2 = self.lb_background_2.pos().y()

        if y1 <= 0:

            y1 = y1 + self.move_step

            self.lb_background_1.move(0, y1)

        else:

            self.lb_background_1.move(0, -self.height)

        if y2 <= self.height:

            y2 = y2 + self.move_step

            self.lb_background_2.move(0, y2)

        else:

            self.lb_background_2.move(0, 0)

    # 重写系统Evt函数
    def mouseMoveEvent(self, evt):
        self.lb_hero.move(evt.x() - int(self.init_hero_param[2] / 2),
                          evt.y() - int(self.init_hero_param[3] / 2))


class HeroPlane(QLabel):
    def __init__(self, filepath, *args, **kwargs):

        super(HeroPlane, self).__init__(*args, **kwargs)

        self.shooting = False
        self.shootInterval = Config['BULLET_DIV'].toInt()
        self.shootRecorder = self.shootInterval
        self.bullets_stack_point = [0, 0]
        self.bullets = [
            Bullet(Config["PATH_BULLET_PIC"].toString(),
                   Config['BULLET_MOVE_STEP'].toInt())
            for i in range(Config['BULLET_NUM'].toInt())
        ]
        self.setPixmap(QPixmap(filepath))

    def shoot(self):
        if self.shootRecorder == self.shootInterval:
            self.bullets[self.bullets_stack_point[1]] = True
            self.bullets_stack_point[1] = self.bullets_stack_point[1] + 1


class Map(QLabel):
    def __init__(self, filepath, *args, **kwargs):

        super(Map, self).__init__(*args, **kwargs)

        self.setPixmap(QPixmap(filepath))


class Bullet(QLabel):
    def __init__(self, filepath, speed, *args, **kwargs):

        super(Bullet, self).__init__(*args, **kwargs)

        self.setPixmap(QPixmap(filepath))
        self.speed = speed
        self.isFree = True
        self.width = Config["BULLET_WIDTH"].toInt()
        self.height = Config["BULLET_HEIGHT"].toInt()

    def update_position(self):
        if isFree is False:
            x, y = self.pos().x(), self.pos().y()
            y = y - self.speed
            self.move(x, y)
            if (y < -self.height):
                self.isFree = True


if __name__ == '__main__':

    app = QApplication(sys.argv)

    win = FrontEnd()

    sys.exit(app.exec_())