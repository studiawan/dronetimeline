import DtGUI
from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    qApp,
    QApplication,
    QFileDialog,
    QMessageBox,
    QMdiArea
)

@DtGUI.hookimpl
def init_menu(DtGUIObj):
    # application menu
    menubar = DtGUIObj.menuBar()

    # File menu
    new_menu = menubar.addMenu('&New Customized Menu')
    
    # File menu action - New Case
    newmenu_act = QAction('&Select something', DtGUIObj)
    newmenu_act.setShortcut('Ctrl+P')
    newmenu_act.setStatusTip('Select something')
    newmenu_act.triggered.connect(DtGUIObj.open_directory_dialog)
    new_menu.addAction(newmenu_act)
