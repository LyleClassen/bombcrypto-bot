import gurun
from gurun.cv import detection, transformation
from gurun.cv import utils as cv_utils
from gurun.gui import io

from bot import actions, settings


def game_login() -> gurun.Node:
    p = gurun.NodeSequence(name="BombCryptoLogin")

    p.add_node(
        gurun.BranchNode(
            gurun.utils.While(
                trigger=detection.TemplateDetectionFrom(
                    actions.screenshot(),
                    target=actions.resource_path("game-login-title.png"),
                    name=f"game-login-detection",
                ),
                action=gurun.NodeSequence(
                    [
                        actions.detection_with_natural_click(
                            "connect-wallet-button.png", threshold=0.5
                        ),
                        gurun.utils.Wait(
                            actions.detection_with_natural_click(
                                "metamask-sign-button.png"
                            ),
                            timeout=60,
                        ),
                        gurun.utils.Sleep(1),
                    ]
                ),
                timeout=60,
            ),
            negative=io.HotKey("f5"),
        )
    )

    return p


def treasure_hunt() -> gurun.Node:
    return actions.wait_for_successful_action(
        "treasure-hunt-button.png", name="TreasureHunt"
    )


def error_message() -> gurun.Node:
    return actions.wait_for_successful_action(
        target="ok.png", wait_target="error-title.png", name="ErrorMessage"
    )


def new_map() -> gurun.Node:
    return actions.detection_with_natural_click("new-map.png")


def heroes_to_work() -> gurun.Node:
    p = gurun.NodeSequence(name="HeroesToWork")

    p.add_node(actions.go_to_heroes_menu(), name="GoToHeroesMenu")

    p.add_node(
        gurun.utils.Wait(
            actions.detection_with_natural_click(
                "green-bar.png", threshold=0.9, offset=(150, 0), rect_to_point_node=transformation.RectToPoint()
            ),
            timeout=15,
        ),
        name="EnableWorkers-0",
    )

    for i in range(3):
        p.add_node(gurun.utils.Sleep(1))
        p.add_node(
            detection.TemplateDetectionFrom(
                actions.screenshot(),
                target=actions.resource_path("character-menu-title.png"),
            )
        )
        p.add_node(cv_utils.ForEachDetection(actions.scroll_heroes_menu()))

        p.add_node(
            gurun.BranchNode(gurun.utils.Wait(
                actions.detection_with_natural_click(
                    "green-bar.png", threshold=0.9, offset=(150, 0), rect_to_point_node=transformation.RectToPoint()
                ),
                timeout=5,
            )),
            name=f"EnableWorkers-{i + 1}",
        )

    p.add_node(gurun.utils.Print("All heroes are ready to work"))
    p.add_node(actions.close_window())

    return gurun.utils.RandomPeriodic(p, min_interval=settings["HEROES"]["MIN"], max_interval=settings["HEROES"]["MAX"])


def refresh_treasure_hunt() -> gurun.Node:
    p = gurun.NodeSequence(name="RefreshTreasureHunt")
    p.add_node(actions.go_back_to_main_menu())
    p.add_node(treasure_hunt())
    return gurun.utils.RandomPeriodic(p, min_interval=settings["REFRESH"]["MIN"], max_interval=settings["REFRESH"]["MIN"])


def unknown() -> gurun.Node:
    p = gurun.NodeSequence(name="Unknown")
    p.add_node(actions.close_window())
    p.add_node(actions.ok_button())
    return p
