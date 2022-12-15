import pluggy

hookimpl = pluggy.HookimplMarker("QtDatabase")
"""Marker to be imported and used in plugins (and for own implementations)"""