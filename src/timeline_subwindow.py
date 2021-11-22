from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QTableView,
    QAbstractItemView
)
from CustomeDelegate import CustomeDelegate
from PyQt5.QtSql import QSqlTableModel
from PyQt5 import QtGui

class TimelineSubWindow(QMdiSubWindow):
    def __init__(self, table_name, column_names , db_connection):
        super().__init__()
        self.table_name = table_name
        self.column_names = column_names
        self.db_connection = db_connection
        self.table_model = None
        self.event_columns = ['message', 'event']
        self.event_column = self.get_column_intersection()

    def show_ui(self):
        # set title and geometry
        subwindow_title = f"{'Drone Timeline: '}{self.table_name}"
        self.setWindowIcon(QtGui.QIcon('../assets/drone.png'))
        self.setWindowTitle(subwindow_title)
        self.setGeometry(60, 60, 600, 400)

        # construct the top level widget and layout
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # set table from database
        self.table_model = QSqlTableModel(db=self.db_connection)
        self.table_model.setTable(self.table_name)
        self.table_model.select()

        # define search widget
        search_label = QLabel()
        search_label.setText('Search event or message:')
        search = QLineEdit()

        # define table widget
        table_label = QLabel()
        table_label.setText('Merged timeline:')
        table_widget = QTableView()
        table_widget.setModel(self.table_model)
        
        # Define custom delegate to mark entity, pyqt stuff
        custom_delegate = CustomeDelegate()
        table_widget.setItemDelegate(custom_delegate)

        # Disable editing
        # table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # search event
        search.textChanged.connect(self.update_filter)

        # add widget to layout
        layout.addWidget(search_label)
        layout.addWidget(search)
        layout.addWidget(table_label)
        layout.addWidget(table_widget)
        widget.setLayout(layout)

        # set widget to subwindow
        self.setWidget(widget)
        self.show()

    def get_column_intersection(self):
        # get column event or message, get the first one found
        intersection = set(self.column_names).intersection(set(self.event_columns))
        intersection = list(intersection)
        event_column = intersection[0]

        return event_column

    def update_filter(self, s):
        percent = '%'
        filter_str = f"{self.event_column}{' LIKE '}\"{percent}{s}{percent}\""
        self.table_model.setFilter(filter_str)

    def set_column_names(self, dbconnection):
        column_names = []
        record = dbconnection.record(self.table_name)
        for i in range(0, record.count()):
            column_names.append(record.fieldName(i))

        return column_names



