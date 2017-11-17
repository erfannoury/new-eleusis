"""
This file contains helper functions for rules
"""
import random
from new_eleusis import *
from itertools import combinations

ALL_CARDS = []
for deck in ["D", "H", "S", "C"]:
    for num in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                "J", "Q", "K"]:
        ALL_CARDS.append(num+deck)


def negate_rule(rule):
    """
    Negates the given rule expression

    Parameters
    ----------
    rule: str or new_eleusis.Tree
        String representation of a rule

    Returns
    -------
    negated_rule: str
        String representation of the negated rule
    """
    assert type(rule) in [str, Tree]
    if type(rule) == Tree:
        rule = str(rule)

    if rule.startswith('not('):
        negated_rule = rule[4:-1]
    elif rule.startswith('less('):
        negated_rule = 'greater(' + rule[5:]
    elif rule.startswith('greater('):
        negated_rule = 'less(' + rule[len('greater(') + 1:]
    else:
        negated_rule = 'not(' + rule + ')'

    return negated_rule


def getAllValidSequences(rule):
    """
    Loops over all possible lists of three cards and returns the list of three
    cards that are accepted by the given rule.

    Parameters
    ----------
    rule: Tree
        The rule that we want to find valid cards for

    Returns
    -------
    goodList: list
        List of three-cards that are accepted by the rule
    """
    goodList = []
    for card1, card2, card3 in combinations(ALL_CARDS, r=3):
        if rule.evaluate([card1, card2, card3]):
            for card4 in ALL_CARDS:
                if card4 in [card1, card2, card3]:
                    continue
                if rule.evaluate([card2, card3, card4]):
                    for card5 in ALL_CARDS:
                        if card5 in [card2, card3, card4]:
                            continue
                        if rule.evaluate([card3, card4, card5]):
                            goodList.append(card3 + card4 + card5)
    return goodList


def getRulesForSequence(cards):
    """
    Takes in a sequence of three cards and returns all possible rules for that
    ordering of cards, i.e. rules that take only one card, rules that take two,
    and finally rules that take three cards into account.

    Parameters
    ----------
    cards: list
        A list of three cards

    Returns
    -------
    all_rules: list
        A list of rule strings that accept the given sequence of three cards
    """
    assert len(cards) == 3, 'Three cards should be provided'

    cur = cards[-1]
    prev = cards[-2]
    prev2 = cards[-3]

    # for each of the three cards, get the one-card rules
    curSet = set(getRulesForOneCard(cur))
    prevSet = set(getRulesForOneCard(prev))
    prev2Set = set(getRulesForOneCard(prev2))

    # select the one-card rules that overlap for all three
    all_one_card_rules = list(curSet & prevSet & prev2Set)

    # for each pair of (previous2, previous) and (previous, current),
    # get the 2-card rules
    prev_cur = set(getRulesForTwoCards([prev, cur]))
    prev2_prev = set(getRulesForTwoCards(([prev2, prev])))

    # If there is overlap, add two-card rules based on current and previous
    all_two_card_rules = list(prev_cur & prev2_prev)

    # Get the three-card rules
    all_three_card_rules = getRulesForThreeCards(cards)

    all_rules = all_one_card_rules + all_two_card_rules + all_three_card_rules

    return all_rules


def getRulesForThreeCards(cards):
    """
    Takes three cards and gets the rules that accept three cards,
    for the given ordering

    Parameters
    ----------
    cards: list
        List of three cards

    Returns
    -------
    three_rules: list
        a list of strings that describe the three-card rules that accept the
        given three cards
    """
    assert len(cards) == 3, 'Three cards should be provided'

    cur = cards[-1]
    prev = cards[-2]
    prev2 = cards[-3]

    prev_curr = getRulesForTwoCards([prev, cur])
    prev2_prev = getRulesForTwoCards(
        ([prev2, prev]),
        cur_name="previous", prev_name="previous2")

    value_comp_rules = ["less(value(", "greater(value(", "equal(value("]
    suit_comp_rules = ["less(suit(", "greater(suit(", "equal(suit("]

    three_rules = []
    for r_prev in prev2_prev:
        prev_start = r_prev[:r_prev.index("previous2")]
        for r_cur in prev_curr:
            use = False
            cur_start = r_cur[:r_cur.index("previous")]
            # if the first parts of the rule match, they are about
            # the same thing
            if prev_start == cur_start:
                use = True

            # match up rules that are both comparing values
            elif prev_start in value_comp_rules \
            and cur_start in value_comp_rules:
                use = True

            # match up rules that are both comparing suites
            elif prev_start in suit_comp_rules \
            and cur_start in suit_comp_rules:
                use = True

            # match up rules that are counting the differences between values
            elif (prev_start.startswith("equal(minus1(") or
                  prev_start.startswith("equal(plus1(")) \
            and (cur_start.startswith("equal(minus1(") or
                 cur_start.startswith("equal(plus1(")):
                use = True

            # append the rule that matched
            if use:
                three_rules.append("and(" + r_prev + ", " + r_cur + ")")
    return three_rules


def getRulesForOneCard(card, cur_name="current"):
    """
    Finds all the 1-card rules for the given card

    Parameters
    ----------
    card: str
        String representation of a card
    cur_name: str
        Name of the given card

    Returns
    -------
    list_of_rules: list
        A list of strings that describe the rules that accept the given card
    """
    possible_values = {"suit": suit, "color": color, "is_royal": is_royal,
                       "even": even, "value": value}

    list_of_rules = []
    for name, func in possible_values.items():
        card_value = func(card)
        list_of_rules.append(
            "equal(" + name + "(" + cur_name + "), " + str(card_value) + ")")

    return list_of_rules


def getRulesForTwoCards(cards, cur_name="current", prev_name="previous"):
    """
    Finds all 2-card rules for a pair of cards

    Parameters
    ----------
    card: list
        List of two cards
    cur_name: str
        Name of the given card in the 'current' position
    prev_name: str
        Name of the given card in the 'previous' position

    Returns
    -------
    all_pair_rules: list
        List of strings describing the rules that accept the given pair of
        cards
    """
    assert len(cards) == 2, 'Only two cards should be provided'

    cur = cards[-1]
    prev = cards[-2]

    all_pair_rules = []
    same_funcs = {"value": value, "suit": suit,
                  "is_royal": is_royal, "even": even}
    # are the value, suit,color royalty, or parity the same?
    for func in same_funcs:
        if same_funcs[func](cur) == same_funcs[func](prev):
            # when an attribute is equal for two consecutive cards, then this
            # attribute is a rank-1 attribute and so we don't need to have
            # these rules
            continue
        else:
            all_pair_rules.append(
                "not(equal(" + func + "(" + cur_name + "), " +
                func + "(" + prev_name + ")))")

    # if value(cur) > value(prev)
    if greater(value(cur), value(prev)):
        all_pair_rules.append(
            "greater(value(" + cur_name + "), value(" + prev_name + "))")
        difference = value(cur) - value(prev)
        # add the rule that gives the specific distance between the cards
        all_pair_rules.append(
            "equal(" + ("plus1(" * difference)+"value(" + prev_name + ")" +
            (")" * difference)+", value(" + cur_name + "))")
    # if value(prev) > value(cur)
    elif greater(value(prev), value(cur)):
        all_pair_rules.append(
            "less(value(" + cur_name + "), value(" + prev_name + "))")
        difference = value(prev) - value(cur)
        # add the rule that gives the specific distance between the cards
        all_pair_rules.append(
            "equal(" + ("minus1(" * difference) + "value(" + prev_name + ")" +
            (")" * difference) + ", value(" + cur_name + "))")

    # if suit(cur) > suit(prev)
    if greater(suit(cur), suit(prev)):
        all_pair_rules.append(
            "greater(suit(" + cur_name + "), suit(" + prev_name + "))")
    # if suit(prev) > suit(cur)
    elif greater(suit(prev), suit(cur)):
        all_pair_rules.append(
            "less(suit(" + cur_name + "), suit(" + prev_name + "))")

    # Make rules for specific "this value" followed by "this value' so
    # red->black will be there with color1 != color2
    prev_rules = getRulesForOneCard(prev, cur_name=prev_name)
    cur_rules = getRulesForOneCard(cur, cur_name=cur_name)
    for rp, rc in zip(prev_rules, cur_rules):
        # again, remove the rules that are the same for two consecutive cards
        if rp.replace(prev_name, '') != rc.replace(cur_name, ''):
        all_pair_rules.append("and(" + rp + ", " + rc + ")")

    return all_pair_rules


def combineRulesWithOperator(listOfRules, operator):
    """
    Takes a list of rules and makes an overall rule that ties them together
    with the AND or the OR operator

    Parameters
    ----------
    listOfRules: list
        A list of string representation of rules
    operator: str
        Should be either AND or OR

    Returns
    -------
    total: str
        String representation of the rules combined using the given operator
    """
    assert type(listOfRules) == list
    assert all(map(lambda r: type(r) == str, listOfRules))
    assert operator.lower() in ['and', 'or']

    if len(listOfRules) == 1:
        return listOfRules[0]

    operator = operator.lower()
    total = listOfRules[0]
    for i in range(1, len(listOfRules)):
        total = operator + "("+total+", "+listOfRules[i]+")"
    return total


def combineListOfRules(ruleList):
    """
    Takes a list of rules or a list of lists of rules and makes an overall
    rule that is the disjunction (AND) of rules inside each inner list and
    conjunction (OR) of the resulting rules.

    Parameters
    ----------
    ruleList: list:
        List of string representation of rules, or list of lists of string
        representation of the rules

    Returns
    -------
    total_rule: Tree
        The resulting rule tree from combining the given rules
    """
    if type(ruleList[0]) is not list:
        # it is a one-dimensional list, so just AND everything together
        return parse(combineRulesWithOperator(
                list(map(lambda r: str(r), ruleList)), "and"))

    or_list = []
    for a_list in ruleList:
        # combine them with AND
        or_list.append(combineRulesWithOperator(
            list(map(lambda r: str(r), a_list)), "and"))
    # combine the whole thing with OR
    total_rule = combineRulesWithOperator(or_list, "or")

    return parse(total_rule)


def getRandomRule():
    """
    Creates a random rule tree

    Returns
    -------
    rule: Tree
        A random rule tree
    """
    possible_cards = ["current", "previous", "previous2"]
    possible_attrs_dict = {
        "color": ["R", "B"],
        "suit": ["D", "H", "S", "C"],
        "is_royal": ["True", "False"],
        "even": ["True", "False"],
        "value": ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                  "J", "Q", "K"]}

    two_items_rules_dict = {
        "equal": ["value", "suit", "color", "is_royal", "even"],
        "greater": ["value"],
        "less": ["value"]}
    # not using plus1 or minus1 because they are a bit more complicated

    operators = ["and", "or"]

    def random_one_card_rule(card_name):
        attr, val = random.choice(list(possible_attrs_dict.items()))
        return "equal(" + attr + "(" + card_name + "), " + \
            random.choice(val) + ")"

    def random_two_card_rule(cur_name, prev_name):
        comparison = random.choice(list(two_items_rules_dict.keys()))
        val = random.choice(two_items_rules_dict[comparison])

        return comparison + "(" + val + "(" + cur_name + "), " + val + \
            "(" + prev_name + "))"

    rand = random.randint(1, 11)
    if rand <= 4:
        # return a 1-item rule of some property applied to one card
        rule = random_one_card_rule('current')

    elif rand <= 9:
        # Return a 2-item rule of some property
        rule = random_two_card_rule('current', 'previous')

    else:
        # return a conjunctive rule
        op = random.choice(operators)

        rule = op + "(" + random_two_card_rule('current', 'previous') + \
            "," + random_two_card_rule('previous', 'previous2') + ")"

    return parse(rule)
