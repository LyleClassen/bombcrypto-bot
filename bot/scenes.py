import gurun
from gurun.cv import detection
from gurun.gui import io

from bot import actions


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


def new_map() -> gurun.Node:
    return actions.detection_with_natural_click("new-map.png")


def heroes_to_work(
    strategy: str, min_interval: float, max_interval: float
) -> gurun.Node:
    p = gurun.NodeSequence(name="HeroesToWork")

    p.add_node(actions.go_to_heroes_menu(), name="GoToHeroesMenu")

    p.add_node(gurun.utils.Sleep(1))

    if strategy == "greens":
        p.add_node(actions.send_green_heroes())
    else:
        p.add_node(actions.send_all_heroes())

    p.add_node(gurun.utils.Print("All heroes are ready to work"))
    p.add_node(actions.close_window())

    return gurun.utils.RandomPeriodic(
        p, min_interval=min_interval, max_interval=max_interval
    )


def refresh_treasure_hunt(min_interval: float, max_interval: float) -> gurun.Node:
    p = gurun.NodeSequence(name="RefreshTreasureHunt")
    p.add_node(actions.go_back_to_main_menu())
    p.add_node(treasure_hunt())
    return gurun.utils.RandomPeriodic(
        p, min_interval=min_interval, max_interval=max_interval
    )


def unknown() -> gurun.Node:
    p = gurun.NodeSequence(name="Unknown")
    p.add_node(actions.close_window())
    p.add_node(actions.ok_button())
    return p
