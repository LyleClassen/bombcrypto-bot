import gurun
from gurun.cv import detection, transformation
from gurun.gui import io

from bot import actions


def game_login() -> gurun.Node:
    p = gurun.NodeSequence(name="BombCryptoLogin")
    p.add_node(
        actions.detection_with_natural_click("connect-wallet-button.png", threshold=0.5)
    )
    p.add_node(
        gurun.utils.Wait(
            actions.detection_with_natural_click("metamask-sign-button.png"), timeout=60
        )
    )
    p.add_node(gurun.utils.Sleep(1))
    return p


def treasure_hunt() -> gurun.Node:
    return gurun.BranchNode(
        actions.detection_with_natural_click("treasure-hunt-button.png"),
        positive=gurun.utils.Sleep(2),
    )


def error_message() -> gurun.Node:
    p = gurun.NodeSequence(name="ErrorMessage")
    p.add_node(
        detection.TemplateDetectionFrom(
            actions.screenshot(),
            target=actions.resource_path("error-title.png"),
            name="ErrorTitle",
        )
    )
    p.add_node(gurun.NullNode())
    p.add_node(actions.detection_with_natural_click("ok-button.png"))
    return p


def new_map() -> gurun.Node:
    return actions.detection_with_natural_click("new-map.png")


def heroes_to_work():
    p = gurun.NodeSequence(name="SendAllHeroesToWork")

    p.add_node(actions.go_to_heroes_menu(), name="GoToHeroesMenu")

    p.add_node(
        gurun.utils.Wait(
            actions.detection_with_natural_click(
                "work-button-disabled.png", threshold=0.9
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
                name="WorkButtonDisabled",
                single_match=True,
            )
        )
        p.add_node(transformation.RectToPoint())
        p.add_node(transformation.Offset(yOffset=350, ravel=True))
        p.add_node(io.MoveTo(duration=1))
        p.add_node(io.DragRel(yOffset=-250, duration=2))
        p.add_node(gurun.utils.Sleep(2))
        p.add_node(
            gurun.utils.Wait(
                actions.detection_with_natural_click(
                    "work-button-disabled.png", threshold=0.9
                ),
                timeout=15,
            ),
            name=f"EnableWorkers-{i + 1}",
        )

    p.add_node(gurun.utils.Print("All heroes are ready to work"))
    p.add_node(actions.close_window())

    return gurun.utils.RandomPeriodic(p, min_interval=500, max_interval=600)


def refresh_treasure_hunt():
    p = gurun.NodeSequence(name="RefreshArena")
    p.add_node(actions.detection_with_natural_click("back-to-menu-button.png"))
    p.add_node(gurun.utils.Wait(treasure_hunt(), timeout=15))
    return gurun.utils.RandomPeriodic(p, min_interval=250, max_interval=350)
