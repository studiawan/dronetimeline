import pluggy
from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QListWidget,
    QMessageBox
)

from MergeTimelineSubWindow import hookspecs, lib

class MergeTimelineSubWindow(QMdiSubWindow):
    def __init__(self, timeline_columns, database, merged_timeline_table_name):
        super().__init__()

        # Init plugin
        self.pm = pluggy.PluginManager("MergeTimelineSubWindow")
        self.pm.add_hookspecs(hookspecs)
        self.pm.load_setuptools_entrypoints("MergeTimelineSubWindow")
        self.pm.register(lib)

        self.timeline_columns = timeline_columns
        self.database = database
        self.timeline_combo = None
        self.timeline_list = None
        self.column_list = None
        self.final_column = None
        self.merged_timeline_table_name = merged_timeline_table_name

    def show_ui(self):
        return self.pm.hook.show_ui(MergeTimelineSubWindowObj=self)
    
    def add_timeline_button_clicked(self):
        return self.pm.hook.add_timeline_button_clicked(MergeTimelineSubWindowObj=self)
    
    def add_column_as_timestamp_button_clicked(self):
        return self.pm.hook.add_column_as_timestamp_button_clicked(MergeTimelineSubWindowObj=self)
    
    def add_column_as_event_button_clicked(self):
        return self.pm.hook.add_column_as_event_button_clicked(MergeTimelineSubWindowObj=self)
    
    def add_column_clicked(self, column_type):
        return self.pm.hook.add_column_clicked(MergeTimelineSubWindowObj=self, column_type=column_type)
    
    def timeline_list_clicked(self):
        return self.pm.hook.timeline_list_clicked(MergeTimelineSubWindowObj=self)
    
    def remove_column_button_clicked(self):
        return self.pm.hook.remove_column_button_clicked(MergeTimelineSubWindowObj=self)
    
    def merge_button_clicked(self):
        return self.pm.hook.merge_button_clicked(MergeTimelineSubWindowObj=self)
    
    def show_info_messagebox(self, text):
        return self.pm.hook.show_info_messagebox(text=text)

def main():
    pass