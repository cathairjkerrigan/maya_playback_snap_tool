from maya import cmds, mel
from textwrap import dedent
import logging
import shutil
import os

logger = logging.getLogger(__name__)


def get_maya_scripts_folder():
    # type: () -> str
    path = os.path.join(
        os.path.dirname(os.environ["MAYA_APP_DIR"]),
        r"maya/scripts"
        )
    return os.path.normpath(path)


def copy_folder(src, dest):
    # type: (str, str) -> str
    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(src, dest, symlinks=True)
        logger.info(
            "Folder '{}' successfully copied to '{}'".format(src, dest)
        )
        return dest
    except Exception as e:
        logger.warning("Error copying folder '{}': {}".format(src, e))
        return ""


def get_module_folder():
    # type: () -> str
    path = os.path.join(os.path.dirname(__file__), 'PlaybackRestore')
    return os.path.normpath(path)


def build_shelf_button():
    # type: () -> None
    shelf = mel.eval('$gShelfTopLevel=$gShelfTopLevel')
    parent = cmds.tabLayout(shelf, q=True, st=True)  # type: ignore
    cmds.shelfButton(
                w=32,
                h=32,
                i="play_hover.png",
                l="PlaybackRestore",
                ann="Toggle Playback Restore",
                c=dedent(
                    """
                    from PlaybackRestore import toggle_playback_snap_tool

                    toggle_playback_snap_tool()
                    """
                ),
                iol="PlaybackRestore",
                sic=True,
                p=parent
            )


def install():
    # type: () -> None
    src_folder = get_module_folder()
    dest_folder = get_maya_scripts_folder()
    logger.info("Copying folder '{}' to '{}'".format(src_folder, dest_folder))
    copy_folder(src_folder, dest_folder)
    build_shelf_button()
    logger.info("Installation complete.")
