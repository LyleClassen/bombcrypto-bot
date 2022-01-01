import os

import gurun
from gurun import utils
from gurun.cv import detection
from gurun.gui import io

from bot import settings


def screenshot() -> gurun.Node:
    return gurun.gui.screenshot.ScreenshotMMS()


def resource_path(filename: str) -> str:
    return os.path.join(settings["RESOURCES_DIR"], filename)


def button_connect_wallet() -> gurun.Node:
    p = gurun.NodeSequence(name="ConnectWallet")
    p.add_node(
        detection.TemplateDetectionFrom(
            screenshot(),
            target=resource_path("connect-wallet-button.png"),
            name="ConnectWalletButton",
            threshold=0.5,
        )
    )
    p.add_node(io.MultipleNaturalClicks())
    return p


def metamask_sign() -> gurun.Node:
    p = gurun.NodeSequence(name="MetamaskSign")
    p.add_node(
        detection.TemplateDetectionFrom(
            screenshot(),
            target=resource_path("metamask-sign-button.png"),
            name="MetamaskSignButton",
        )
    )
    p.add_node(io.MultipleNaturalClicks())

    return p

def button_back_to_menu() -> gurun.Node:
    p = gurun.NodeSequence(name="BackToMenu")
    p.add_node(
        detection.TemplateDetectionFrom(
            screenshot(),
            target=resource_path("back-to-menu-button.png"),
            name="BackToMenuButton",
        )
    )
    p.add_node(io.MultipleNaturalClicks())
    return p


def button_heroes_list():
    p = gurun.NodeSequence(name="HeroesList")
    p.add_node(
        detection.TemplateDetectionFrom(
            screenshot(),
            target=resource_path("heroes-button.png"),
            name="HeroesButton",
        )
    )
    p.add_node(io.MultipleNaturalClicks())
    return p


def go_to_heroes_menu():
    p = gurun.NodeSequence(name="GoToHeroesMenu")

    p.add_node(gurun.BranchNode(button_back_to_menu(), positive=gurun.utils.Sleep(5)), name="BackToMenu")
    p.add_node(detection.TemplateDetectionFrom(
                    screenshot(),
                    target=resource_path("heroes-button.png"),
                    name="HeroesMenu",
        ), name="FindHeroesMenu")
    p.add_node(io.MultipleNaturalClicks(), name="ClickHeroesMenu")

    return p


def click_on_disabled_work_button():
    p = gurun.NodeSequence(name="ClickOnDisableHeroes")
    p.add_node(
        detection.TemplateDetectionFrom(
            screenshot(),
            target=resource_path("work-button-disabled.png"),
            name="DisableWorkButton",
            transformation=gurun.cv.transformation.RectToPoint(),
            threshold=0.9,
        )
    )
    p.add_node(io.MultipleNaturalClicks())

    return p


def close_window() -> gurun.Node:
    p = gurun.NodeSequence(name="CloseWindow")
    p.add_node(
        detection.TemplateDetectionFrom(
            screenshot(),
            target=resource_path("close-button.png"),
            name="CloseButton",
        )
    )
    p.add_node(io.MultipleNaturalClicks())
    return p




def action_game_login() -> gurun.Node:
    p = gurun.NodeSequence(name="BombCryptoLogin")
    p.add_node(button_connect_wallet())
    p.add_node(gurun.utils.Wait(metamask_sign(), timeout=60))
    p.add_node(gurun.utils.Sleep(5))
    return p


def action_treasure_hunt() -> gurun.Node:
    p = gurun.NodeSequence(name="TreasureHunt")

    p.add_node(
        detection.TemplateDetectionFrom(
            screenshot(),
            target=resource_path("treasure-hunt-button.png"),
            name="TreasureHuntButton",
        )
    )
    p.add_node(io.MultipleNaturalClicks())

    return gurun.BranchNode(p, positive=gurun.utils.Sleep(2))


def action_error_message() -> gurun.Node:
    p = gurun.NodeSequence(name="ErrorMessage")
    p.add_node(
        detection.TemplateDetectionFrom(
            screenshot(),
            target=resource_path("error-title.png"),
            name="ErrorTitle",
        )
    )
    p.add_node(gurun.NullNode())
    p.add_node(
        detection.TemplateDetectionFrom(
            screenshot(),
            target=resource_path("ok-button.png"),
            name="OkButton",
        )
    )
    p.add_node(io.MultipleNaturalClicks())

    return p


def action_new_map() -> gurun.Node:
    p = gurun.NodeSequence(name="NewMap")
    p.add_node(
        detection.TemplateDetectionFrom(
            screenshot(),
            target=resource_path("new-map.png"),
            name="NewMap",
        )
    )
    p.add_node(io.MultipleNaturalClicks())
    return p

def action_heroes_to_work():
    p = gurun.NodeSequence(name="SendAllHeroesToWork")

    p.add_node(go_to_heroes_menu(), name="GoToHeroesMenu")

    p.add_node(gurun.utils.Wait(click_on_disabled_work_button(), timeout=15), name="ClickOnDisableHeroes")

    for _ in range(3):
        p.add_node(gurun.utils.Sleep(1))
        p.add_node(
            detection.TemplateDetectionFrom(
                screenshot(),
                target=resource_path("character-menu-title.png"),
                name="WorkButtonDisabled",
                single_match=True,
                ravel=True,
            )
        )
        p.add_node(io.MoveTo(duration=1))
        p.add_node(io.MoveRel(y=350, duration=1))
        # p.add_node(MoveMouse(y=300, duration=1))
        p.add_node(io.DragRel(yOffset=-250, duration=1))
        p.add_node(gurun.utils.Sleep(2))

        p.add_node(gurun.utils.Wait(click_on_disabled_work_button(), timeout=15), name="ClickOnDisableHeroes")
        p.add_node(gurun.utils.Sleep(2))

    p.add_node(gurun.utils.Wait(close_window(), timeout=15))

    return gurun.utils.RandomPeriodic(p, min_interval=500, max_interval=600)


def action_refresh_treasure_hunt():
    p = gurun.NodeSequence(name="RefreshArena")
    p.add_node(button_back_to_menu())
    p.add_node(gurun.utils.Wait(action_treasure_hunt(), timeout=15))
    return gurun.utils.RandomPeriodic(p, min_interval=250, max_interval=350)


# def set_workspace(workspace: str):
#     p = gurun.NodeSequence(name="SetWorkspace")
#     p.add_node(gurun.io.HotKey(["shift", "alt", workspace]))
#     p.add_node(gurun.utils.Wait(10))
#     return p
