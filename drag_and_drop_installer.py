"""
Maya Playback Snap Tool

Author: Cathair Kerrigan
GitHub: https://github.com/cathairjkerrigan
Licence: MIT Licence
Version: 1.0.0

"""

from src import install


def onMayaDroppedPythonFile(*args, **kwargs):
    # type: (*str, **str) -> None
    """This function is only supported since Maya 2017 Update 3"""

    install()
