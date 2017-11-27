# Put your program name in place of program_name

from Game import *
from random import randint
from new_eleusis import *

global game_ended
game_ended = False


def generate_random_card():
    values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["S", "H", "D", "C"]
    return values[randint(0, len(values) - 1)] + suits[randint(0, len(suits) - 1)]


class Player(object):

    def __init__(self, theGame):
        '''
        Initializes the player object. This takes in a Game object that stores the board state used by play
        :param self:
        '''
        self.hand = [generate_random_card() for i in range(14)]
        self.game = theGame
    def play(self, cards):
        """
        'cards' is a list of three valid cards to be given by the dealer at the beginning of the game.
        Your scientist should play a card out of its given hand OR return a rule, not both.
        'game_ended' parameter is a flag that is set to True once the game ends. It is False by default
        NOTE: added a default value for cards
        """
        return self.game.scientist(cards, self.hand, game_ended)


class Adversary(object):
    def __init__(self):
        self.hand = [generate_random_card() for i in range(14)]

    def play(self):
        """
        'cards' is a list of three valid cards to be given by the dealer at the beginning of the game.
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

theGame = Game()
# The players in the game
player = Player(theGame)
adversary1 = Adversary()
adversary2 = Adversary()
adversary3 = Adversary()

# Set a rule for testing
#rule = "if(is_royal(current), False, True)"
rule = "equal(is_royal(current), False)"
theGame.setRule(rule)

# The three cards that adhere to the rule
cards = ["10H", "2C", "4S"]

"""
In each round scientist is called and you need to return a card or rule.
The cards passed to scientist are the last 3 cards played.
Use these to update your board state.
"""
for round_num in range(14):
    # Each player plays a card or guesses a rule
    try:
        print("Board state at beginning of round:\n",player.game.boardState())
        # Player 1 plays
        player_card_rule = player.play(cards)
        print("Result from player:",player_card_rule)
        if is_card(player_card_rule):
            del cards[0]
            cards.append(player_card_rule)
        else:
            raise Exception('')

        # Adversary 1 plays
        ad1_card_rule = adversary1.play()
        print("Result from adversary 1:",ad1_card_rule)
        if is_card(ad1_card_rule):
            del cards[0]
            cards.append(ad1_card_rule)
            # print cards
        else:
            raise Exception('')

        # Adversary 2 plays
        ad2_card_rule = adversary2.play()
        print("Result from adversary 2:", ad2_card_rule)
        if is_card(ad2_card_rule):
            del cards[0]
            cards.append(ad2_card_rule)
            # print cards
        else:
            raise Exception('')

        # Adversary 3 plays
        ad3_card_rule = adversary3.play()
        print("Result from adversary 3:", ad3_card_rule)
        if is_card(ad3_card_rule):
            del cards[0]
            cards.append(ad3_card_rule)
            # print cards
        else:
            raise Exception('')

    except:
        game_ended = True
        break

# Everyone has to guess a rule

rule_player = player.play(cards)
print("The final board state is",player.game.boardState())
print("The rule guessed was",rule_player)
# Check if the guessed rule is correct and print the score
print("The score is",theGame.score())
