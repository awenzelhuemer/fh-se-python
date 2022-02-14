from PyQt5 import QtWidgets
import sys


class MyWindow(object):
    def setupUI(self, main_window):
        main_window.setGeometry(200, 200, 300, 300)
        main_window.setWindowTitle("GUI Example")

        self.label = QtWidgets.QLabel(main_window)
        self.label.setText("Example Label")
        self.label.move(50, 50)

        self.button = QtWidgets.QPushButton(main_window)
        self.button.setText("Click Me!")
        self.button.clicked.connect(self.clicked)

    def clicked(self):
        self.label.setText("You pressed the button")
        self.update()

    def update(self):
        self.label.adjustSize()


def window():
    app = QtWidgets.QApplication([])
    main_window = QtWidgets.QMainWindow()
    ui = MyWindow()
    ui.setupUI(main_window)

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()
