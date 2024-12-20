import sys
import datetime
import chess
from PyQt6 import uic
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPixmap, QImage, QColor, QIcon
from PyQt6.QtWidgets import QApplication, QLineEdit, QDialogButtonBox, QVBoxLayout, QLabel, QWidget, QPushButton, QDialog, QButtonGroup, QFileDialog
from chesslogic import ChessLogic
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
class SaveGameDialog(QDialog):
    def __init__(self, winner):
        super().__init__()
        self.setWindowTitle("Сохранить игру")
        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        label1 = QLabel("Игрок 1")
        self.player1 = QLineEdit()
        label2 = QLabel("Игрок 2")
        self.player2 = QLineEdit()
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        if winner == 'w':
            message1 = QLabel("Белые победили!")
        elif winner == 'b':
            message1 = QLabel("Черные победили!")
        else:
            message1 = QLabel("Ничья!")
        message2 = QLabel("Вы хотите сохранить игру?")
        layout.addWidget(message1)  
        layout.addWidget(label1)  
        layout.addWidget(self.player1)
        layout.addWidget(label2)  
        layout.addWidget(self.player2)
        layout.addWidget(message2)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
class ChessPage(QWidget, ChessLogic):
    def __init__(self, time, loadgame=False):
        super().__init__()
        uic.loadUi('newchess.ui', self)
        self.chessGrid.setSpacing(0)
        self.turn = 'w'
        self.time = time
        self.selectedField = ()
        self.alph = 'abcdefgh'
        self.move_count = 1
        self.moves = ''
        self.cmove = ''
        self.game = chess.Board()
        if loadgame:
            self.gameGoing = False
            self.loadgame = loadgame
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
    def check_move_from_to_tentative(self, from_square, to_square):
        for m in self.game.legal_moves:
            if m.from_square == from_square and m.to_square == to_square:
                return True
        return False
    
    def doMove(self, uciMove):
        self.cmove = chess.Move.from_uci(uciMove)
        self.selectedField = self.fromChessCords(uciMove[:2])
        cords = self.fromChessCords(uciMove[2:])
        if not self.gameGoing or self.check_move_from_to_tentative(chess.parse_square(uciMove[:2]), chess.parse_square(uciMove[2:])):
            self.movePiece(self.selectedField, cords)
            if self.board[cords[0]][cords[1]].lower()[0] == 'p' and (cords[0] == 0 or cords[0] == 7):
                self.promotePawn(cords[0], cords[1])
            if self.game.is_queenside_castling(self.cmove):
                self.movePiece((self.selectedField[0], 0), (self.selectedField[0], 3))
            elif self.game.is_kingside_castling(self.cmove):
                self.movePiece((self.selectedField[0], 7), (self.selectedField[0], 5))
            elif self.game.is_en_passant(self.cmove):
                if self.turn == 'w':
                    i = 1
                else:
                    i = -1
                self.chessGrid.itemAtPosition(cords[0] + i, cords[1]).widget().draw(0)
                self.board[cords[0] + i][cords[1]] = 0
            self.chessGrid.itemAtPosition(self.selectedField[0], self.selectedField[1]).widget().draw(0)
            self.game.push(self.cmove)
            self.cmove = ''
            if self.game.is_stalemate() and self.gameGoing:
                self.endGame('s')
            if self.game.is_checkmate() and self.gameGoing:
                self.endGame(self.turn)
            self.next_turn()
        else:
            self.chessGrid.itemAtPosition(self.selectedField[0], self.selectedField[1]).widget().clearSelect()
        self.selectedField = ()
    def mousePressEvent(self, event):
        if self.gameGoing:
            pos = event.pos()
            cords = ((pos.y() - 100) // 60, (pos.x() - 260) // 60)
            if event.button() == Qt.MouseButton.LeftButton and 0 <= cords[0] <= 7 and 0 <= cords[1] <= 7 and self.selectedField == () and self.board[cords[0]][cords[1]] != 0 and self.board[cords[0]][cords[1]][1] == self.turn:
                self.selectedField = cords
                self.chessGrid.itemAtPosition(cords[0], cords[1]).widget().setSelect()
            elif event.button() == Qt.MouseButton.LeftButton and 0 <= cords[0] <= 7 and 0 <= cords[1] <= 7 and self.selectedField != () and self.selectedField != cords:
                self.doMove(self.getMove(self.selectedField, cords))
    def toChessCords(self, i, j):
        return self.alph[j] + str(8 - i)
    def fromChessCords(self, x):
        return (8 - int(x[1]), self.alph.index(x[0]))
    def next_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
    def nextMove(self):
        self.move_count = 0
        for i in self.loadgame.mainline_moves():
            self.doMove(i.uci())
        self.move_count += 1
    def getMove(self, p1, p2):
        return f'{self.toChessCords(p1[0], p1[1])}{self.toChessCords(p2[0], p2[1])}'
    def movePiece(self, p1, p2):
        a = self.board[p1[0]][p1[1]]
        self.board[p1[0]][p1[1]] = 0
        self.board[p2[0]][p2[1]] = a
        self.chessGrid.itemAtPosition(p1[0], p1[1]).widget().draw(0)
        self.chessGrid.itemAtPosition(p2[0], p2[1]).widget().draw(a)
    def promotePawn(self, x, y):
        self.promotePawnW.show()
        self.promotePawnGroup.buttonClicked.connect(lambda g: self.promote(g, x, y))
    def promote(self, btn, x, y):
        promotePawnList = ['R', 'N', 'B', 'Q']
        a = self.promotePawnGroup.id(btn)
        self.board[x][y] = 0
        self.chessGrid.itemAtPosition(x, y).widget().draw(0)
        if self.turn == 'w':
            self.chessGrid.itemAtPosition(x, y).widget().draw(promotePawnList[a] + 'b')
            self.board[x][y] = promotePawnList[a] + 'b'
            p = chess.Piece.from_symbol(promotePawnList[a].lower())
        else:
            self.chessGrid.itemAtPosition(x, y).widget().draw(promotePawnList[a] + 'w')
            self.board[x][y] = promotePawnList[a] + 'w'
            p = chess.Piece.from_symbol(promotePawnList[a])
        self.game.set_piece_at(chess.parse_square(self.toChessCords(x, y)), p)
        self.cmove += promotePawnList[a]
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
            self.endGame('b')
        elif self.btime <= 0:
            self.endGame('w')
    def newGame(self):
        self.promotePawnW.hide()
        self.promotePawnGroup = QButtonGroup()
        promotePawnList = ['Rw', 'Nw', 'Bw', 'Qw']
        for i in range(4):
            btn = ChessPieceBtn(promotePawnList[i])
            self.promotePawnBox.addWidget(btn)
            self.promotePawnGroup.addButton(btn)
            self.promotePawnGroup.setId(btn, i)
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
        dlg = SaveGameDialog(winner)
        if dlg.exec():
            path = QFileDialog.getExistingDirectory(
                self,
                "Select directory",
                ''
            )
            game = chess.pgn.Game.from_board(self.game)
            game.headers['Black'] = dlg.player1.text()
            game.headers['White'] = dlg.player2.text()
            game.headers['Date'] = str(datetime.date.today()).replace('-', '.')
            new_pgn = open(f'{path}/game.pgn', "w", encoding="utf-8")
            exporter = chess.pgn.FileExporter(new_pgn)
            game.accept(exporter)
