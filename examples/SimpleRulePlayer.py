# -*- coding: utf-8 -*-
import asyncio
import time

from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer


class SimpleRulePlayer(Player):

    #check if there is a sleep move
    @staticmethod
    def check_sleep(battle):
        for move in battle.available_moves:
            if "slp" == move.status:
                return True
        return False

        #check if opponent has sleep move
    @staticmethod
    def check_opp_sleep(battle):
        for move in battle.opponent_available_moves:
            if "slp" == move.status:
                return True
        return False

    # check if any pokemon have a status effect
    @staticmethod
    def check_if_status(battle):
        for pokemon in battle.active_pokemon:
            if pokemon.status:
                return False
        for pokemon in battle.opponent_active_pokemon:
            if pokemon.status:
                return False  
        return True

    @staticmethod
    def get_sleep_move(battle):
        for move in battle.availabe_moves:
            if move.status == "slp":
                return move
        return None

    @staticmethod
    def get_heal(battle):
        heals = {}
        for move in battle.available_moves:
            if move.heal > 0:
                heals.add(move)
        return max(heals)

    @staticmethod
    def get_toxic(battle):
        for move in battle.available_moves:
            if "toxic" == move.id:
                return move
        return None

    @staticmethod
    def get_willowisp(battle):
        for move in battle.available_moves:
            if "willowisp" == move.id:
                return move
        return None

    @staticmethod
    def get_thunderwave(battle):
        for move in battle.available_moves:
            if "thunderwave" == move.id:
                return move
        return None

    # return max damage
    @staticmethod
    def get_max_damage(moves):
        
        # If the player can attack, it will
        if moves:
            # Finds the best move among available ones
            best_move = max(moves, key=lambda move: move.base_power)
            return best_move

        # If no attack is available, a random switch will be made
        else:
            return None

    def choose_move(self, battle):
        maxDamage = self.get_max_damage(battle.available_moves)
        oppMaxDamage = self.get_max_damage(battle.opponent_active_pokemon.moves)
        # if speed > opp speed
        if(battle.active_pokemon.base_stats["spd"] > battle.opponent_active_pokemon.base_stats["spd"]):
             # if max damage * .925 > oppHealth
            if(maxDamage.base_power * 0.925 > battle.opponent_active_pokemon.current_hp):
                #do max damage move
                return maxDamage
            # if both have sleep move and no enemy has a status effect
            if(self.check_sleep(battle) and self.check_opp_sleep(battle) and self.check_if_status(battle)):
                # use sleep move
                return self.get_sleep_move(battle)
            # if oppMaxDamage < 50% of maxHealth && health < 50% && have healing move
            if(oppMaxDamage.base_power < 0.5 * battle.active_pokemon.max_hp and battle.active_pokemon.current_hp < 0.5 * battle.active_pokemon.max_hp and self.get_heal(battle)):
                # use healing move
                return self.get_heal(battle)
        # if maxDamage < 20% of oppMaxHealth && oppMaxDamage < 30% of maxHealth && have toxic
        if(maxDamage.base_power < 0.2 * battle.opponent_active_pokemon.max_hp and oppMaxDamage.base_power < 0.3 * battle.active_pokemon.max_hp and self.get_toxic(battle)):
            # return toxic move
            return self.get_toxic(battle)
        #if maxDamage < 20% of oppMaxHealth && oppMaxDamage < 30% of maxHealth && have willofthewisp && oppAttack > oppPhysicalAttack
        if(maxDamage.base_power < 0.2 * battle.opponent_active_pokemon.max_hp and oppMaxDamage.base_power < 0.3 * battle.active_pokemon.max_hp and self.get_willowisp(battle)):
            # return willofthewisp
            return self.get_willowisp(battle)
        # if maxDamage < 20% of oppMaxHealth && oppMaxDamage < 30% of maxHealth && have thunderwave
        if(maxDamage.base_power < 0.2 * battle.opponent_active_pokemon.max_hp and oppMaxDamage.base_power < 0.3 * battle.active_pokemon.max_hp and self.get_thunderwave(battle)):
            # return thunderwave
            return self.get_thunerwave(battle)
        # if maxDamage < 30% of oppMaxHealth && oppMaxDamage > curHealth
        if(maxDamage.base_power < 0.3 * battle.opponent_active_pokemon.max_hp and oppMaxDamage.base_power > battle.active_pokemon.current_hp):
            #return switch to minimum damage of pokemon
             return self.create_order(
                max(
                    battle.available_switches,
                    key=lambda s: self._estimate_matchup(s, battle.opponent.active_pokemon),
                )
            )
        #default to maxDamage
        if(maxDamage):
            return maxDamage
        return self.choose_random_move()

    



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
