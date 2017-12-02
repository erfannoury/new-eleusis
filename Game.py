"""
Contains the Player class
"""
import random
from rule_functions import *
import phase2


class Player:
    """
    The Player class which contains the logic of the New Eleusis game.

    Parameters
    ----------
    cards: list
        The initial list of legal cards from the dealer which starts the game.
    max_rule_constancy: int
        The maximum number of turns where if the hypothesis set stays unchanged
        then we can declare the game finished and return a rule.
    """

    def __init__(self, cards, max_rule_constancy=5):
        assert len(cards) == 3
        self.board_state = []
        for c in cards:
            self.board_state.append((c, []))
        self.hypothesis_set = []
        self.applyAcceptedCard(cards[2])

        self.hand = [generate_random_card() for i in range(14)]

        self.max_rule_constancy = max_rule_constancy
        self.constant_rule_count = 0
        self.turn = 0

    def boardState(self):
        """
        This function returns the list of cards played so far

        Returns
        -------
        board_state: list
            The list describing the state of the game so far
        """
        return self.board_state

    def chooseCard(self):
        """
        This function chooses which card to play next

        Returns
        -------
        card: str
            The next card to play

        """
        prev = self.board_state[-1][0]
        prev2 = self.board_state[-2][0]

        random.shuffle(self.hand)

        rule_tree = parse(combineListOfRules(self.hypothesis_set))

        if self.turn % 2 == 0:
            for cur in self.hand:
                if rule_tree.evaluate([prev2, prev, cur]):
                    return cur
        else:
            for cur in self.hand:
                if not rule_tree.evaluate([prev2, prev, cur]):
                    return cur
        return random.choice(self.hand)

    def applyAcceptedCard(self, current):
        """
        This function adapts the rules for when a card is accepted
        (if necessary)

        Parameters
        ----------
        current: str
            The card that was accepted
        """
        assert current == self.board_state[-1][0]
        previous = self.board_state[-2][0]
        previous2 = self.board_state[-3][0]
        cards = [previous2, previous, current]

        rule_changed = False
        # first check to see if any of the rule sets accept this card
        for rule_set in self.hypothesis_set:
            if parse(combineRulesWithOperator(rule_set, 'and')).evaluate(
                    cards):
                return

        add_new_set = True
        for rule_set in sorted(self.hypothesis_set, key=lambda rs: len(rs),
                               reverse=True):
            if not any([parse(r).evaluate(cards) for r in rule_set]):
                continue
            else:
                add_new_set = False
                new_rule_set = []
                for r in rule_set:
                    if parse(r).evaluate(cards):
                        new_rule_set.append(r)
                if len(rule_set) != len(new_rule_set):
                    rule_changed = True
                rule_set.clear()
                for r in new_rule_set:
                    rule_set.append(r)

        if add_new_set:
            rule_changed = True
            self.hypothesis_set.append(getRulesForSequence(cards))

        new_hypothesis_set = []
        for rule_set in self.hypothesis_set:
            if len(rule_set) > 0:
                new_hypothesis_set.append(rule_set)

        self.hypothesis_set = new_hypothesis_set

        if rule_changed:
            self.constant_rule_count = 0

    def applyRejectedCard(self, current):
        """
        This function adapts the rules for when a card is rejected
        (if necessary)

        If a rule r1 (which is a disjunction of a number of predicates) accept
        a cards sequence, then every predicate in rule r1 holds for the cards
        sequence. Therefore, if we write r1 as p & q,

        Parameters
        ----------
        current: str
            The card that was rejected
        """
        assert current == self.board_state[-1][1][-1]
        previous = self.board_state[-1][0]
        previous2 = self.board_state[-2][0]
        cards = [previous2, previous, current]

        rule_changed = False

        for rule_set in sorted(self.hypothesis_set, key=lambda rs: len(rs)):
            if parse(
                    combineRulesWithOperator(rule_set, 'and')).evaluate(cards):
                rule_changed = True
                # all of the subrules were true for this cards, what should
                # be done?
                # Suppose the rule_set was p & q and the given rejected cards
                # can be described by p & q & r & s. Now we search all card
                # sequences that are only accepted by this rule_set and find
                # the set of their properties, which becomes {p, q, r, t, u}.
                # Now the updated rule_set should be p & q & !s, since s was
                # not in the set of attributes that previous accepted card
                # sequences had.
                attr_set = set()
                for i in range(len(self.board_state) - 2):
                    c_seq = list(
                        map(lambda c: c[0], self.board_state[i:i + 3]))
                    if not any([parse(
                            combineRulesWithOperator(rs, 'and')).evaluate(c_seq)
                            for rs in self.hypothesis_set if rs != rule_set]):
                        attr_set.update(getRulesForSequence(c_seq))

                neg_rules = []
                for r in getRulesForSequence(cards):
                    if (r not in rule_set) and (r not in attr_set):
                        neg_rules.append(r)

                for r in neg_rules:
                    rule_set.append(negate_rule(r))

            else:
                # if the rule didn't accept the card, then there is no need
                # to change the rule, we can leave it as is
                continue

        new_hypothesis_set = []
        for rule_set in self.hypothesis_set:
            if len(rule_set) > 0:
                new_hypothesis_set.append(rule_set)

        self.hypothesis_set = new_hypothesis_set

        if rule_changed:
            self.constant_rule_count = 0

    def simplifyRules(self):
        """
        This function gets rid of any redundant rules
        """
        return combineListOfRules(self.hypothesis_set)

    def update_card_to_boardstate(self, card, result):
        """
        Update your board state with card based on the result

        Parameters
        ----------
        card: str
            The card that was played
        result: bool
            Whether the dealer accepted the card or not
        """
        self.turn += 1
        self.constant_rule_count += 1

        if result:
            self.board_state.append((card, []))
            self.applyAcceptedCard(card)
        else:
            self.board_state[-1][1].append(card)
            self.applyRejectedCard(card)

    def play(self):
        """
        Either plays a card or returns a rule

        Returns
        -------
        chosen: str
            The next card to be played
        OR
        rule: str
            The rule hypothesized so far
        """
        if phase2.game_ended:
            return combineListOfRules(self.hypothesis_set)

        if self.constant_rule_count == self.max_rule_constancy:
            phase2.game_ended = True
            return combineListOfRules(self.hypothesis_set)

        chosen = self.chooseCard()
        self.hand.append(generate_random_card())
        del self.hand[self.hand.index(chosen)]
        return chosen


class Scorer:
    """
    The Scorer class which implements a function that scores players

    Parameters
    ----------
    rule_expr: str
        String representation of a rule
    """
    def __init__(self, rule_expr):
        self.setRule(rule_expr)

    def rule(self):
        """
        This function returns the true game rule to the user

        Returns
        -----------
        true_rule: Tree
            The rule tree that we have estimated so far in the game
        """
        return self.true_rule

    def setRule(self, rule_expr):
        """
        This function sets a given rule for a game

        Parameters
        ----------
        rule_expr: str
            String representation of a rule
        """
        try:
            self.true_rule = parse(rule_expr)
        except:
            raise ValueError("Invalid Rule")

    def score(self, player, is_player):
        """
        This function returns the score for a given Player

        Parameters
        ----------
        player: object
            A Player object which implements the following functions:
                * player.boardState()
                    Which returns the board state of the game as a list of
                    tuples
                * player.play()
                    Which returns the final rule, because game_ended is set to
                    True
        is_player: bool
            Whether the given player ended the game or not

        Returns
        -------
        score: int
            Score of the game played for the given player
        """
        print("Inside the score function")
        score = 0
        cardsPlayed = 0
        boardState = player.boardState()

        for play in boardState:
            # look at legal plays
            # +1 for every successful play over 20 cards and under 200 cards
            cardsPlayed += 1
            if cardsPlayed > 20:
                score += 1

            # look at illegal plays
            # +2 for every unsuccessful play
            for card in play[1]:
                cardsPlayed += 1
                score += 2

        phase2.game_ended = True

        guessedRule = player.play()
        assert not is_card(guessedRule)

        # Now check that the rule describes all of the cards played
        describes = True
        guessedTree = parse(guessedRule)
        for i in range(2, len(boardState)):
            if not guessedTree.evaluate(
                    [boardState[i - 2][0], boardState[i - 1][0],
                     boardState[i][0]]):
                describes = False
            for failedCard in boardState[i][1]:
                if guessedTree.evaluate(
                        [boardState[i - 1][0], boardState[i][0],
                         failedCard]):
                    describes = False
        if not describes:
            # +30 for a rule that does not describe all cards on the board
            score += 30

        validReal = set(getAllValidSequences(self.true_rule))
        validGuess = set(getAllValidSequences(guessedTree))
        # the rules are the same
        if len(validGuess ^ validReal) > 0:
            # +15 for a rule that is not equivalent to the correct rule
            score += 15
        else:
            # Each player that guesses the correct rule with few or no extra
            # terms, receives an additional bonus of -75 points
            score -= 75
            if is_player:
                # If the player that ended the game gives the correct rule,
                # it receives an additional -25 points
                score -= 25

        return score
