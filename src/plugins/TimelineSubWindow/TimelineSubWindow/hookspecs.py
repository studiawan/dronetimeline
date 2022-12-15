import pluggy

hookspec = pluggy.HookspecMarker("TimelineSubWindow")
"""Marker to be imported and used in plugins (and for own implementations)"""

@hookspec(firstresult=True)
def show_ui(TimeLineSubWindowObj):
    """Show the UI

    :param TimeLineSubWindowObj: TimelineSubWindow object
    :return: None
    """

@hookspec(firstresult=True)
def get_column_intersection(TimeLineSubWindowObj):
    """Get the intersection of the selected columns

    :param TimeLineSubWindowObj: TimelineSubWindow object
    :return: list of column names
    """

@hookspec(firstresult=True)
def update_filter(TimeLineSubWindowObj, s):
    """Update the filter

    :param TimeLineSubWindowObj: TimelineSubWindow object
    :param s: filter string
    :return: None
    """