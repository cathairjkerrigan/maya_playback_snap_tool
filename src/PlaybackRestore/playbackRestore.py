"""
Maya Playback Restore ScriptJob

Author: Cathair Kerrigan
GitHub: https://github.com/cathairjkerrigan
Licence: MIT Licence


Feel free to share/edit the script.
"""

from maya import cmds

import logging

logger = logging.getLogger(__name__)

PLAYBACK_RESTORE_SJ = "playbackRestoreScriptJob"
STORE_FRAME_SJ = "playbackRestoreTimeChangedScriptJob"
OPTION_VAR = "storedPlaybackFrame"

DEBUG = False


def store_current_frame():
    # type: () -> None
    frame = cmds.currentTime(q=True)
    cmds.optionVar(fv=(OPTION_VAR, frame))
    if DEBUG:
        logger.info(f"Stored frame: {frame}")


def restore_frame():
    # type: () -> None
    if not cmds.optionVar(ex=OPTION_VAR):
        return
    stored_frame = cmds.optionVar(q=OPTION_VAR)

    cmds.currentTime(stored_frame, e=True)

    if DEBUG:
        logger.info(f"Restored frame: {stored_frame}")


def create_script_jobs():
    # type: () -> None
    kill_script_jobs(False)

    store_current_frame()

    restore_frame_script_job = cmds.scriptJob(
        cc=["playingBack", restore_frame],
        pro=True,
        kws=True
    )

    store_frame_script_job = cmds.scriptJob(
        event=["timeChanged", store_current_frame],
        pro=True,
        kws=True
    )

    cmds.optionVar(iv=(PLAYBACK_RESTORE_SJ, restore_frame_script_job))
    cmds.optionVar(iv=(STORE_FRAME_SJ, store_frame_script_job))

    if DEBUG:
        logger.info("Script jobs created.")

    cmds.inViewMessage(
        msg="<hl>Playback Restore Started</hl>.",
        pos="topCenter",
        f=True
    )


def kill_script_jobs(inview_message=True):
    # type: (bool) -> None
    if cmds.optionVar(ex=PLAYBACK_RESTORE_SJ):
        restore_frame_script_job = cmds.optionVar(q=PLAYBACK_RESTORE_SJ)
        if cmds.scriptJob(ex=restore_frame_script_job):
            cmds.scriptJob(k=restore_frame_script_job, f=True)
            if DEBUG:
                logger.info("Killed playback restore script job.")
        cmds.optionVar(rm=PLAYBACK_RESTORE_SJ)

    if cmds.optionVar(ex=STORE_FRAME_SJ):
        store_frame_script_job = cmds.optionVar(q=STORE_FRAME_SJ)
        if cmds.scriptJob(ex=store_frame_script_job):
            cmds.scriptJob(k=store_frame_script_job, f=True)
            if DEBUG:
                logger.info("Killed time tracking script job.")
        cmds.optionVar(rm=STORE_FRAME_SJ)

    if inview_message:
        cmds.inViewMessage(
            msg="<hl>Playback Restore Ended</hl>.",
            pos="topCenter",
            f=True
        )


def toggle_script_job():
    # type: () -> None
    if cmds.optionVar(ex=PLAYBACK_RESTORE_SJ):
        kill_script_jobs()
        return
    create_script_jobs()
