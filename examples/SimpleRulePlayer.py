# -*- coding: utf-8 -*-
import asyncio
import time

from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer


class SimpleRulePlayer(Player):

    #check if there is a sleep move
    def check_sleep(battle):
        for move in battle.available_moves:
            if "slp" == move.status:
                return True
        return False

        #check if opponent has sleep move
    def check_opp_sleep(battle):
        for move in battle.opponent_available_moves:
            if "slp" == move.status:
                return True
        return False

    # check if any pokemon have a status effect
    def check_if_status(battle):
        for pokemon in battle.active_pokemon:
            if pokemon.status:
                return False
        for pokemon in battle.opponent_active_pokemon:
            if pokemon.status:
                return False  
        return True

    def get_sleep_move(self, battle):
        for move in battle.availabe_moves:
            if move.status == "slp":
                return move
        return self.choose_random_move

    def get_heal(battle):
        heals = {}
        for move in battle.available_moves:
            if move.heal > 0:
                heals.add(move)
        return max(heals)

    def get_toxic(battle):
        for move in battle.available_moves:
            if "toxic" == move.id:
                return move
        return None

    def get_willowisp(battle):
        for move in battle.available_moves:
            if "willowisp" == move.id:
                return move
        return None

    def get_thunderwave(battle):
        for move in battle.available_moves:
            if "thunderwave" == move.id:
                return move
        return None

    # return max damage
    def get_max_damage(self, battle):
        
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available ones
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return best_move

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)

    def choose_move(self, battle):
        maxDamage = get_max_damage(self, battle)
        oppMaxDamage = get_max_damage(battle.opponent, battle)
        # if speed > opp speed
        if(battle.active_pokemon.base_stats["spd"] > battle.opponent_active_pokemon.base_stats["spd"]):
             # if max damage * .925 > oppHealth
            if(maxDamage.base_power * 0.925 > battle.opponent_active_pokemon.current_hp):
                #do max damage move
                return maxDamage
            # if both have sleep move and no enemy has a status effect
            if(check_sleep(battle) and check_opp_sleep(battle) and check_if_status(battle)):
                # use sleep move
                return get_sleep_move(self, battle)
            # if oppMaxDamage < 50% of maxHealth && health < 50% && have healing move
            if(oppMaxDamage < 0.5 * battle.active_pokemon.max_hp and battle.active_pokemon.current_hp < 0.5 * battle.active_pokemon.max_hp and get_heal(battle)):
                # use healing move
                return get_heal(battle)
        # if maxDamage < 20% of oppMaxHealth && oppMaxDamage < 30% of maxHealth && have toxic
        if(maxDamage < 0.2 * battle.opponent_active_pokemon.max_hp and oppMaxDamage < 0.3 * battle.active_pokemon.max_hp and get_toxic(battle)):
            # return toxic move
            return get_toxic(battle)
        #if maxDamage < 20% of oppMaxHealth && oppMaxDamage < 30% of maxHealth && have willofthewisp && oppAttack > oppPhysicalAttack
        if(maxDamage < 0.2 * battle.opponent_active_pokemon.max_hp and oppMaxDamage < 0.3 * battle.active_pokemon.max_hp and get_willowisp(battle)):
            # return willofthewisp
            return get_willowisp(battle)
        # if maxDamage < 20% of oppMaxHealth && oppMaxDamage < 30% of maxHealth && have thunderwave
        if(maxDamage < 0.2 * battle.opponent_active_pokemon.max_hp and oppMaxDamage < 0.3 * battle.active_pokemon.max_hp and get_thunderwave(battle)):
            # return thunderwave
            return get_thunerwave(battle)
        # if maxDamage < 30% of oppMaxHealth && oppMaxDamage > curHealth
        if(maxDamage < 0.3 * battle.opponent_active_pokemon.max_hp and oppMaxDamage > battle.active_pokemon.current_hp):
            #return switch to minimum damage of pokemon
             return self.create_order(
                max(
                    battle.available_switches,
                    key=lambda s: self._estimate_matchup(s, battle.opponent.active_pokemon),
                )
            )
        #default to maxDamage
        return maxDamage

    



async def main():
    start = time.time()

    # We create two players.
    random_player = RandomPlayer(battle_format="gen8randombattle")
    simple_rule_player = SimpleRulePlayer(battle_format="gen8randombattle")

    # Now, let's evaluate our player
    await simple_rule_player.battle_against(random_player, n_battles=100)

    print(
        "Max damage player won %d / 100 battles [this took %f seconds]"
        % (simple_rule_player.n_won_battles, time.time() - start)
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
