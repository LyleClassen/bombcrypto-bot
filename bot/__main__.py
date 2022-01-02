from gurun.runner import Runner

from bot import scenes

if __name__ == "__main__":
    runner = Runner(
        [
            scenes.game_login(),
            scenes.error_message(),
            scenes.new_map(),
            scenes.heroes_to_work(),
            scenes.treasure_hunt(),
            scenes.refresh_treasure_hunt(),
        ],
        interval=1,
    )
    runner()
