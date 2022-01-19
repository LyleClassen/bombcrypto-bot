import gurun
from gurun.cv import detection, transformation
from gurun.cv import utils as cv_utils
from gurun.gui import io

from bot import image_reader


def screenshot() -> gurun.Node:
    return gurun.gui.screenshot.ScreenshotMMS()


def detection_with_natural_click(
    target: str,
    offset: gurun.Node = None,
    name: str = None,
    rect_to_point_node: transformation.Transformation = transformation.NaturalRectToPoint(),
    apply_zoom: bool = True,
    **kwargs,
) -> gurun.Node:
    p = gurun.NodeSequence(name=name)
    p.add_node(
        detection.TemplateDetectionFrom(
            screenshot(), target=image_reader.read(target, apply_zoom), **kwargs
        )
    )
    p.add_node(rect_to_point_node)

    if offset:
        if isinstance(offset, gurun.Node):
            p.add_node(offset)
        else:
            p.add_node(gurun.cv.transformation.Offset(*offset))

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
                target=image_reader.read(wait_target),
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


def scroll_heroes_menu() -> gurun.Node:
    p = gurun.NodeSequence(name="ScrollHeroesMenu")
    p.add_node(transformation.RectToPoint())
    p.add_node(transformation.Offset(yOffset=350, ravel=True))
    p.add_node(io.MoveTo(duration=1))
    p.add_node(io.DragRel(yOffset=-250, duration=2))
    p.add_node(gurun.utils.Sleep(2))

    return p


def send_green_heroes() -> gurun.Node:
    p = gurun.NodeSequence(name="SendGreenHeroesToWork")

    p.add_node(
        gurun.BranchNode(
            detection_with_natural_click(
                "full-stamina.png",
                threshold=0.9,
                offset=(100, 0),
                rect_to_point_node=transformation.RectToPoint(),
            )
        ),
        name=f"FullStamina-0",
    )
    p.add_node(
        gurun.BranchNode(
            detection_with_natural_click(
                "green-bar.png",
                threshold=0.9,
                offset=(150, 0),
                rect_to_point_node=transformation.RectToPoint(),
            )
        ),
        name=f"EnableWorkers-0",
    )

    for i in range(3):
        p.add_node(gurun.utils.Sleep(2))
        p.add_node(
            detection.TemplateDetectionFrom(
                screenshot(),
                target=image_reader.read("character-menu-title.png"),
            )
        )
        p.add_node(cv_utils.ForEachDetection(scroll_heroes_menu()))

        p.add_node(
            gurun.BranchNode(
                detection_with_natural_click(
                    "green-bar.png",
                    threshold=0.9,
                    offset=(150, 0),
                    rect_to_point_node=transformation.RectToPoint(),
                )
            ),
            name=f"EnableWorkers-{i + 1}",
        )

        p.add_node(
            gurun.BranchNode(
                detection_with_natural_click(
                    "full-stamina.png",
                    threshold=0.9,
                    offset=(100, 0),
                    rect_to_point_node=transformation.RectToPoint(),
                )
            ),
            name=f"FullStamina-{i + 1}",
        )

    return p


def send_all_heroes() -> gurun.Node:
    p = gurun.NodeSequence(name="SendAllHeroesToWork")

    p.add_node(
        gurun.BranchNode(
            detection_with_natural_click(
                "all-button.png",
                threshold=0.5,
                rect_to_point_node=transformation.RectToPoint(),
            )
        )
    )

    return p
