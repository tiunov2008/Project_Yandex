import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage, QColor, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

class ChessPiece(QLabel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.setMinimumSize(60, 60)
        if name != 0:
            self.draw(name)
        else:
            self.clear()
    def draw(self, name):
        self.name = name
        if name != 0:
            curr_image = QImage()
            curr_image.load(name)
            pixmap = QPixmap().fromImage(curr_image)
            self.setPixmap(pixmap)
        else:
            self.clear()
    def setSelect(self):
        if self.name != 0:
            curr_image = QImage()
            curr_image.load(self.name)
            for x in range(curr_image.width() - 1):
                for y in range(curr_image.height() - 1):
                    if curr_image.pixelColor(x, y).getRgb()[3] == 0:
                        curr_image.setPixelColor(x, y, QColor(0, 100, 0, 60))
            pixmap = QPixmap(60, 60).fromImage(curr_image)
            self.setPixmap(pixmap)
    def clearSelect(self):
        self.draw(self.name)
class Chess(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('chess.ui', self)
        self.timer.hide()
        self.chessBoardBg.hide()
        self.blackTimer.hide()
        self.whiteTimer.hide()
        self.playButton.clicked.connect(self.showTimer)
        self.chessGrid.setSpacing(0)
        self.turn = 'w'
        self.selectedField = ()
        self.game = False

    def mousePressEvent(self, event):
        if self.game:
            pos = event.pos()
            cords = ((pos.y() - 100) // 60, (pos.x() - 260) // 60)
            if event.button() == Qt.MouseButton.LeftButton and 0 <= cords[0] <= 7 and 0 <= cords[1] <= 7 and self.selectedField == () and self.board[cords[0]][cords[1]] != 0 and self.board[cords[0]][cords[1]][1] == self.turn:
                self.selectedField = cords
                self.chessGrid.itemAtPosition(cords[0], cords[1]).widget().setSelect()
            elif event.button() == Qt.MouseButton.LeftButton and 0 <= cords[0] <= 7 and 0 <= cords[1] <= 7 and self.selectedField != ():
                if self.canMove(self.selectedField, cords):
                    self.movePiece(self.selectedField, cords)
                    self.next_turn()
                    self.chessGrid.itemAtPosition(self.selectedField[0], self.selectedField[1]).widget().draw(0)
                else:
                    self.chessGrid.itemAtPosition(self.selectedField[0], self.selectedField[1]).widget().clearSelect()
                self.selectedField = ()
        
    def next_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
    def showTimer(self):
        self.timer.show()
        self.startButton.clicked.connect(self.checkTimer)
        self.main.hide()
    def checkTimer(self):
        text = self.timerText.text()
        if text != '' and text.isnumeric():
            self.btime = int(text) * 60
            self.wtime = int(text) * 60
            self.bTimer = QTimer(self)
            self.wTimer = QTimer(self)
            self.bTimer.start(1000)
            self.wTimer.start(1000)
            self.wTimer.timeout.connect(self.updateTimer)
            self.newGame()
        else:
            self.btime = False
            self.newGame()
    def updateTimer(self):
        if self.turn == 'b':
            self.btime -= 1
            self.blackTimer.setText(f'{self.btime // 60}:{self.btime % 60}')
        else:
            self.wtime -= 1
            self.whiteTimer.setText(f'{self.wtime // 60}:{self.wtime % 60}')
    def movePiece(self, p1, p2):
        a = self.board[p1[0]][p1[1]]
        self.board[p1[0]][p1[1]] = 0
        self.board[p2[0]][p2[1]] = a
        self.chessGrid.itemAtPosition(p1[0], p1[1]).widget().draw(0)
        self.chessGrid.itemAtPosition(p2[0], p2[1]).widget().draw(a)
    def newGame(self):
        self.game = True
        self.main.hide()
        self.timer.hide()
        self.chessBoardBg.show()
        if self.btime != False:
            self.blackTimer.show()
            self.whiteTimer.show()
            self.blackTimer.setText(f'{self.btime // 60}:{self.btime % 60}')
            self.whiteTimer.setText(f'{self.wtime // 60}:{self.wtime % 60}')
        curr_image = QImage()
        curr_image.load('chessbg.png')
        pixmap = QPixmap().fromImage(curr_image)
        self.chessBoardBg.setPixmap(pixmap)
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
    def canBishop(self, x1, y1, x2, y2):
        if abs(x2 - x1) != abs(y2 - y1):
            return False
        i = (y2 - y1) // abs(y2 - y1)
        j = (x2 - x1) // abs(x2 - x1)
        x1 += j
        y1 += i
        while x1 != x2 and y1 != y2:
            if self.board[y1][x1] != 0:
                return False
            x1 += j
            y1 += i
        return True
    def canRook(self, x1, y1, x2, y2):
        if x2 == x1:
            i = (y2 - y1) // abs(y2 - y1)
            j = 0
        elif y2 == y1:
            j = (x2 - x1) // abs(x2 - x1)
            i = 0
        else:
            return False
        x1 += j
        y1 += i
        while x1 != x2 or y1 != y2:
            if self.board[y1][x1] != 0:
                return False
            x1 += j
            y1 += i
        return True
    def canMove(self, p1, p2):
        x1 = p1[1]
        y1 = p1[0]
        x2 = p2[1]
        y2 = p2[0]
        p = self.board[y1][x1]
        if p == 0 or p[1] != self.turn or (self.board[y2][x2] != 0 and self.board[y2][x2][1] == self.turn) or (x1 == x2 and y1 == y2):
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
            return self.canRook(x1, y1, x2, y2)
        elif p[0] == 'B':
            return self.canBishop(x1, y1, x2, y2)
        elif p[0] == 'Q':
            return self.canRook(x1, y1, x2, y2) or self.canBishop(x1, y1, x2, y2)
        elif p[0] == 'K':
            if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                return True
        elif p[0] == 'N':
            if (abs(x1 - x2) == 2 and abs(y1 - y2) == 1) or (abs(x1 - x2) == 1 and abs(y1 - y2) == 2):
                return True
        return False
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chess()
    ex.show()
    sys.excepthook = lambda a, b, c: sys.__excepthook__(a, b, c)
    sys.exit(app.exec())
