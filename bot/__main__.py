import os
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


if __name__ == "__main__":
    os.environ["GURUN_VERBOSE"] = str(settings["VERBOSE"])
    runner = Runner(
        [
            gurun.NodeSequence([gurun.gui.os.Workspace(w, settings["OS"]), main_scenes()])
            for w in settings["WORKSPACES"]
        ] if settings["MULTI_ACCOUNT"] else main_scenes(),
        interval=1,
    )
    runner.run()
