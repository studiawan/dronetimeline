import DtGUI
from PyQt5.QtWidgets import (
    QAction,
)

@DtGUI.hookimpl
def init_menu(DtGUIObj):
    # application menu
    menubar = DtGUIObj.menuBar()

    # File menu
    new_menu = menubar.addMenu('&New Customized Menu')
    
    # File menu action
    newmenu_act = QAction('&Select something', DtGUIObj)
    newmenu_act.setShortcut('Ctrl+P')
    newmenu_act.setStatusTip('Select something')

    def newmenu_trigger():
        DtGUIObj.show_info_messagebox('You have selected the new menu')

    newmenu_act.triggered.connect(newmenu_trigger)
    new_menu.addAction(newmenu_act)
