import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(628, 597)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add_item())
        self.addButton.setGeometry(QtCore.QRect(40, 80, 121, 31))
        self.addButton.setObjectName("addButton")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(40, 130, 541, 391))
        self.listWidget.setObjectName("listWidget")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.delete_item())
        self.deleteButton.setGeometry(QtCore.QRect(180, 80, 121, 31))
        self.deleteButton.setObjectName("deleteButton")
        self.clearButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.clear_items())
        self.clearButton.setGeometry(QtCore.QRect(320, 80, 121, 31))
        self.clearButton.setObjectName("clearButton")
        self.taskText = QtWidgets.QLineEdit(self.centralwidget)
        self.taskText.setGeometry(QtCore.QRect(40, 20, 541, 31))
        self.taskText.setObjectName("taskText")
        self.editButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.update_item())
        self.editButton.setGeometry(QtCore.QRect(460, 80, 121, 31))
        self.editButton.setObjectName("editButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 628, 21))
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
        self.addButton.setText(_translate("MainWindow", "Add Task"))
        self.deleteButton.setText(_translate("MainWindow", "Delete Task"))
        self.clearButton.setText(_translate("MainWindow", "Clear List"))
        self.editButton.setText(_translate("MainWindow", "Edit Task"))

    def add_item(self):
        content = self.taskText.text()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('''insert into todo_list (list_item) values(?)''', [content])
        conn.commit()
        conn.close()
        self.listWidget.addItem(content)
        self.taskText.clear()
        self.update_list()

    def update_item(self):
        content = self.taskText.text()
        item = self.listWidget.currentItem()
        if content is not None and item is not None:
            tokens = item.text().split(' ')
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            c.execute('''update todo_list set list_item = ? where id = ?''', [content, tokens[0]])
            conn.commit()
            conn.close()
            self.taskText.clear()
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

    def clear_items(self):
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('''delete from todo_list''')
        conn.commit()
        conn.close()
        self.update_list()

    def update_list(self):
        self.listWidget.clear()
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
