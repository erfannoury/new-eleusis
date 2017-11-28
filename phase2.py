# Put your program name in place of program_name

from Game import *
from random import randint
from new_eleusis import *

global game_ended
game_ended = False





class Adversary(object):
    def __init__(self):
        self.hand = [generate_random_card() for i in range(14)]

    def play(self):
        """
        'cards' is a list of three valid cards to be given by the dealer at
        the beginning of the game.
        Your scientist should play a card out of its given hand.
        """
        # Return a rule with a probability of 1/14
        prob_list = [i for i in range(14)]
        prob = prob_list[randint(0, 13)]
        if prob == 4:
            # Generate a random rule
            rule = ""
            conditions = ["equal", "greater"]
            properties = ["suit", "value"]
            cond = conditions[randint(0, len(properties) - 1)]
            if cond == "greater":
                prop = "value"
            else:
                prop = properties[randint(0, len(properties) - 1)]

            rule += cond + "(" + prop + "(current), " + prop + "(previous)), "
            return rule[:-2] + ")"
        else:
            return self.hand[randint(0, len(self.hand) - 1)]


if __name__ == '__main__':
    # Set a rule for testing
    rule = "if(is_royal(current), False)"
    judge = Scorer()
    judge.setRule(rule)


    cards = ["10H", "2C", "4S"]
    tree = parse(rule)

    player = Player(cards)
    adversary1 = Adversary()
    adversary2 = Adversary()
    adversary3 = Adversary()

    #The score function needs to know if this was the player that ended the game
    ended_player = 0

    for round_num in range(14):
        try:
            # Player 1 plays
            player_card_rule = player.play()
            print("The player played",player_card_rule)
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
            print("Adversary 1 played",ad1_card_rule)
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

            print("The board state is:",player.boardState())

        except:
            print("The game ends!")
            game_ended = True
            break



    # Everyone has to guess a rule
    rule_player = player.play(True)
    print("The rule guessed by the player was",rule_player)

    # Check if the guessed rule is correct and print the score
    is_player = (ended_player == 0)
    the_score = judge.score(player, is_player)
    print("The score for player was ",the_score)
