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
            self.true_valid = getAllValidSequences(rule_tree)
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

    def chooseCard(self):
        """
        This function chooses which card to play next

        Returns
        -------
        card: str
            The next card to play
        """
        # TODO: implement it
        return random.choice(ALL_CARDS)

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
                # Suppose the rule_set was p & q and the given cards can be
                # descibed by p & q & r & s. Now we search all card sequences
                # that are only accepted by this rule_set and find the set of
                # their properties, which becomes {p, q, r, t, u}. Now the
                # updated rule_set should be p & q & !s, since s was not in
                # the set of attributes that previous accepted card sequences
                # had.
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
                new_rule_set = []
                for r in rule_set:
                    if not parse(r).evaluate(cards):
                        new_rule_set.append(r)
                rule_set.clear()
                for r in new_rule_set:
                    rule_set.append(r)

    def simplifyRules(self):
        """
        This function gets rid of any redundant rules
        """
        pass

    def scientist(self):
        """
        The function that runs the game. It plays 20 cards and tries to
        guess the rule
        :return:
        """
        cards = self.getValidCards()
        print("got valid cards:", cards)
        for card in cards:
            self.board_state.append((card, []))
        # Since applying the rules requires three cards to be given, therefore
        # for the first two given cards, we populate the hypothesis set
        # manually
        one_card_rules = list(set(getRulesForOneCard(cards[0])) &
                              set(getRulesForOneCard(cards[1])))
        two_card_rules = getRulesForTwoCards(cards)

        self.hypothesis_set.append(one_card_rules + two_card_rules)
        print("The current guess is", combineListOfRules(self.hypothesis_set))

        for turn in range(20):
            print("Turn:", turn)
            chosen = self.chooseCard()
            print("Playing", chosen, "card")
            if self.play(chosen):
                print(chosen, "was legal")
                self.applyAcceptedCard(chosen)
            else:
                print(chosen, "was illegal")
                self.applyRejectedCard(chosen)
            self.simplifyRules()
            print("Current Score is", self.score())
            print(self.boardState(), "\n")

        return self.findBestRule()

    def score(self):
        """
        This function returns the score for the game played so far
        TODO: NEED TO ADD THE +30 FOR A RULE THAT DOESN'T DESCRIBE ALL CARDS

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

        guessedRule = self.findBestRule()
        validReal = set(self.true_valid)
        validGuess = set(getAllValidSequences(guessedRule))

        # If the two sets of valid sequences are the same,
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
        if valid:
            self.board_state.append((card, []))
        else:
            self.board_state[-1][1].append(card)
        return valid

    def findBestRule(self):
        """
        Returns the most likely rule guessed so far

        Returns
        -------
        rule: tree
            The rule tree describing the most likely rule guessed so far
        """
        # NOTE: right now just returns the most specific rule
        return combineListOfRules(self.hypothesis_set)

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
            if self.true_rule.evaluate([card1, card2, card3]):
                for card4 in shuffleList:
                    if card4 == card3 or card4 == card2:
                        continue
                    if self.true_rule.evaluate([card2, card3, card4]):
                        # returns two cards that have both been "current"
                        return [card3, card4]
