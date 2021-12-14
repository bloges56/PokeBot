# -*- coding: utf-8 -*-
import asyncio
import time
import sys

sys.path.append("..")

import BattleUtilities
from poke_env.player.random_player import RandomPlayer
from MaxDamagePlayer import MaxDamagePlayer
from SmartDamagePlayer import SmartDamagePlayer
from MiniMax import MinimaxPlayer
from SmartMiniMax import SmartMinimaxPlayer
from RandomMiniMax import RandomMinimaxPlayer
from SimpleRulePlayer import SimpleRulePlayer
from poke_env.player.player import Player
from poke_env.player.baselines import SimpleHeuristicsPlayer

async def main():
    start = time.time()

    # We create two players.
    smart_damage_player = SmartDamagePlayer(
        battle_format="gen8randombattle",
    )
    minimax_player = MinimaxPlayer(
        battle_format="gen8randombattle",
    )

    await minimax_player.battle_against(smart_damage_player, n_battles=1000)

    print(
        "minimax player (depth 1) won %d / 1000 battles against smart_damage_player (this took %f seconds)"
        % (
            minimax_player.n_won_battles, time.time() - start
        )
    )

    start = time.time()

    # We create two players.
    smart_damage_player = SmartDamagePlayer(
        battle_format="gen8randombattle",
    )
    minimax_player = MinimaxPlayer(
        battle_format="gen8randombattle",
    )

    minimax_player.maxDepth = 2

    await minimax_player.battle_against(smart_damage_player, n_battles=1000)

    print(
        "minimax player (depth 2) won %d / 1000 battles against smart_damage_player (this took %f seconds)"
        % (
            minimax_player.n_won_battles, time.time() - start
        )
    )

    start = time.time()

    # We create two players.
    smart_damage_player = SmartDamagePlayer(
        battle_format="gen8randombattle",
    )
    minimax_player = MinimaxPlayer(
        battle_format="gen8randombattle",
    )

    minimax_player.maxDepth = 3

    await minimax_player.battle_against(smart_damage_player, n_battles=1000)

    print(
        "minimax player (depth 3) won %d / 1000 battles against smart_damage_player (this took %f seconds)"
        % (
            minimax_player.n_won_battles, time.time() - start
        )
    )

    start = time.time()

    # We create two players.
    smart_damage_player = SmartDamagePlayer(
        battle_format="gen8randombattle",
    )
    random_minimax_player = RandomMinimaxPlayer(
        battle_format="gen8randombattle",
    )

    random_minimax_player.statusWeight = 1

    await random_minimax_player.battle_against(smart_damage_player, n_battles=1000)

    print(
        "random minimax player (status weight 1) won %d / 1000 battles against smart_damage_player (this took %f seconds)"
        % (
            random_minimax_player.n_won_battles, time.time() - start
        )
    )

    start = time.time()

    # We create two players.
    smart_damage_player = SmartDamagePlayer(
        battle_format="gen8randombattle",
    )
    random_minimax_player = RandomMinimaxPlayer(
        battle_format="gen8randombattle",
    )

    random_minimax_player.statusWeight = 2

    await random_minimax_player.battle_against(smart_damage_player, n_battles=1000)

    print(
        "random minimax player (status weight 2) won %d / 1000 battles against smart_damage_player (this took %f seconds)"
        % (
            random_minimax_player.n_won_battles, time.time() - start
        )
    )

    start = time.time()

    # We create two players.
    smart_damage_player = SmartDamagePlayer(
        battle_format="gen8randombattle",
    )
    random_minimax_player = RandomMinimaxPlayer(
        battle_format="gen8randombattle",
    )

    random_minimax_player.statusWeight = 3

    await random_minimax_player.battle_against(smart_damage_player, n_battles=1000)

    print(
        "random minimax player (status weight 3) won %d / 1000 battles against smart_damage_player (this took %f seconds)"
        % (
            random_minimax_player.n_won_battles, time.time() - start
        )
    )

if __name__ == "__main__":
        asyncio.get_event_loop().run_until_complete(main())
    # start = time.time()

    # players = {}
    
    # players["random player"] = (RandomPlayer(
    #     battle_format="gen8randombattle",
    # ))
    # players["max damage player"] = (MaxDamagePlayer(
    #     battle_format="gen8randombattle",
    # ))
    # players["smart damage player"] = (SmartDamagePlayer(
    #     battle_format="gen8randombattle",
    # ))
    # players["minimax player"] = (MinimaxPlayer(
    #     battle_format="gen8randombattle",
    # ))
    # players["smart minimax player"] = (SmartMinimaxPlayer(
    #     battle_format="gen8randombattle",
    # ))
    # players["random minimax player"] = (RandomMinimaxPlayer(
    #     battle_format="gen8randombattle",
    # ))
    # players["heurstic player"] = (SimpleHeuristicsPlayer(
    #     battle_format="gen8randombattle",
    # ))
    # players["simple rule player"] = (SimpleRulePlayer(
    #     battle_format="gen8randombattle",
    # ))
    
    # for i in range(len(players.keys())):
    #     for j in range(i + 1, len(players.keys())):
    #         await players[list(players.keys())[i]].battle_against(players[list(players.keys())[j]], n_battles=1000)
    #         print("battle finished")

    # for player in players.keys():
    #     print(
    #     "%s won %d / 6000 battles"
    #     % (
    #         player, players[player].n_won_battles
    #     )
    # )
    # if __name__ == "__main__":
    #     asyncio.get_event_loop().run_until_complete(main())
    # print(
    #     "random player won %d / 1000 battles against max_damage_player (this took %f seconds)"
    #     % (
    #         random_player.n_won_battles, time.time() - start
    #     )
    # )

    # # Random vs Smart
    # start = time.time()
    # random_player = RandomPlayer(
    #     battle_format="gen8randombattle",
    # )
    # smart_damage_player = SmartDamagePlayer(
    #     battle_format="gen8randombattle",
    # )

    # await random_player.battle_against(smart_damage_player, n_battles=1000)

    # print(
    #     "random player won %d / 1000 battles against smart_damage_player (this took %f seconds)"
    #     % (
    #         random_player.n_won_battles, time.time() - start
    #     )
    # )

    # # Random vs Minimax
    # start = time.time()
    # random_player = RandomPlayer(
    #     battle_format="gen8randombattle",
    # )
    # minimax_player = MinimaxPlayer(
    #     battle_format="gen8randombattle",
    # )

    # await random_player.battle_against(minimax_player, n_battles=1000)

    # print(
    #     "random player won %d / 1000 battles against minimax_player (this took %f seconds)"
    #     % (
    #         random_player.n_won_battles, time.time() - start
    #     )
    # )

    # # Random vs heuristic
    # start = time.time()
    # random_player = RandomPlayer(
    #     battle_format="gen8randombattle",
    # )
    # heuristic_player = SimpleHeuristicsPlayer(
    #     battle_format="gen8randombattle",
    # )

    # await random_player.battle_against(heuristic_player, n_battles=1000)

    # print(
    #     "random player won %d / 1000 battles against heuristic_player (this took %f seconds)"
    #     % (
    #         random_player.n_won_battles, time.time() - start
    #     )
    # )

    # # Max vs Smart
    # start = time.time()
    # max_damage_player = MaxDamagePlayer(
    #     battle_format="gen8randombattle",
    # )
    # smart_damage_player = SmartDamagePlayer(
    #     battle_format="gen8randombattle",
    # )

    # await max_damage_player.battle_against(smart_damage_player, n_battles=1000)

    # print(
    #     "max_damage_player won %d / 1000 battles against smart_damage_player (this took %f seconds)"
    #     % (
    #         max_damage_player.n_won_battles, time.time() - start
    #     )
    # )
    
    # # Max vs Minimax
    # start = time.time()
    # max_damage_player = MaxDamagePlayer(
    #     battle_format="gen8randombattle",
    # )
    # minimax_player = MinimaxPlayer(
    #     battle_format="gen8randombattle",
    # )

    # await max_damage_player.battle_against(minimax_player, n_battles=1000)

    # print(
    #     "max_damage_player won %d / 1000 battles against minimax_player (this took %f seconds)"
    #     % (
    #         max_damage_player.n_won_battles, time.time() - start
    #     )
    # )

    # # Max vs Heuristic
    # start = time.time()
    # max_damage_player = MaxDamagePlayer(
    #     battle_format="gen8randombattle",
    # )
    # heuristic_player = SimpleHeuristicsPlayer(
    #     battle_format="gen8randombattle",
    # )

    # await max_damage_player.battle_against(heuristic_player, n_battles=1000)

    # print(
    #     "max_damage_player won %d / 1000 battles against heuristic_player (this took %f seconds)"
    #     % (
    #         max_damage_player.n_won_battles, time.time() - start
    #     )
    # )

    # # Smart vs Minimax
    # start = time.time()
    # smart_damage_player = SmartDamagePlayer(
    #     battle_format="gen8randombattle",
    # )
    # minimax_player = MinimaxPlayer(
    #     battle_format="gen8randombattle",
    # )

    # await smart_damage_player.battle_against(minimax_player, n_battles=1000)

    # print(
    #     "smart_damage_player won %d / 1000 battles against minimax_player (this took %f seconds)"
    #     % (
    #         smart_damage_player.n_won_battles, time.time() - start
    #     )
    # )

    # # Smart vs SMart Minimax
    # start = time.time()
    # smart_damage_player = SmartDamagePlayer(
    #     battle_format="gen8randombattle",
    # )
    # smart_minimax_player = SmartMinimaxPlayer(
    #     battle_format="gen8randombattle",
    # )

    # await smart_damage_player.battle_against(smart_minimax_player, n_battles=1000)

    # print(
    #     "smart_damage_player won %d / 1000 battles against smart_minimax_player (this took %f seconds)"
    #     % (
    #         smart_damage_player.n_won_battles, time.time() - start
    #     )
    # )

    # # Smart vs Heuristic
    # start = time.time()
    # smart_damage_player = SmartDamagePlayer(
    #     battle_format="gen8randombattle",
    # )
    # heuristic_player = SimpleHeuristicsPlayer(
    #     battle_format="gen8randombattle",
    # )

    # await smart_damage_player.battle_against(heuristic_player, n_battles=1000)

    # print(
    #     "smart_damage_player won %d / 1000 battles against heuristic_player (this took %f seconds)"
    #     % (
    #         smart_damage_player.n_won_battles, time.time() - start
    #     )
    # )

    # # Minimax vs Heuristic
    # start = time.time()
    # minimax_player = MinimaxPlayer(
    #     battle_format="gen8randombattle",
    # )
    # heuristic_player = SimpleHeuristicsPlayer(
    #     battle_format="gen8randombattle",
    # )

    # await minimax_player.battle_against(heuristic_player, n_battles=1000)

    # print(
    #     "minimax_player won %d / 1000 battles against heuristic_player (this took %f seconds)"
    #     % (
    #         minimax_player.n_won_battles, time.time() - start
    #     )
    # )

