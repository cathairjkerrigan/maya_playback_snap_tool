from maya import cmds, mel
from textwrap import dedent
import logging
import shutil
import os

logger = logging.getLogger(__name__)


def get_maya_scripts_folder():
    # type: () -> str
    maya_scripts_path = os.path.join(
        os.path.dirname(os.environ["MAYA_APP_DIR"]),
        r"maya/scripts"
    )
    if not os.path.exists(maya_scripts_path):
        raise RuntimeError("Maya scripts folder not found.")

    dir_path = os.path.join(maya_scripts_path, "PlaybackSnap")

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return os.path.normpath(dir_path)


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
    path = os.path.join(os.path.dirname(__file__), 'PlaybackSnap')
    return os.path.normpath(path)


def build_shelf_button(icon_path):
    # type: (str) -> None
    logger.info("Building shelf button")
    shelf = mel.eval('$gShelfTopLevel=$gShelfTopLevel')
    parent = cmds.tabLayout(shelf, q=True, st=True)  # type: ignore
    icon = os.path.join(icon_path, "playback_snap_icon.svg")
    cmds.shelfButton(
                w=32,
                h=32,
                i=icon,
                l="PlaybackSnap",
                ann="Toggle Playback Snap Tool",
                c=dedent(
                    """
                    from PlaybackSnap import toggle_playback_snap_tool

                    toggle_playback_snap_tool()
                    """
                ),
                iol="",
                sic=True,
                p=parent
            )


def install():
    # type: () -> None
    src_folder = get_module_folder()
    dest_folder = get_maya_scripts_folder()
    logger.info("Copying folder '{}' to '{}'".format(src_folder, dest_folder))
    copy_folder(src_folder, dest_folder)
    icon_path = os.path.join(dest_folder, "icons")
    build_shelf_button(icon_path)
    logger.info("Installation complete.")
