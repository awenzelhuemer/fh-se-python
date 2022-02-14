import os
import pathlib

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog

import detail_dialog
import file_helper


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 577)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listView = QtWidgets.QListWidget(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 40, 781, 511))
        self.listView.setObjectName("lvFile")
        self.listView.doubleClicked.connect(self.show_details)
        self.btnAddFile = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add())
        self.btnAddFile.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.btnAddFile.setObjectName("btnAddFile")
        self.btnDelete = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.delete())
        self.btnDelete.setGeometry(QtCore.QRect(520, 10, 101, 23))
        self.btnDelete.setObjectName("btnDelete")
        self.btnExport = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.export())
        self.btnExport.setGeometry(QtCore.QRect(710, 10, 75, 23))
        self.btnExport.setObjectName("btnExport")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(630, 10, 69, 22))
        self.comboBox.setObjectName("comboBox")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.init()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnAddFile.setText(_translate("MainWindow", "Add File"))
        self.btnDelete.setText(_translate("MainWindow", "Delete"))
        self.btnExport.setText(_translate("MainWindow", "Export"))

    def init(self):
        self.update_list()
        self.comboBox.addItems(file_helper.filetypes)

    def update_list(self):
        self.listView.clear()

        self.listView.addItems(file_helper.get_files())

    def export(self):
        if self.listView.currentItem() is not None:
            file_type = self.comboBox.currentText()
            source_filename = self.listView.currentItem().text()

            filename = os.path.join(file_helper.output_directory, source_filename)
            filepath = pathlib.Path(filename)
            source_filetype = filepath.suffix
            df = file_helper.parse_file(filename, source_filetype)
            target_file_name = f"{filepath.stem}{file_type}"
            file_helper.get_dataframe(source_filename)
            file_helper.save_file(df, target_file_name, file_type, target_directory='export')

    def add(self):
        full_filename = QFileDialog.getOpenFileName(self.btnAddFile, 'Open file')[0]

        try:
            if full_filename == '':
                raise ValueError('No file specified')
            else:
                filepath = pathlib.Path(full_filename)
                target_filename = filepath.name
                file_type = filepath.suffix
                if file_type not in file_helper.filetypes:
                    raise ValueError(f'File {target_filename} has invalid type')
            df = file_helper.parse_file(full_filename, file_type)
            file_helper.save_file(df, target_filename, file_type)
            self.update_list()
        except ValueError as e:
            print(f'Error: {e}')
        except BaseException as e:
            print(f'Exception details: {e}')

    def delete(self):
        if self.listView.currentItem() is not None:
            file_helper.remove_file(self.listView.currentItem().text())
            self.update_list()

    def show_details(self):
        dialog = QDialog()
        dialog.ui = detail_dialog.Ui_Dialog(self.listView.currentItem().text())
        dialog.ui.setupUi(dialog)
        dialog.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

