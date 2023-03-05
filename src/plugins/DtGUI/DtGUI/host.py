import pluggy
import os

from DtGUI import hookspecs, lib
from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    qApp,
    QApplication,
    QFileDialog,
    QMessageBox,
    QMdiArea
)

class DtGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Init plugin
        self.pm = pluggy.PluginManager("DtGUI")
        self.pm.add_hookspecs(hookspecs)
        self.pm.load_setuptools_entrypoints("DtGUI")
        self.pm.register(lib)

        self.main_window_title = 'DroneTimeline: Forensic Timeline Analysis for Drones'
        self.database = None
        self.case_name = ''
        self.case_directory = ''
        self.timeline_columns = {}
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.merged_timeline_table_name = 'mergedtimeline'
        self.init_ui()
        self.init_menu()

    def init_ui(self):
        return self.pm.hook.init_ui(DtGUIObj=self)
    
    def init_menu(self):
        return self.pm.hook.init_menu(DtGUIObj=self)

    def timeline_subwindow_trigger(self, table_name, column_names):
        return self.pm.hook.timeline_subwindow_trigger(DtGUIObj=self, table_name=table_name, column_names=column_names)
    
    def merge_window_trigger(self):
        return self.pm.hook.merge_window_trigger(DtGUIObj=self)
    
    def merged_timeline_window_trigger(self):
        return self.pm.hook.merged_timeline_window_trigger(DtGUIObj=self)
    
    def show_info_messagebox(self, text):
        return self.pm.hook.show_info_messagebox(text=text)

def main():
    pass