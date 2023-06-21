'''
Author: Huang-Junchen huangjc_mail@163.com
Date: 2023-06-21 13:53:45
LastEditors: Huang-Junchen huangjc_mail@163.com
LastEditTime: 2023-06-21 14:50:47
FilePath: /kunkun-game/app.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QBrush, QPen, QImage, QPixmap, QMovie

import cv2
import pygame
import random

class Game(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化Pygame
        pygame.init()

        # 设置游戏窗口大小
        self.width = 640
        self.height = 480
        self.setGeometry(100, 100, self.width, self.height)

        # 设置游戏速度
        self.speed = 5

        # 初始化游戏分数
        self.score = 0

        # 初始化玩家位置
        self.player_x = self.width//2
        self.player_y = self.height - 133

        self.player = QLabel(self)
        self.player_movie = QMovie("media/images/CXK.gif")
        self.player.setMovie(self.player_movie)
        self.player_movie.start()

        # 初始化篮球位置
        self.ball_x = random.randint(0, self.width - 50)
        self.ball_y = 0

        self.ball = QLabel(self)
        self.ball_movie = QMovie("media/images/big_basketball.gif")
        self.ball.setMovie(self.ball_movie)
        self.ball_movie.start()

        # 创建摄像头对象
        self.cap = cv2.VideoCapture(0)

        # 设置游戏定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGame)
        self.timer.start(10)

    def paintEvent(self, event):
        # 创建游戏画面
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)

        # 绘制摄像头画面
        ret, frame = self.cap.read()
        if ret:
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            image = image.rgbSwapped()

            # 将图像显示在标签上
            # self.image_label.setPixmap(QPixmap.fromImage(image))
            painter.drawImage(QPoint(0, 0), image)
        # 绘制玩家
        # painter.setBrush(QBrush(Qt.green))
        # painter.drawRect(self.player_x, self.player_y, 50, 50)
        self.player.setGeometry(self.player_x, self.player_y, 100, 133)
        # 绘制篮球
        # painter.setBrush(QBrush(Qt.red))
        # painter.drawEllipse(self.ball_x, self.ball_y, 50, 50)
        self.ball.setGeometry(self.ball_x, self.ball_y, 50, 50)
        # 绘制分数
        painter.setPen(QPen(Qt.black, 20))
        painter.drawText(10, 50, f"Score: {self.score}")

    def updateGame(self):
        # 更新篮球位置
        self.ball_y += self.speed

        # 判断篮球是否与玩家相撞
        if self.ball_x < self.player_x + 50 and self.ball_x + 50 > self.player_x and self.ball_y + 50 > self.player_y:
            self.score += 1
            self.ball_x = random.randint(0, self.width - 50)
            self.ball_y = 0

        # 判断篮球是否超出屏幕
        if self.ball_y > self.height:
            self.ball_x = random.randint(0, self.width - 50)
            self.ball_y = 0

        # 重新绘制游戏窗口
        self.repaint()

    def keyPressEvent(self, event):
        # 移动玩家
        if event.key() == Qt.Key_Left:
            self.player_x -= 20
        elif event.key() == Qt.Key_Right:
            self.player_x += 20

        # 确保玩家不超出屏幕
        if self.player_x < 0:
            self.player_x = 0
        elif self.player_x > self.width - 50:
            self.player_x = self.width - 50

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())