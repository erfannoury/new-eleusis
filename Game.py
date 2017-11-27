"""
Contains the Game class
"""
from rule_functions import *


class Game:
    """
    The Game class which contains the logic of the New Eleusis game.

    Parameters
    ----------
    board_state: list
        A list of tuples, where the first item of the tuple is a card
        that has been accepted as legal in the sequence and the second tuple
        is a list (can be empty) which are the cards played after the last
        legal card which were illegal according to the dealer.
    hypothesis_set: list
        A list of lists, in which the inner lists contain a number of rules
        that are disjuncted and the resulting rules from the inner lists are
        then conjuncted to create the final rule.
    """
    def __init__(self, board_state=None, hypothesis_set=None):
        # Note the true rule gets defined later
        self.board_state = board_state
        self.hypothesis_set = hypothesis_set

        # If they are not initialized, make them empty lists
        if board_state is None:
            self.board_state = []
        if hypothesis_set is None:
            self.hypothesis_set = []

    def rule(self):
        """
        This function returns the game rule to the user

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
            rule_tree = parse(rule_expr)
            self.true_rule = rule_tree
        except:
            raise ValueError("Invalid Rule")

    def boardState(self):
        """
        This function returns the list of cards played so far

        Returns
        -------
        board_state: list
            The list describing the state of the game so far
        """
        return self.board_state

    def chooseCard(self, hand):
        """
        This function chooses which card to play next
        It takes in the available cards as a list called hand
        Returns
        -------
        card: str
            The next card to play

        """
        #Get which turn we are on from how many cards have been played
        turn = -3
        for item in self.board_state:
            #add one for the accepted card, and the number of rejected cards
            turn += len(item[1]) + 1


        prev = self.board_state[-1][0]
        prev2 = self.board_state[-2][0]

        rule_tree = parse(combineListOfRules(self.hypothesis_set))
        if turn % 2 == 0:
            for cur in hand:
                if rule_tree.evaluate([prev2, prev, cur]):
                    return cur
        else:
            for cur in hand:
                if not rule_tree.evaluate([prev2, prev, cur]):
                    return cur
        return random.choice(hand)

    def applyAcceptedCard(self, current):
        """
        This function adapts the rules for when a card is accepted
        (if necessary)

        Parameters
        ----------
        current: str
            The card that was accepted
        """
        previous = self.board_state[-2][0]
        previous2 = self.board_state[-3][0]
        cards = [previous2, previous, current]

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
                rule_set.clear()
                for r in new_rule_set:
                    rule_set.append(r)

        if add_new_set:
            self.hypothesis_set.append(getRulesForSequence(cards))

        new_hypothesis_set = []
        for rule_set in self.hypothesis_set:
            if len(rule_set) > 0:
                new_hypothesis_set.append(rule_set)

        self.hypothesis_set = new_hypothesis_set

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
        previous = self.board_state[-1][0]
        previous2 = self.board_state[-2][0]
        cards = [previous2, previous, current]

        for rule_set in sorted(self.hypothesis_set, key=lambda rs: len(rs)):
            if parse(
                combineRulesWithOperator(rule_set, 'and')).evaluate(cards):
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
                    c_seq = list(map(lambda c: c[0], self.board_state[i:i+3]))
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

    def simplifyRules(self):
        """
        This function gets rid of any redundant rules
        """
        pass

    def scientist(self, cards, hand, game_ended):
        """
        The function that plays a card and returns either a rule or the card played

        Returns
        -------
        A rule or the card played

        """

        if len(self.hypothesis_set) == 0:
            for card in cards:
                self.board_state.append((card, []))
            #We get three cards to start with, so make the initial hypothesis
            self.hypothesis_set.append(getRulesForSequence(cards))
        else:
            #apply the cards played by the other players to our understanding of the game
            for card in cards:
                if is_card(card):
                    if self.play(card):
                        self.applyAcceptedCard(card)
                    else:
                        self.applyRejectedCard(card)

        if game_ended:
            return combineListOfRules(self.hypothesis_set)


        chosen = self.chooseCard(hand)
        if self.play(chosen):
            self.applyAcceptedCard(chosen)
        else:
            self.applyRejectedCard(chosen)
        self.simplifyRules()

        #return combineListOfRules(self.hypothesis_set)
        #TODO: return a rule if it hasn't changed in L amount of turns
        return chosen

    def score(self):
        """
        This function returns the score for the game played so far

        Returns
        -------
        score: int
            Score of the game played so far
        """
        score = 0
        cardsPlayed = 0

        for play in self.board_state:
            # look at legal plays
            cardsPlayed += 1
            if cardsPlayed > 20:
                score += 1

            # look at illegal plays
            for card in play[1]:
                cardsPlayed += 1
                if cardsPlayed > 20:
                    score += 2

        guessedRule = combineListOfRules(self.hypothesis_set)
        # Now check that the rule describes all of the cards played
        describes = True
        guessedTree = parse(guessedRule)
        for i in range(2,len(self.board_state)):
            if not guessedTree.evaluate(
                [self.board_state[i-2][0], self.board_state[i-1][0],
                 self.board_state[i][0]]):
                describes = False
            for failedCard in self.board_state[i][1]:
                if guessedTree.evaluate(
                    [self.board_state[i-1][0], self.board_state[i][0],
                     failedCard]):
                    describes = False
        if not describes:
            score += 30

        validReal = set(getAllValidSequences(self.true_rule))
        validGuess = set(getAllValidSequences(guessedTree))
        # the rules are the same
        if len(validGuess ^ validReal) > 0:
            score += 15
        return score

    def play(self, card):
        """
        Plays the card and returns whether or not it was valid.
        Also adds it to the board state

        Parameters
        ----------
        card: str
            The card that the player has played

        Returns
        -------
        valid: bool
            Whether the card played was legal or not
        """
        previous = self.board_state[-1][0]
        previous2 = self.board_state[-2][0]
        valid = self.true_rule.evaluate([previous2, previous, card])
        if isinstance(valid,str):
            if valid == "True":
                self.board_state.append((card, []))
                valid = True
            else:
                self.board_state[-1][1].append(card)
                valid = False
        else:
            if valid:
                self.board_state.append((card, []))
            else:
                self.board_state[-1][1].append(card)
        return valid

    def getValidCards(self):
        """
        Gets a card or set of cards that is valid with the game rule
        (only called for the first turn)

        Returns
        -------
        cards: list
            A list of two cards that are accepted by the rule of the game, to
            begin the game
        """
        # Keeps getting sets of three random cards until we have three that
        # have worked as "current"
        # This is because for a 1-card rule, the first two cards don't matter
        shuffleList = ALL_CARDS
        random.shuffle(shuffleList)
        for card1, card2, card3 in combinations(shuffleList, r=3):
            good = self.true_rule.evaluate([card1, card2, card3])
            if good == "True" or (good != "False" and good != False):
                for card4 in shuffleList:
                    if card4 == card3 or card4 == card2:
                        continue
                    if self.true_rule.evaluate([card2, card3, card4]):
                        # returns two cards that have both been "current"
                        return [card3, card4]
