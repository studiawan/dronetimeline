import TimelineSubWindow
from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QTableView,
    QLabel
)
from PyQt5.QtSql import QSqlTableModel
from PyQt5 import QtGui

@TimelineSubWindow.hookimpl(tryfirst=True)
def get_column_intersection(TimeLineSubWindowObj):
    # get column event or message, get the first one found
    print("TimeLineSubWindowObj.column_names", TimeLineSubWindowObj.column_names)
    print("TimeLineSubWindowObj.event_columns", TimeLineSubWindowObj.event_columns)
    # Change event_columns add _plugin
    ev = []
    for e in TimeLineSubWindowObj.event_columns:
        ev.append(e + "_plugin")

    intersection = set(TimeLineSubWindowObj.column_names).intersection(set(ev))

    intersection = list(intersection)
    event_column = intersection[0]

    return event_column
