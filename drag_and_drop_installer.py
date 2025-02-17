from src import install

try:
    import maya.mel  # type: ignore
    import maya.cmds  # type: ignore
    isMaya = True
except ImportError:
    isMaya = False


def onMayaDroppedPythonFile(*args, **kwargs):
    # type: (*str, **str) -> None
    """This function is only supported since Maya 2017 Update 3"""
    pass


def _onMayaDropped():
    # type: () -> None
    """Dragging and dropping this file into the scene executes the install."""
    install()


if isMaya:
    _onMayaDropped()
