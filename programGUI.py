import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, 
QPushButton, QDesktopWidget, QHBoxLayout, QVBoxLayout, QGridLayout, 
QLabel, QLineEdit, QTextEdit, QRadioButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # set grid layout
        # grid = QGridLayout()
        # self.setLayout(grid)

        ''' create from '''
        from_label = QLabel('From')
        from_label.setAlignment(Qt.AlignCenter)
        from_lineEdit = QLineEdit()
        from_lineEdit.setFixedWidth(130)
        from_open_btn = QPushButton('open')
        
        fromHBox = QHBoxLayout()
        fromHBox.addWidget(from_label)
        fromHBox.addStretch(1)
        fromHBox.addWidget(from_lineEdit)
        fromHBox.addStretch(2)
        fromHBox.addWidget(from_open_btn)

        ''' create to '''
        to_label = QLabel('To')
        to_label.setAlignment(Qt.AlignCenter)
        self.to_same_rbtn = QRadioButton('same directory', self)
        self.to_same_rbtn.setChecked(True)
        self.to_same_rbtn.clicked.connect(self.radioButtonClicked)
        to_other_rbtn = QRadioButton('others', self)
        to_other_rbtn.clicked.connect(self.radioButtonClicked)

        toHBox = QHBoxLayout()
        toHBox.addWidget(to_label)
        toHBox.addStretch(1)
        toHBox.addWidget(self.to_same_rbtn)
        toHBox.addStretch(1)
        toHBox.addWidget(to_other_rbtn)

        ''' create secret (if click the others) '''
        self.to_lineEdit = QLineEdit()
        self.to_lineEdit.setFixedWidth(130)
        to_open_btn = QPushButton('open')
  
        secretHBox = QHBoxLayout()
        secretHBox.addWidget(self.to_lineEdit)
        secretHBox.addWidget(to_open_btn)
        
        ''' create quit button '''
        quit_btn = QPushButton('quit')
        quit_btn.clicked.connect(QCoreApplication.instance().quit)


        quitHBox = QHBoxLayout()
        quitHBox.addStretch(5)
        quitHBox.addWidget(quit_btn)
        # grid.addWidget(quit_btn, 2, 2)

        vbox = QVBoxLayout()
        vbox.addLayout(fromHBox)
        vbox.addLayout(toHBox)
        vbox.addLayout(secretHBox)
        vbox.addLayout(quitHBox)

        self.setLayout(vbox)

        self.setWindowTitle('PDF & IMAGE Converter')
       # self.setWindowIcon(QIcon('pdf_image.png'))
        self.resize(300, 180)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def radioButtonClicked(self):
        if self.to_same_rbtn.isChecked():
            self.to_lineEdit.setVisible(False)
        else:
            self.to_lineEdit.setVisible(True)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())