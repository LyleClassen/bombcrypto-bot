import os

import gurun
from gurun.cv import detection, transformation
from gurun.gui import io

from bot import settings


def screenshot() -> gurun.Node:
    return gurun.gui.screenshot.ScreenshotMMS()


def resource_path(filename: str) -> str:
    return os.path.join(settings["RESOURCES_DIR"], filename)


def detection_with_natural_click(
    target: str, offset: gurun.Node = None, name: str = None, **kwargs
) -> gurun.Node:
    p = gurun.NodeSequence(name=name)
    p.add_node(
        detection.TemplateDetectionFrom(
            screenshot(), target=resource_path(target), **kwargs
        )
    )
    p.add_node(transformation.NaturalRectToPoint())

    if offset:
        p.add_node(offset)

    p.add_node(io.MultipleNaturalClicks(clicks=2))
    return p


def wait_for_successful_action(
    target: str, wait_target: str = None, timeout: float = 60, name: str = None
) -> gurun.Node:
    wait_target = target if wait_target is None else wait_target

    p = gurun.NodeSequence(name=name)
    p.add_node(
        gurun.utils.While(
            trigger=detection.TemplateDetectionFrom(
                screenshot(),
                target=resource_path(wait_target),
                name=f"{name}-detection",
            ),
            action=detection_with_natural_click(target),
            timeout=timeout,
        ),
        name=f"{name}-while",
    )

    return p


def go_back_to_main_menu() -> gurun.Node:
    return wait_for_successful_action(
        "back-to-menu-button.png", name="GoBackToMainMenu"
    )


def close_window() -> gurun.Node:
    return wait_for_successful_action("close-button.png", name="CloseWindowAction")


def ok_button() -> gurun.Node:
    return wait_for_successful_action("ok.png", name="OkButton")


def go_to_heroes_menu() -> gurun.Node:
    p = gurun.NodeSequence(name="GoToHeroesMenu")

    p.add_node(
        gurun.BranchNode(
            go_back_to_main_menu(),
            positive=gurun.utils.Sleep(2),
        ),
        name="BackToMenu",
    )
    p.add_node(detection_with_natural_click("heroes-button.png"))

    return p
