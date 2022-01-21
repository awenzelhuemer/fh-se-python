import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(486, 597)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonAdd = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add_item())
        self.pushButtonAdd.setGeometry(QtCore.QRect(40, 80, 121, 31))
        self.pushButtonAdd.setObjectName("pushButton")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(40, 130, 401, 391))
        self.listWidget.setObjectName("listWidget")
        self.pushButtonDelete = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.delete_item())
        self.pushButtonDelete.setGeometry(QtCore.QRect(180, 80, 121, 31))
        self.pushButtonDelete.setObjectName("pushButton_2")
        self.pushButtonClear = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.clear_list())
        self.pushButtonClear.setGeometry(QtCore.QRect(320, 80, 121, 31))
        self.pushButtonClear.setObjectName("pushButton_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 20, 401, 31))
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 486, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.update_list()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ToDo List"))
        self.pushButtonAdd.setText(_translate("MainWindow", "Add Task"))
        self.pushButtonDelete.setText(_translate("MainWindow", "Delete Task"))
        self.pushButtonClear.setText(_translate("MainWindow", "Clear List"))

    def add_item(self):
        content = self.lineEdit.text()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('''insert into todo_list (list_item) values(?)''', [content])
        conn.commit()
        conn.close()
        self.listWidget.addItem(content)
        self.lineEdit.clear()
        self.update_list()

    def delete_item(self):
        item = self.listWidget.currentItem()
        if item is not None:
            tokens = item.text().split(' ')
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            c.execute('''delete from todo_list where id = (?)''', [tokens[0]])
            conn.commit()
            conn.close()

        self.update_list()

    def clear_list(self):
        self.listWidget.clear()

    def update_list(self):
        self.clear_list()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('''select * from todo_list''')
        items = c.fetchall()

        for item in items:
            self.listWidget.addItem(f"{item[0]} {item[1]}")

        c.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
