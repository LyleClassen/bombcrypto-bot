from gurun.runner import Runner

from bot import pipelines

if __name__ == "__main__":
    runner = Runner(
        [
            pipelines.action_game_login(),
            pipelines.action_heroes_to_work(),
            pipelines.action_treasure_hunt(),
            pipelines.action_error_message(),
            pipelines.action_new_map(),
            pipelines.action_refresh_treasure_hunt(),
        ]
    )
    runner()
