from src import install


def onMayaDroppedPythonFile(*args, **kwargs):
    # type: (*str, **str) -> None
    """This function is only supported since Maya 2017 Update 3"""

    install()
