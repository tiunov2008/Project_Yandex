from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QFileDialog
import sqlite3
import chess.pgn
from PyQt6 import uic
class GamesPage(QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        uic.loadUi('gamespage.ui', self)
        self.MainWindow = MainWindow
        self.con = sqlite3.connect('chess.db')
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["White", "Black", "Winner"])
        try:
            self.con.execute("""CREATE TABLE chess
                     (id integer primary key autoincrement, white, black, winner, path, inFileId)""")
        except:
            rows = self.con.execute('''SELECT * FROM chess ''').fetchall()
            for row in rows:
                i = self.table.rowCount()
                self.table.insertRow(i)
                self.table.setItem(i, 0, QTableWidgetItem(row[1]))
                self.table.setItem(i, 1, QTableWidgetItem(row[2]))
                self.table.setItem(i, 2, QTableWidgetItem(row[3]))
        self.addGame.clicked.connect(self.addFile)
        self.deleteGame.clicked.connect(self.deleteFile)
        self.runGame.clicked.connect(self.startGame)
    def addFile(self):
        name = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "PGN Files (*.pgn)",
        )
        pgn = open(name[0])
        game = chess.pgn.read_game(pgn)
        while game is not None:
            white_name = game.headers['White']
            black_name = game.headers['Black']
            print(str(game).split(' \n'))
            break
            p1 = game.headers['Result'].split('-')[0]
            if p1 == '1':
                winner = 'White'
            else:
                winner = 'Black'
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            self.table.setItem(rowPosition, 0, QTableWidgetItem(white_name))
            self.table.setItem(rowPosition, 1, QTableWidgetItem(black_name))
            self.table.setItem(rowPosition, 2, QTableWidgetItem(winner))
            self.con.execute(f"""INSERT INTO chess(white, black, winner, path) values("{white_name}", "{black_name}", "{winner}", '{name[0]}')""")
            game = chess.pgn.read_game(pgn)
        self.con.commit()
    def deleteFile(self):
        self.table.removeRow(self.table.currentRow())
    def startGame(self):
        name = self.con.execute(f"""SELECT (path, inFileId) FROM chess WHERE id = {self.table.currentRow() + 1}""").fetchall()
        pgn = open(name[0])
        if name[1] is not None:
            for _ in range(name[1] - 1):
                game = chess.pgn.read_game(pgn)
        game = chess.pgn.read_game(pgn)
        self.MainWindow.setCentralWidget(ChessPage(0, game, name[1]))