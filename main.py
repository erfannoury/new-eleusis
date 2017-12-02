"""
This file tests the runnning of the game
"""
import phase2
import Game
from rule_functions import parse, is_card


def main():
    # Set a rule for testing
    rule = "if(is_royal(current), False)"
    judge = Game.Scorer(rule)

    cards = ["10H", "2C", "4S"]
    tree = parse(rule)

    player = Game.Player(cards)
    adversary1 = phase2.Adversary()
    adversary2 = phase2.Adversary()
    adversary3 = phase2.Adversary()

    # The score function needs to know if this was the player that ended the
    # game
    ended_player = 0

    for round_num in range(14):
        try:
            # Player 1 plays
            player_card_rule = player.play()
            print("The player played", player_card_rule)
            if is_card(player_card_rule):
                # checking whether card played is correct or wrong
                temp_cards = [cards[-2], cards[-1], player_card_rule]
                result = tree.evaluate(tuple(temp_cards))
                if result:
                    del cards[0]
                    cards.append(player_card_rule)
                # player updating board state based on card played and result
                player.update_card_to_boardstate(player_card_rule, result)
            else:
                ended_player = 0
                raise Exception('')

            # Adversary 1 plays
            ad1_card_rule = adversary1.play()
            print("Adversary 1 played", ad1_card_rule)
            if is_card(ad1_card_rule):
                temp_cards = [cards[-2], cards[-1], ad1_card_rule]
                result = tree.evaluate(tuple(temp_cards))
                if result:
                    del cards[0]
                    cards.append(ad1_card_rule)
                player.update_card_to_boardstate(ad1_card_rule, result)
            else:
                ended_player = 1
                raise Exception('')

            # Adversary 2 plays
            ad2_card_rule = adversary2.play()
            print("Adversary 2 played", ad2_card_rule)
            if is_card(ad2_card_rule):
                temp_cards = [cards[-2], cards[-1], ad2_card_rule]
                result = tree.evaluate(tuple(temp_cards))
                if result:
                    del cards[0]
                    cards.append(ad2_card_rule)
                player.update_card_to_boardstate(ad2_card_rule, result)
            else:
                ended_player = 2
                raise Exception('')

            # Adversary 3 plays
            ad3_card_rule = adversary3.play()
            print("Adversary 3 played", ad3_card_rule)
            if is_card(ad3_card_rule):
                temp_cards = [cards[-2], cards[-1], ad3_card_rule]
                result = tree.evaluate(tuple(temp_cards))
                if result:
                    del cards[0]
                    cards.append(ad3_card_rule)
                player.update_card_to_boardstate(ad3_card_rule, result)
            else:
                ended_player = 3
                raise Exception('')

            print("The board state is:", player.boardState())

        except Exception:
            print("The game ends!")
            phase2.game_ended = True
            break

    # Everyone has to guess a rule
    rule_player = player.play()
    print("The rule guessed by the player was", rule_player)

    # Check if the guessed rule is correct and print the score
    is_player = (ended_player == 0)
    the_score = judge.score(player, is_player)
    print("The score for player was ", the_score)


if __name__ == '__main__':
    main()
