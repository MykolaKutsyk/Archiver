import os
import pathlib
import shutil
import sys
import zipfile
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from check_db import *
from GUI.des import *
from GUI.archive import *

class Interface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.reg)
        self.ui.pushButton_2.clicked.connect(self.auth)
        self.ui.pushButton_2.clicked.connect(self.show_main_window)
        self.ui.pushButton_2.clicked.connect(self.close)

        self.base_line_edit = [self.ui.lineEdit, self.ui.lineEdit_2]

        self.check_db = CheckThread()
        self.check_db.mysignal.connect(self.signal_handler)


    def show_main_window(self):
        self.w2 = MainWindow()
        self.w2.show()

    # Перевірка правильності введення
    def check_input(funct):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if len(line_edit.text()) == 0:
                    return
            funct(self)
        return wrapper

    # Обробник сигналів
    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, 'Оповіщення', value)

    @check_input
    def auth(self):
        name = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()
        self.check_db.thr_login(name, passw)



    @check_input
    def reg(self):
        name = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()
        self.check_db.thr_register(name, passw)





class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.show_main)
        self.ui.pushButton.clicked.connect(self.close)

        self.ui.toolButton.clicked.connect(self.addFiles)
        self.ui.pushButton_3.clicked.connect(self.openFile)

        self.ui.pushButton_2.clicked.connect(self.saveFile)

    def openFile(self):
        if os.path.exists("directory.zip"):
            os.remove("directory.zip")


        zipname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , '*.zip')


        with zipfile.ZipFile(zipname) as z:
            z.extractall("openZIP")

        for root, dirs, files in os.walk("openZIP"):
            for filename in files:
                self.ui.listWidget.addItem(filename)

    def show_main(self):
        self.w = Interface()
        self.w.show()


    def addFiles(self):
        if os.path.exists("directory.zip"):
            os.remove("directory.zip")

        fname=QFileDialog.getOpenFileName(self, 'Open file', 'D:\codefirst.io\PyQt5 tutorials\Browse Files', 'All (*.*)')
        shutil.copy(fname[0], "openZIP")
        self.ui.listWidget.addItem(fname[0])


    def saveFile(self):
        directory = pathlib.Path("openZIP/")
        with zipfile.ZipFile("directory.zip", mode="w") as archive:
            for file_path in directory.iterdir():
                archive.write(file_path, arcname=file_path.name)

        for f in os.listdir("openZIP"):
            os.remove(os.path.join("openZIP", f))
        self.ui.listWidget.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('archiverIcon.png'))
    mywin = Interface()
    mywin.show()
    sys.exit(app.exec_())