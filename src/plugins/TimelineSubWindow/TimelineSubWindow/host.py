import pluggy

from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QTableView,
    QLabel
)

from TimelineSubWindow import hookspecs, lib

class TimelineSubWindow(QMdiSubWindow):
    def __init__(self, table_name, column_names, db_connection):
        super().__init__()
        # Init plugin
        self.pm = pluggy.PluginManager("TimelineSubWindow")
        self.pm.add_hookspecs(hookspecs)
        self.pm.load_setuptools_entrypoints("TimelineSubWindow")
        self.pm.register(lib)

        self.table_name = table_name
        self.column_names = column_names
        self.db_connection = db_connection
        self.table_model = None
        self.event_columns = ['message', 'event']
        self.event_column = self.get_column_intersection()

    def show_ui(self):
        return self.pm.hook.show_ui(TimeLineSubWindowObj=self)
    
    def get_column_intersection(self):
        return self.pm.hook.get_column_intersection(TimeLineSubWindowObj=self)
    
    def update_filter(self, s):
        return self.pm.hook.update_filter(TimeLineSubWindowObj=self, s=s)

def main():
    pass