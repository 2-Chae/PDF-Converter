import sys
import threading
from fpdf import FPDF
from pdf2image import convert_from_path
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, 
QPushButton, QDesktopWidget, QHBoxLayout, QVBoxLayout, QGridLayout, 
QLabel, QLineEdit, QTextEdit, QRadioButton, QFileDialog, QMessageBox,
QStatusBar, QProgressBar)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtCore import pyqtSignal

__author__ = "Chaehyeon Lee <123456ccdd@naver.com>"

class MyAppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        self.myapp = MyApp(self)
        self.setCentralWidget(self.myapp)

        self.statusBar = QStatusBar(self)
        self.set_status_message('ready')
        self.setStatusBar(self.statusBar)
        self.setWindowTitle('PDF & IMAGE Converter')
        self.setWindowIcon(QIcon('pdf_image.png'))
        self.resize(500, 180)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_status_message(self, message):
        return self.statusBar.showMessage(message)

    def startTH(self):
        self.th.start()

class MyApp(QWidget):

    finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.finished.connect(self.end_convert)
        self.initUI()

    def initUI(self):

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
        self.openFilePath = ""
        self.openFilesPath = []

        self.saveFilename = ""
        self.saveFilePath = ""


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
        self.to_other_rbtn = QRadioButton('others', self)
        self.to_other_rbtn.clicked.connect(self.radioButtonClicked)

        toHBox = QHBoxLayout()
        toHBox.addWidget(to_label)
        toHBox.addStretch(1)
        toHBox.addWidget(self.to_same_rbtn)
        toHBox.addStretch(2)
        toHBox.addWidget(self.to_other_rbtn)
        toHBox.addStretch(5)

        ''' create secret (if click the others) '''
        self.to_lineEdit = QLineEdit()
        self.to_lineEdit.setFixedWidth(320)
        self.to_lineEdit.setReadOnly(False)
        self.to_lineEdit.setPlaceholderText('Save as (without extension like .jpg or .pdf)')

        secretHBox = QHBoxLayout()
        secretHBox.addStretch(2)
        secretHBox.addWidget(self.to_lineEdit)
        secretHBox.addStretch(3)


        ''' create convert & quit button '''
        self.convert_btn = QPushButton('convert')
        self.convert_btn.clicked.connect(self.convertButtonClicked)
        quit_btn = QPushButton('quit')
        quit_btn.clicked.connect(self.quit_button_click)

        bottomHBox = QHBoxLayout()
        bottomHBox.addStretch(5)
        bottomHBox.addWidget(self.convert_btn)
        bottomHBox.addWidget(quit_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(fromHBox)
        vbox.addLayout(toHBox)
        vbox.addLayout(secretHBox)
        vbox.addLayout(bottomHBox)

        self.setLayout(vbox)

    # save the openFilePath
    def openButtonClicked(self):
        fnames = QFileDialog.getOpenFileNames(self, 'Select File(PDF or IMG)', './', 'JPEG image or PDF (*.jpg *.pdf)')

        self.openFilesPath = fnames[0]
        if len(self.openFilesPath) == 0:
            return
        self.openFilename = fnames[0][0].split("/")[-1]

        # multiple files
        if len(self.openFilesPath) > 1: 
            self.from_lineEdit.setText(self.openFilesPath[0] + '...')
        else:
            self.from_lineEdit.setText(self.openFilesPath[0])

        if '.pdf' in self.openFilename:
            self.isPdf = True
        else: # jpg file.
            self.isPdf = False


    # save the saveFilePath
    def radioButtonClicked(self):
        # same direction
        if self.to_same_rbtn.isChecked():
            self.to_lineEdit.setReadOnly(False)
            self.to_lineEdit.setPlaceholderText('Save as (without extension like .jpg or .pdf)')
            return
        # others 
        else:
            self.to_lineEdit.setReadOnly(True)
            # this is pdf
            if self.isPdf :
                fname = QFileDialog.getSaveFileName(self, 'Save', './', 'JPEG image (*.jpg')
                self.saveFilePath = fname[0]
                if len(self.saveFilePath) == 0 :
                    return
                self.to_lineEdit.setText(fname[0] + '.jpg')
            # this is image
            else:
                fname = QFileDialog.getSaveFileName(self, 'Save', './' , 'PDF (*.pdf')
                self.saveFilePath = fname[0]
                if len(self.saveFilePath) == 0 :
                    return
                self.to_lineEdit.setText(fname[0] + '.pdf')
            self.to_lineEdit.setVisible(True)
    

    def convertButtonClicked(self):
        # to_lineEdit is empty
        if len(self.from_lineEdit.text()) == 0 :
            QMessageBox.about(self, "Alert", "Please select the file first!\nClick the open button.")
            return 

        if len(self.to_lineEdit.text()) == 0 and self.to_same_rbtn.isChecked():
            QMessageBox.about(self, "Alert", "Please type the file name first!")
            self.to_lineEdit.setFocus(True)
            return 

        if len(self.to_lineEdit.text()) == 0 and self.to_other_rbtn.isChecked():
            QMessageBox.about(self, "Alert", "Please select the directory first!\nClick the other button again.")
            return 

        self.parent.statusBar.showMessage('converting...')
        self.thread = threading.Thread(target=self.run_convert)
        self.thread.start()
        self.to_lineEdit.setReadOnly(True)
        self.convert_btn.setEnabled(False)
        
    def run_convert(self):
        # convert pdf to image
        i = 1
        if self.isPdf:
            pages = convert_from_path(self.openFilesPath[0], 500)
            for page in pages:
              page.save(self.to_lineEdit.text() + str(i) + '.jpg', 'JPEG')
              i += 1
        else:  # convert image to pdf
            pdf = FPDF()
            for image in self.openFilesPath :
                pdf.add_page()
                pdf.image(image,0,0,210,297)

            if '.pdf' in self.to_lineEdit.text():
                pdf.output(self.to_lineEdit.text(), 'F')
            else:
                 pdf.output(self.to_lineEdit.text() + '.pdf', 'F')
        
        self.finished.emit()


    def end_convert(self):
        self.parent.statusBar.showMessage('done!!')
        QMessageBox.information(self, "Done", "Done! Check your files! :)")
        self.init_everything()

       
    def init_everything(self):
         # Initiate!
        self.from_lineEdit.setText("")
        self.to_lineEdit.setText("")
        self.convert_btn.setEnabled(True)
        self.parent.statusBar.showMessage('ready')
        self.to_lineEdit.setReadOnly(False)


    def quit_button_click(self):
        done_msg = QMessageBox().question(self, "QUIT?", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if done_msg == QMessageBox.Yes:
            QCoreApplication.instance().quit()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyAppMainWindow()
    sys.exit(app.exec_())