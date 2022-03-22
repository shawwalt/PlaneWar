import sys

import random

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
        self.setWindowIcon(QIcon(Config['PATH_WINDOW_ICON'].toString()))
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

        self.setFixedSize(self.width, self.height)
        self.setWindowTitle(title)

        self.init_background()
        self.init_objects()

    def init_background(self):

        self.lb_background_1 = Map(Config["PATH_BACKGROUND_MAP"].toString(), 0,
                                   self)
        self.lb_background_2 = Map(Config["PATH_BACKGROUND_MAP"].toString(),
                                   self.height, self)
        self.lb_background_1.setGeometry(0, -700, self.width, self.height)
        self.lb_background_2.setGeometry(0, 0, self.width, self.height)

    def init_objects(self):

        self.lb_hero = HeroPlane(Config["PATH_HEROPLANE_PIC"].toString(), self,
                                 self)
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

        self.lb_background_1.timer.start()
        self.lb_background_2.timer.start()

    # 重写系统Evt函数
    def mouseMoveEvent(self, evt):
        self.lb_hero.move(evt.x() - int(self.init_hero_param[2] / 2),
                          evt.y() - int(self.init_hero_param[3] / 2))

    def mousePressEvent(self, evt):
        self.lb_hero.move(evt.x() - int(self.init_hero_param[2] / 2),
                          evt.y() - int(self.init_hero_param[3] / 2))
        self.lb_hero.timer_shoot.start()

    def mouseReleaseEvent(self, evt):
        self.lb_hero.timer_shoot.stop()


class HeroPlane(QLabel):
    def __init__(self, filepath, map, *args, **kwargs):

        super(HeroPlane, self).__init__(*args, **kwargs)

        self.shooting = False
        self.timer_shoot = QTimer()
        self.shootInterval = Config['BULLET_DIV'].toInt()
        self.shootRecorder = self.shootInterval
        self.bullets_stack_point = 0
        self.bullets = [
            Bullet(Config["PATH_BULLET_PIC"].toString(),
                   Config['BULLET_MOVE_STEP'].toInt(), map)
            for i in range(Config['BULLET_NUM'].toInt())
        ]
        self.setPixmap(QPixmap(filepath))

        self.timer_shoot.setInterval(Config['BULLET_SHOOT_RATE'].toInt())
        self.timer_shoot.timeout.connect(self.shoot)

    def shoot(self):
        if self.shootRecorder == self.shootInterval:
            self.shootRecorder = 0
            # 将当前子弹状态设为占用中
            self.bullets[self.bullets_stack_point].isFree = False
            # 初始化子弹位置为飞机头部位置
            self.bullets[self.bullets_stack_point].move(
                self.pos().x() + int(Config['PLANE_WIDTH'].toInt() / 2),
                self.pos().y())
            # 启动子弹内置时钟，自动更新位置
            self.bullets[self.bullets_stack_point].timer.start()
            self.bullets_stack_point = self.bullets_stack_point + 1
            if self.bullets_stack_point > Config['BULLET_NUM'].toInt() - 1:
                self.bullets_stack_point = 0
        self.shootRecorder = self.shootRecorder + 1


class Map(QLabel):
    def __init__(self, filepath, threshhold, *args, **kwargs):

        super(Map, self).__init__(*args, **kwargs)

        self.setPixmap(QPixmap(filepath))
        self.timer = QTimer()
        self.move_step = Config["BACKGROUND_ROLL_STEP"].toInt()
        self.trigger_threshhold = threshhold
        self.width = Config["SCENE_WIDTH"].toInt()
        self.height = Config["SCENE_HEIGHT"].toInt()

        self.timer.setInterval(Config['FLASH_RATE'].toInt())
        self.timer.timeout.connect(self.update_position)

    def update_position(self):

        pos_y = self.pos().y()

        if pos_y <= self.trigger_threshhold:
            pos_y = pos_y + self.move_step
            self.move(0, pos_y)

        else:
            self.move(0, self.pos().y() - self.height)


class Bullet(QLabel):
    def __init__(self, filepath, speed, *args, **kwargs):

        super(Bullet, self).__init__(*args, **kwargs)

        self.setPixmap(QPixmap(filepath))
        self.speed = speed
        self.isFree = True
        self.timer = QTimer()
        self.timer.setInterval(3)
        self.timer.timeout.connect(self.update_position)
        self.width = Config["BULLET_WIDTH"].toInt()
        self.height = Config["BULLET_HEIGHT"].toInt()
        self.setGeometry(0, -Config['SCENE_HEIGHT'].toInt(), self.width,
                         self.height)

    def update_position(self) -> bool:
        if self.isFree is False:
            x, y = self.pos().x(), self.pos().y()
            y = y - self.speed
            self.move(x, y)
            if (y < -self.height):
                self.timer.stop()
                self.isFree = True


class EnemyPlane(QLabel):
    def __init__(self, filepath, *args, **kwargs):
        super(EnemyPlane, self).__init__(*args, **kwargs)
        self.setPixmap(QPixmap(filepath))

        self.timer = QTimer()
        self.isFree = True,
        self.interval = Config['ENEMY_INTERVAL'].toInt()
        self.bullets = [
            Bullet(Config['PATH_MISSILE_ENEMY_PIC'].toString(),
                   Config['ENEMY_BULLET_SPEED'].toInt())
            for i in range(Config['ENEMY_BULLET_NUM'].toInt())
        ]
        self.speed = Config['ENEMY_SPEED'].toInt()
        self.width = Config['ENEMY_WIDTH'].toInt()
        self.height = Config['ENEMY_HEIGHT'].toInt()

    def update_position(self):
        if self.isFree is True:
            # 初始化敌机位置
            self.move(
                random.randint(self.width, Config['SCENE_WIDTH'].toInt()) -
                self.width,
                random.randint(self.height, Config['SCENE_HEIGHT'].toInt()) +
                self.height)
        else:
            # 更新路线策略
            pass


if __name__ == '__main__':

    app = QApplication(sys.argv)

    win = FrontEnd()

    sys.exit(app.exec_())