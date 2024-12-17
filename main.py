import sys
from PyQt6 import uic
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPixmap, QImage, QColor, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QTableWidgetItem, QButtonGroup, QFileDialog
from chesslogic import ChessLogic
from gamespage import GamesPage
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
class ChessPieceBtn(QPushButton):
    def __init__(self, name):
        super().__init__()
        self.setIcon(QIcon(name))
        self.setMinimumSize(60, 60)
        self.setIconSize(QSize(60, 60))

class TimerPage(QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        uic.loadUi('timerpage.ui', self)
        self.MainWindow = MainWindow
        self.playButton.clicked.connect(self.checkTimer)
    def checkTimer(self):
        text = self.timerInput.text()
        if text != '' and text.isnumeric():
            self.MainWindow.setCentralWidget(ChessPage(int(text)))
        else:
            self.MainWindow.setCentralWidget(ChessPage(0))
class ChessPage(QWidget, ChessLogic):
    def __init__(self, time, game=False):
        super().__init__()
        uic.loadUi('newchess.ui', self)
        self.chessGrid.setSpacing(0)
        self.turn = 'w'
        self.time = time
        self.selectedField = ()
        self.alph = 'abcdefgh'
        self.move_count = 0
        if game:
            self.gameGoing = False
            self.moves = []
            moves_pgn = game.mainline_moves()
            for move in moves_pgn:
                move = move.uci()
                print(self.alph.index(move[0]))
                self.moves.append(((8 - int(move[1]), self.alph.index(move[0])), (8 - int(move[3]), self.alph.index(move[2]))))
            self.nextBtn.clicked.connect(self.nextMove)
        else:
            self.gameGoing = True
            self.nav.hide()
        self.board = [['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],
            ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],
            ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw']]
        self.newGame()
    def mousePressEvent(self, event):
        if self.gameGoing:
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
                    self.isCheckMate()
                else:
                    self.chessGrid.itemAtPosition(self.selectedField[0], self.selectedField[1]).widget().clearSelect()
                self.selectedField = ()
    def toChessCords(self, i, j):
        return (j + 1, 8 - i)
    def toIJCords(self, x, y):
        return (8 - y, x - 1)
    def isInDanger(self, i1, j1):
        for i in range(8):
            for j in range(8):
                if self.canMove((j, i), (i1, j1)):
                    return True
    def isCheckMate(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'Kb':
                    Kb = (i, j)
                if self.board[i][j] == 'Kw':
                    Kw = (i, j)
        print(self.isInDanger(*Kb))
        if self.isInDanger(*Kb):
            print('Шах черным')
            for i in range(Kb[0] - 1, Kb[0] + 1):
                for j in range(Kb[1] - 1, Kb[1] + 1):
                    print(self.board[i][j])
                    if not (self.board[i][j] != 0 and self.isInDanger(i, j)):
                        return False
            print('Шам и Мат черный')
        if self.isInDanger(*Kw):
            print('Шах белым')
                    
    def next_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
    def nextMove(self):
        if self.move_count < len(self.moves):
            self.movePiece(*self.moves[self.move_count])
            self.move_count += 1
    def movePiece(self, p1, p2):
        a = self.board[p1[0]][p1[1]]
        self.board[p1[0]][p1[1]] = 0
        self.board[p2[0]][p2[1]] = a
        self.chessGrid.itemAtPosition(p1[0], p1[1]).widget().draw(0)
        self.chessGrid.itemAtPosition(p2[0], p2[1]).widget().draw(a)
        if a != 0 and a[0] == 'P' and (p2[0] == 0 or p2[0] == 7):
            self.promotePawn(*p2)
    def promotePawn(self, x, y):
        self.promotePawnW.show()
        self.promotePawnGroup = QButtonGroup()
        promotePawnList = ['Rw', 'Nw', 'Bw', 'Qw']
        for i in range(4):
            btn = ChessPieceBtn(promotePawnList[i])
            self.promotePawnBox.addWidget(btn)
            self.promotePawnGroup.addButton(btn)
            self.promotePawnGroup.setId(btn, i)
        self.promotePawnGroup.buttonClicked.connect(lambda g: self.promote(g, x, y))
    def promote(self, btn, x, y):
        promotePawnList = ['Rw', 'Nw', 'Bw', 'Qw']
        a = self.promotePawnGroup.id(btn)
        self.board[x][y] = 0
        self.board[x][y] = promotePawnList[a]
        self.chessGrid.itemAtPosition(x, y).widget().draw(0)
        self.chessGrid.itemAtPosition(x, y).widget().draw(promotePawnList[a])
        self.promotePawnW.hide()
    def startTimer(self):
        self.btime = self.time * 60
        self.wtime = self.time * 60
        self.bTimer = QTimer(self)
        self.wTimer = QTimer(self)
        self.bTimer.start(1000)
        self.wTimer.start(1000)
        self.wTimer.timeout.connect(self.updateTimer)
    def updateTimer(self):
        if self.turn == 'b':
            self.btime -= 1
            self.blackTimer.setText(f'{self.btime // 60}:{self.btime % 60}')
        else:
            self.wtime -= 1
            self.whiteTimer.setText(f'{self.wtime // 60}:{self.wtime % 60}')
        if self.wtime <= 0:
            self.endGame('w')
        elif self.btime <= 0:
            self.endGame('b')
    def newGame(self):
        self.promotePawnW.hide()
        self.game = True
        if self.time != 0:
            self.blackTimer.setText(f'{self.time}:00')
            self.whiteTimer.setText(f'{self.time}:00')
        else:
            self.blackTimer.hide()
            self.whiteTimer.hide()
        curr_image = QImage()
        curr_image.load('chessbg.png')
        pixmap = QPixmap().fromImage(curr_image)
        self.chessBoardBg.setPixmap(pixmap)
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    self.chessGrid.addWidget(ChessPiece(self.board[i][j]), i, j)
                else:
                    self.chessGrid.addWidget(ChessPiece(0), i, j)
        if self.time != 0:
            self.startTimer()

    def endGame(self, winner):
        pass
class MainPage(QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        uic.loadUi('mainpage.ui', self)
        self.playButton.clicked.connect(lambda: MainWindow.setCentralWidget(TimerPage(MainWindow)))
        self.gamesManager.clicked.connect(lambda: MainWindow.setCentralWidget(GamesPage(MainWindow)))

class Chess(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(MainPage(self))
        self.resize(1000, 800)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chess()
    ex.show()
    sys.excepthook = lambda a, b, c: sys.__excepthook__(a, b, c)
    sys.exit(app.exec())
