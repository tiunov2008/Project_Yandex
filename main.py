import sys

from PyQt6 import uic, QtCore
from PyQt6.QtGui import QPainter, QPixmap, QImage, QColor, QTransform, QColorTransform
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QFileDialog, QLabel, QWidget


class Pawn(QLabel):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(60, 60)
        curr_image = QImage()
        curr_image.load('Pb.png')
        pixmap = QPixmap().fromImage(curr_image)
        self.setPixmap(pixmap)


class Chess(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('chess.ui', self)
        '''name = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.curr_image = QImage()
        self.curr_image.load(name)
        self.pixmap = QPixmap().fromImage(self.curr_image)
        self.image.setPixmap(self.pixmap)'''
        self.timer.hide()
        self.chessBoardBg.hide()
        self.playButton.clicked.connect(self.showTimer)
        self.startButton.clicked.connect(self.newGame)
        self.chessGrid.setSpacing(0)
        '''self.board = [['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],
                      ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],
                      ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw']]'''
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                      ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    self.chessGrid.addWidget(Pawn(), i, j)
                else:
                    self.chessGrid.addWidget(QWidget(), i, j)
        self.newGame()
    def showTimer(self):
        self.timer.show()
        self.main.hide()
    def newGame(self):
        self.main.hide()
        self.timer.hide()
        self.chessBoardBg.show()
        curr_image = QImage()
        curr_image.load('chessbg.png')
        pixmap = QPixmap().fromImage(curr_image)
        self.chessBoardBg.setPixmap(pixmap)
    def move(self, x1, y1, x2, y2):
        pass

    def updateBoard(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chess()
    ex.show()
    sys.exit(app.exec())
