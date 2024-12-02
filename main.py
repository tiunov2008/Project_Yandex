import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage, QColor, QTransform, QColorTransform
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QFileDialog, QLabel, QWidget

class ChessPiece(QLabel):
    def __init__(self, name):
        super().__init__()
        if name != 0:
            self.draw(name)
        else:
            self.clear()
    def draw(self, name):
        if name != 0:
            self.setMinimumSize(60, 60)
            curr_image = QImage()
            curr_image.load(name)
            pixmap = QPixmap().fromImage(curr_image)
            self.setPixmap(pixmap)
        else:
            self.clear()

class Chess(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('chess.ui', self)
        self.timer.hide()
        self.chessBoardBg.hide()
        self.playButton.clicked.connect(self.showTimer)
        self.startButton.clicked.connect(self.newGame)
        self.chessGrid.setSpacing(0)
        self.turn = 'w'
        self.selectedField = ()
        self.board = [['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],
                        ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],
                        ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw']]
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    self.chessGrid.addWidget(ChessPiece(self.board[i][j]), i, j)
                else:
                    self.chessGrid.addWidget(ChessPiece(0), i, j)
        self.newGame()

    def mousePressEvent(self, event):
        pos = event.pos()
        cords = ((pos.y() - 100) // 60, (pos.x() - 260) // 60)
        if event.button() == Qt.MouseButton.LeftButton and 0 <= cords[0] <= 7 and 0 <= cords[1] <= 7 and self.selectedField == () and self.board[cords[0]][cords[1]] != 0:
            self.selectedField = cords
        elif event.button() == Qt.MouseButton.LeftButton and 0 <= cords[0] <= 7 and 0 <= cords[1] <= 7 and self.selectedField != ():
            if self.canMove(self.selectedField, cords):
                self.movePiece(self.selectedField, cords)
                #self.next_turn()
            self.selectedField = ()
        
    def next_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
    def showTimer(self):
        self.timer.show()
        self.main.hide()
    def movePiece(self, p1, p2):
        a = self.board[p1[0]][p1[1]]
        self.board[p1[0]][p1[1]] = 0
        self.board[p2[0]][p2[1]] = a
        self.chessGrid.itemAtPosition(p1[0], p1[1]).widget().draw(0)
        self.chessGrid.itemAtPosition(p2[0], p2[1]).widget().draw(a)
    def newGame(self):
        self.main.hide()
        self.timer.hide()
        self.chessBoardBg.show()
        curr_image = QImage()
        curr_image.load('chessbg.png')
        pixmap = QPixmap().fromImage(curr_image)
        self.chessBoardBg.setPixmap(pixmap)
    def canMove(self, p1, p2):
        x1 = p1[1]
        y1 = p1[0]
        x2 = p2[1]
        y2 = p2[0]
        p = self.board[y1][x1]
        print(x1, y1, x2, y2)
        if p == 0 or p[1] != self.turn:
            return False
        elif p[0] == 'P':
            if self.board[y2][x2] == 0 and x1 == x2 and\
                ((p[1] == 'w' and (y1 - y2 == 1 or (y1 == 6 and y1 - y2 == 2))) or \
                (p[1] == 'b' and (y2 - y1 == 1 or (y1 == 1 and y2 - y1 == 2)))):
                return True
            if self.board[y2][x2] != 0 and abs(x1 - x2) == 1 and\
                ((p[1] == 'w' and y1 - y2 == 1) or \
                (p[1] == 'b' and y2 - y1 == 1)):
                return True
        elif p[0] == 'R':
            if x1 == x2 and y1 > y2 and (not any([self.board[i][x1] for i in range(y1 - 1, y2, -1)]) \
                                         or len([self.board[i][x1] for i in range(y1 - 1, y2, -1)]) == 0):
                return True
            elif x1 == x2 and y1 < y2 and (not any([self.board[i][x1] for i in range(y1 + 1, y2)]) \
                                           or len([self.board[i][x1] for i in range(y1 + 1, y2)]) == 0):
                return True
            elif y1 == y2 and x1 < x2 and (not any([self.board[y1][i] for i in range(x1 + 1, x2)]) \
                                           or len([self.board[y1][i] for i in range(x1 + 1, x2)]) == 0):
                return True
            elif y1 == y2 and x1 > x2 and (not all([self.board[y1][i] for i in range(x1 - 1, x2, -1)])\
                                           or len([self.board[y1][i] for i in range(x1 - 1, x2, -1)]) == 0):
                return True
        return False
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chess()
    ex.show()
    sys.excepthook = lambda a, b, c: sys.__excepthook__(a, b, c)
    sys.exit(app.exec())
