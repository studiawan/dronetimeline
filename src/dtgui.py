import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    qApp,
    QApplication,
    QFileDialog,
    QMessageBox,
    QMdiArea
)
from PyQt5 import QtGui
from DtGUI import host as DtGUI_Pluggin

def main():
    app = QApplication(sys.argv)
    _ = DtGUI_Pluggin.DtGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
