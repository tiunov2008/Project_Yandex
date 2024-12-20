import io
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QFileDialog
import sqlite3
import chess.pgn
from PyQt6 import uic

from chesspage import ChessPage

class GamesPage(QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        uic.loadUi('gamespage.ui', self)
        self.MainWindow = MainWindow
        self.con = sqlite3.connect('chess.db')
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["White", "Black", "Winner", 'ID'])
        try:
            self.con.execute("""CREATE TABLE chess
                     (id integer primary key autoincrement, white, black, winner, datakeys, datavalues, moves)""")
        except:
            self.loadFromDB()
        self.addGame.clicked.connect(self.addFile)
        self.deleteGame.clicked.connect(self.deleteFile)
        self.runGame.clicked.connect(self.startGame)
    def loadFromDB(self):
        while self.table.rowCount() > 0:
            self.table.removeRow(0)
        rows = self.con.execute('''SELECT * FROM chess ''').fetchall()
        for row in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(row[1]))
            self.table.setItem(i, 1, QTableWidgetItem(row[2]))
            self.table.setItem(i, 2, QTableWidgetItem(row[3]))
            self.table.setItem(i, 3, QTableWidgetItem(str(row[0])))
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
            p1 = game.headers['Result'].split('-')[0]
            p2 = game.headers['Result'].split('-')[1]
            if p1 == '1':
                winner = 'White'
            elif p2 == '1':
                winner = 'Black'
            elif p1 == '1/2':
                winner = 'Draw'
            self.con.execute(f"""INSERT INTO chess(white, black, winner, datakeys, datavalues, moves) values("{white_name}", "{black_name}", "{winner}", "{':'.join(list(game.headers))}", "{':'.join(list(game.headers.values()))}", "{str(game.mainline_moves())}")""")
            game = chess.pgn.read_game(pgn)
        self.con.commit()
        self.loadFromDB()
    def deleteFile(self):
        self.con.execute(f"""DELETE FROM chess WHERE id = '{self.table.item(self.table.currentRow(), 3).text()}'""").fetchall()
        self.table.removeRow(self.table.currentRow())
        self.con.commit()
    def startGame(self):
        moves = self.con.execute(f"""SELECT * FROM chess WHERE id = {self.table.item(self.table.currentRow(), 3).text()}""").fetchall()
        pgn = io.StringIO(moves[0][6])
        game = chess.pgn.read_game(pgn)
        self.MainWindow.setCentralWidget(ChessPage(0, game, moves[0][3]))