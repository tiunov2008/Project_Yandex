import sys

from PyQt6 import uic, QtCore
from PyQt6.QtGui import QPainter, QPixmap, QImage, QColor, QTransform, QColorTransform
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QButtonGroup


class MyPillow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('chess.ui', self)
        '''name = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.curr_image = QImage()
        self.curr_image.load(name)
        self.pixmap = QPixmap().fromImage(self.curr_image)
        self.image.setPixmap(self.pixmap)'''
        self.timer.hide()
    def channel(self, button):
        if button.text() == 'R':
            self.curr_image.colorTransformed(QColorTransform(QColor(255, 0, 0)))
                    #self.curr_image.setPixelColor(x, y, QColor(255, *self.curr_image.pixelColor(x, y).getRgb()[1:]))
        if button.text() == 'G':
            for x in range(self.curr_image.width() - 1):
                for y in range(self.curr_image.height() - 1):
                    self.curr_image.setPixelColor(x, y, QColor(self.curr_image.pixelColor(x, y).getRgb()[0], 255, self.curr_image.pixelColor(x, y).getRgb()[2]))
        if button.text() == 'B':
            for x in range(self.curr_image.width() - 1):
                for y in range(self.curr_image.height() - 1):
                    self.curr_image.setPixelColor(x, y, QColor(*self.curr_image.pixelColor(x, y).getRgb()[:2], 255))
        self.pixmap = QPixmap().fromImage(self.curr_image)
        self.image.setPixmap(self.pixmap)
    def new_game():
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyPillow()
    ex.show()
    sys.exit(app.exec())
