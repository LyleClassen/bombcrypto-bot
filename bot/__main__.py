import subprocess
from typing import Any

import gurun
from gurun.runner import Runner

from bot import scenes, settings


def main_scenes() -> gurun.Node:
    return gurun.NodeSet(
        [
            scenes.game_login(),
            scenes.error_message(),
            scenes.new_map(),
            scenes.heroes_to_work(),
            scenes.treasure_hunt(),
            scenes.refresh_treasure_hunt(),
            scenes.unknown(),
        ]
    )


class Workspace(gurun.Node):
    def __init__(self, workspace: str, os: str):
        self.workspace = workspace
        self.os = os

        super().__init__(name=f"Workspace-{workspace}")

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self.os == "linux":
            subprocess.run(["wmctrl", "-s", self.workspace])


if __name__ == "__main__":
    runner = Runner(
        [
            gurun.NodeSequence([Workspace(w, settings["OS"]), main_scenes()])
            for w in settings["WORKSPACES"]
        ],
        interval=1,
    )
    runner()
