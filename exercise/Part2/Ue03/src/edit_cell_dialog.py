from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):

    def __init__(self, value):
        self.value = value

    def setupUi(self, Dialog):
        Dialog.setObjectName("Edit cell value")
        Dialog.resize(400, 72)
        self.dialogActions = QtWidgets.QDialogButtonBox(Dialog)
        self.dialogActions.setGeometry(QtCore.QRect(40, 30, 341, 32))
        self.dialogActions.setOrientation(QtCore.Qt.Horizontal)
        self.dialogActions.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dialogActions.setObjectName("dialogActions")
        self.txtValue = QtWidgets.QLineEdit(Dialog)
        self.txtValue.setGeometry(QtCore.QRect(20, 10, 361, 20))
        self.txtValue.setObjectName("txtValue")
        self.txtValue.setText(self.value)

        self.retranslateUi(Dialog)
        self.dialogActions.accepted.connect(Dialog.accept) # type: ignore
        self.dialogActions.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

    def updated_text(self):
        return self.txtValue.text()
