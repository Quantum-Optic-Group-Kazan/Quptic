import sys, time
from PyQt5 import QtWidgets,QtCore
from GUI.ui_Quptic import Ui_MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    ui.kled.setValue(False)
    time.sleep(3)
    ui.kled.setValue(True)
    time.sleep(3)
    sys.exit(app.exec_())