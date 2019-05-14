import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, 
QPushButton, QDesktopWidget, QHBoxLayout, QVBoxLayout, QGridLayout, 
QLabel, QLineEdit, QTextEdit, QRadioButton, QFileDialog)
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
        self.from_lineEdit = QLineEdit()
        self.from_lineEdit.setFixedWidth(320)
        self.from_lineEdit.setReadOnly(True)
        from_open_btn = QPushButton('open')
        from_open_btn.clicked.connect(self.openButtonClicked)
        self.isPdf = True
        self.openFilename = ""
        self.saveFilename = ""


        fromHBox = QHBoxLayout()
        fromHBox.addWidget(from_label)
        fromHBox.addStretch(2)
        fromHBox.addWidget(self.from_lineEdit)
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
        toHBox.addStretch(2)
        toHBox.addWidget(to_other_rbtn)
        toHBox.addStretch(5)

        ''' create secret (if click the others) '''
        self.to_lineEdit = QLineEdit()
        self.to_lineEdit.setFixedWidth(320)
        self.to_lineEdit.setReadOnly(True)
        self.to_lineEdit.setVisible(False)
  
        secretHBox = QHBoxLayout()
        secretHBox.addStretch(2)
        secretHBox.addWidget(self.to_lineEdit)
        secretHBox.addStretch(3)


        ''' create convert & quit button '''
        convert_btn = QPushButton('convert')
        #convert_btn.clicked.connect(QCoreApplication.instance().quit)
        quit_btn = QPushButton('quit')
        quit_btn.clicked.connect(QCoreApplication.instance().quit)

        bottomHBox = QHBoxLayout()
        bottomHBox.addStretch(5)
        bottomHBox.addWidget(convert_btn)
        bottomHBox.addWidget(quit_btn)
        # grid.addWidget(quit_btn, 2, 2)

        vbox = QVBoxLayout()
        vbox.addLayout(fromHBox)
        vbox.addLayout(toHBox)
        vbox.addLayout(secretHBox)
        vbox.addLayout(bottomHBox)

        self.setLayout(vbox)

        self.setWindowTitle('PDF & IMAGE Converter')
       # self.setWindowIcon(QIcon('pdf_image.png'))
        self.resize(500, 180)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Select File(PDF or IMG)', './', 'JPEG image or PDF (*.jpg *.pdf)')
        self.from_lineEdit.setText(fname[0])
        if '.pdf' in fname[0] :
            self.isPdf = True
        else: # jpg file.
            self.isPdf = False

    def radioButtonClicked(self):
        if self.to_same_rbtn.isChecked():
            self.to_lineEdit.setVisible(False)
            pass
        else:
            if self.isPdf :
                fname = QFileDialog.getSaveFileName(self, 'Save', './', 'JPEG image (*.jpg')
                self.to_lineEdit.setText(fname[0] + '.jpg')
            else:
                fname = QFileDialog.getSaveFileName(self, 'Save', './' , 'PDF (*.pdf')
                self.to_lineEdit.setText(fname[0] + '.pdf')
            self.to_lineEdit.setVisible(True)
    


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())