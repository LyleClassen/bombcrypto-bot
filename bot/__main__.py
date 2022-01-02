from gurun.runner import Runner

from bot import scenes, settings
import gurun


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


class Workspace(gurun.NodeSequence):
    def __init__(self, workspace: str, os: str):
        nodes = []

        if os.lower() == "windows":
            nodes.append(
                gurun.gui.io.HotKey(
                    ["ctrl", "win", workspace], name=f"WORKSPACE-{workspace}"
                )
            )
        else:
            nodes.append(
                gurun.gui.io.HotKey(
                    ["shift", "alt", f"f{workspace}"], name=f"WORKSPACE-{workspace}"
                )
            )

        nodes.append(main_scenes())

        super().__init__(nodes=nodes, name=f"Workspace-{workspace}")


if __name__ == "__main__":
    runner = Runner(
        [Workspace(w, settings["OS"]) for w in settings["WORKSPACES"]],
        interval=1,
    )
    runner()
