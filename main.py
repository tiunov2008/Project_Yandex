import sys
from PyQt6 import uic
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPixmap, QImage, QColor, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialogButtonBox, QVBoxLayout, QLabel, QWidget, QPushButton, QDialog, QButtonGroup, QFileDialog
from chesslogic import ChessLogic
from chesspage import ChessPage
from gamespage import GamesPage


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
