import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, 
QPushButton, QDesktopWidget, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QTextEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # set grid layout
        grid = QGridLayout()
        self.setLayout(grid)


        # fromBox = QHBoxLayout()
        # fromBox.addStretch()
        
        from_label = QLabel('From')
        from_label.setAlignment(Qt.AlignCenter)
        to_label = QLabel('to')
        to_label.setAlignment(Qt.AlignCenter)

        grid.addWidget(from_label, 0, 0)
        grid.addWidget(to_label, 1, 0)
        

        quit_btn = QPushButton('quit')
        quit_btn.clicked.connect(QCoreApplication.instance().quit)
        #btn.resize(30, 10)

        grid.addWidget(quit_btn, 2, 2)

        grid.addWidget(QLineEdit(), 0, 1);
        grid.addWidget(QLineEdit(), 1, 1);

        open_btn = QPushButton('open')
        grid.addWidget(open_btn, 0, 2)
        

        self.setWindowTitle('PDF & IMAGE Converter')
       # self.setWindowIcon(QIcon('pdf_image.png'))
        self.resize(300, 200)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())