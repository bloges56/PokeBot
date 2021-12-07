# -*- coding: utf-8 -*-
import asyncio
from os import stat
import time

from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer
from MiniMax import MinimaxPlayer


class SimpleRulePlayer(Player):

    SPEED_TIER_COEFICIENT = 0.1
    HP_FRACTION_COEFICIENT = 0.4
    SWITCH_OUT_MATCHUP_THRESHOLD = -2

    def _estimate_matchup(self, mon, opponent):
        score = max([opponent.damage_multiplier(t) for t in mon.types if t is not None])
        score -= max(
            [mon.damage_multiplier(t) for t in opponent.types if t is not None]
        )
        if mon.base_stats["spe"] > opponent.base_stats["spe"]:
            score += self.SPEED_TIER_COEFICIENT
        elif opponent.base_stats["spe"] > mon.base_stats["spe"]:
            score -= self.SPEED_TIER_COEFICIENT

        score += mon.current_hp_fraction * self.HP_FRACTION_COEFICIENT
        score -= opponent.current_hp_fraction * self.HP_FRACTION_COEFICIENT

        return score
    
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

    def get_sleep_move(self, battle):
        for move in battle.availabe_moves:
            if move.status == "slp":
                return self.create_order(move)
        return None

    def get_heal(self, battle):
        heals = []
        for move in battle.available_moves:
            if move.heal > 0:
                heals.append(move)
        if heals:
            return self.create_order(max(heals))
        return None

    def get_toxic(self, battle):
        for move in battle.available_moves:
            if "toxic" == move.id:
                return self.create_order(move)
        return None

    def get_willowisp(self, battle):
        for move in battle.available_moves:
            if "willowisp" == move.id:
                return self.create_order(move)
        return None

    def get_thunderwave(self, battle):
        for move in battle.available_moves:
            if "thunderwave" == move.id:
                return self.create_order(move)
        return None

    # return max damage
    @staticmethod
    def get_max_damage(battle):
        
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available ones
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return best_move.base_power

        # If no attack is available, a random switch will be made
        else:
            return 0

    @staticmethod
    def get_opp_max_damage(battle):
        
        # If the player can attack, it will
        if battle.opponent_active_pokemon.moves:
            # Finds the best move among available ones
            best_move = max(list(battle.opponent_active_pokemon.moves.values()), key=lambda move: move.base_power)
            return best_move.base_power

        # If no attack is available, a random switch will be made
        else:
            return 0

    # return max damage
    def get_max_move(self, battle):
        
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available ones
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)

    def choose_move(self, battle):
        maxDamage = self.get_max_damage(battle)
        oppMaxDamage = self.get_opp_max_damage(battle)
        # if speed > opp speed
        if(battle.active_pokemon.base_stats["spd"] > battle.opponent_active_pokemon.base_stats["spd"]):
             # if max damage * .925 > oppHealth
            if(maxDamage * 0.925 > battle.opponent_active_pokemon.current_hp):
                #do max damage move
                return self.get_max_move(battle)
            # if both have sleep move and no enemy has a status effect
            if(self.check_sleep(battle) and self.check_opp_sleep(battle) and self.check_if_status(battle)):
                # use sleep move
                return self.get_sleep_move(battle)
            # if oppMaxDamage < 50% of maxHealth && health < 50% && have healing move
            if(oppMaxDamage < 0.5 * battle.active_pokemon.max_hp and battle.active_pokemon.current_hp < 0.5 * battle.active_pokemon.max_hp and self.get_heal(battle)):
                # use healing move
                return self.get_heal(battle)
        # if maxDamage < 20% of oppMaxHealth && oppMaxDamage < 30% of maxHealth && have toxic
        if(maxDamage < 0.2 * battle.opponent_active_pokemon.max_hp and oppMaxDamage < 0.3 * battle.active_pokemon.max_hp and self.get_toxic(battle)):
            # return toxic move
            return self.get_toxic(battle)
        #if maxDamage < 20% of oppMaxHealth && oppMaxDamage < 30% of maxHealth && have willofthewisp && oppAttack > oppPhysicalAttack
        if(maxDamage < 0.2 * battle.opponent_active_pokemon.max_hp and oppMaxDamage < 0.3 * battle.active_pokemon.max_hp and self.get_willowisp(battle)):
            # return willofthewisp
            return self.get_willowisp(battle)
        # if maxDamage < 20% of oppMaxHealth && oppMaxDamage < 30% of maxHealth && have thunderwave
        if(maxDamage < 0.2 * battle.opponent_active_pokemon.max_hp and oppMaxDamage < 0.3 * battle.active_pokemon.max_hp and self.get_thunderwave(battle)):
            # return thunderwave
            return self.get_thunderwave(battle)
        # if maxDamage < 30% of oppMaxHealth && oppMaxDamage > curHealth
        if(battle.available_switches and maxDamage < 0.3 * battle.opponent_active_pokemon.max_hp and oppMaxDamage > battle.active_pokemon.current_hp):
            #return switch to minimum damage of pokemon
             return self.create_order(max(battle.available_switches,key=lambda s: self._estimate_matchup(s, battle.opponent_active_pokemon)))
        #default to maxDamage
        return self.get_max_move(battle)

    



async def main():
    start = time.time()

    # We create two players.
    random_player = MinimaxPlayer(battle_format="gen8randombattle")
    simple_rule_player = SimpleRulePlayer(battle_format="gen8randombattle")

    # Now, let's evaluate our player
    await simple_rule_player.battle_against(random_player, n_battles=100)

    print(
        "Simple rule player won %d / 100 battles [this took %f seconds]"
        % (simple_rule_player.n_won_battles, time.time() - start)
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
