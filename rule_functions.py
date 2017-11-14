'''
This file contains helper functions for rules
'''
import random
from new_eleusis import *
from itertools import combinations

ALL_CARDS = []
for deck in ["D","H","S","C"]:
    for num in ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]:
        ALL_CARDS.append(num+deck)

def getAllValidSequences(rule):
    '''
    loops over all possible lists of three cards and returns the list
    :param rule: the rule that we want to find valid cards for
    :return:
    '''
    # print("Evaluating",rule)
    goodList = []
    for card1, card2, card3 in combinations(ALL_CARDS, r=3):
        if rule.evaluate([card1, card2, card3]):
            goodList.append(card1 + card2 + card3)
    return goodList


def getRulesForSequence(cards):
    '''
    Takes in a sequence and returns all possible rules for that ordering
    :param cards: a list of three cards
    :return: returns a list of all possible rules the cards have in common (as trees)
    '''

    #for each of the three cards, get the one-card rules
    curSet = set(getRulesForOneCard(cards[-1]))
    prevSet = set(getRulesForOneCard(cards[-2]))
    prev2Set = set(getRulesForOneCard(cards[0]))

    #select the one-card rules that overlap for all three
    all_one_card_rules = list((curSet & prevSet) & prev2Set)

    #for each pair of (previous2,previous) and (previous,current), get the 2-card rules
    prev_curr = getRulesForTwoCards([cards[1],cards[2]])
    prev2_prev = set(getRulesForTwoCards(([cards[0],cards[1]])))

    #If there is overlap, add two-card rules based on current and previous
    all_two_card_rules = list(set(prev_curr) & prev2_prev)

    #Get the three-card rules
    all_three_card_rules = getRulesForThreeCards(cards)

    all_rules =  all_one_card_rules + all_two_card_rules + all_three_card_rules

    #turn the rules into trees
    all_trees = []
    for rule in all_rules:
        all_trees.append(parse(rule))
    return all_trees

def getRulesForThreeCards(cards):
    '''
    takes three cards and gets the rules for their ordering
    :param cards:
    :return: a list of three-card rules that describe all the cards (as strings)
    '''
    prev_curr = getRulesForTwoCards([cards[1], cards[2]])
    prev2_prev = getRulesForTwoCards(([cards[0], cards[1]]), "previous2", "previous")
    three_rules = []

    for rule1 in prev2_prev:
        start1 = rule1[:rule1.index("previous2")]
        for rule2 in prev_curr:
            use = False
            start2 = rule2[:rule2.index("previous")]
            #if the first parts of the rule match, they are about the same thing
            if start1 == start2:
                use = True
            #match up rules that are both comparing values
            elif start1 in ["less(value(","greater(value(","equal(value("] and start2 in ["less(value(","greater(value(","equal(value("]:
                use = True
            #match up rules that are both comparing suites
            elif start1 in ["less(suit(","greater(suit(","equal(suit("] and start2 in ["less(suit(","greater(suit(","equal(suit("]:
                use = True
            #match up rules that are counting the differences between values
            elif (start1.startswith("equal(minus1(") or start1.startswith("equal(plus1(")) and \
                    (start2.startswith("equal(minus1(") or start2.startswith("equal(plus1(")):
                use = True
            #append the rule that matched
            if use:
                three_rules.append("and(" + rule1 + ", " + rule2 + ")")
    return three_rules


def getRulesForOneCard(card,type = "current"):
    '''
    finds all the 1-card rules
    :param card: one card
    :return: a list of one-card rules that describes the card (as strings)
    '''

    possible_values = {"suit":suit, "color":color, "is_royal":is_royal, "even":even,
                       "value":value}
    list_of_rules = []
    for func in possible_values.keys():
        card_value = possible_values[func](card)
        list_of_rules.append("equal("+func+"("+type+"), "+str(card_value)+")")
    return list_of_rules



def getRulesForTwoCards(cards,type1 = "previous",type2 = "current"):
    '''
    finds all 2-card rules for a pair of cards
    :param card: a list of two cards
    :return: a list of 2-card rules that describe the pair (as strings)
    '''

    all_pair_rules = []
    same_funcs = {"value":value,"suit":suit,"is_royal":is_royal,"even":even}
    #are the value, suit,color royalty, or parity the same?
    for func in same_funcs:
        if same_funcs[func](cards[0]) == same_funcs[func](cards[1]):
            all_pair_rules.append("equal("+func+"("+type1+"), "+func+"("+type2+"))")

    #Is one card greater than the other in value:
    if greater(value(cards[0]),value(cards[1])):
        all_pair_rules.append("greater(value("+type1+"), value("+type2+"))")
        difference = value(cards[0])-value(cards[1])
        #add the rule that gives the specific distance between the cards
        all_pair_rules.append("equal("+("plus1("*difference)+"value(" + type1 + ")"+
                              (")"*difference)+", value(" + type2 + "))")
    elif greater(value(cards[1]),value(cards[0])):
        all_pair_rules.append("less(value(" + type1 + "), value(" + type2 + "))")
        difference = value(cards[1]) - value(cards[0])
        # add the rule that gives the specific distance between the cards
        all_pair_rules.append("equal(" + ("minus1(" * difference) + "value(" + type1 + ")" +
                              (")" * difference) + ", value(" + type2 + "))")

    #is one card greater than the other in suit
    if greater(suit(cards[0]),suit(cards[1])):
        all_pair_rules.append("greater(suit("+type1+"), suit("+type2+"))")
    elif greater(suit(cards[1]),suit(cards[0])):
        all_pair_rules.append("less(suit(" + type1 + "), suit(" + type2 + "))")


    #Make rules for specific "this value" followed by "this value' so red->black will be there with color1 != color2
    prev_rules = getRulesForOneCard(cards[0],type1)
    cur_rules = getRulesForOneCard(cards[1],type2)
    for i in range(len(prev_rules)):
        all_pair_rules.append("and("+prev_rules[i]+", "+cur_rules[i]+")")

    return all_pair_rules

def combineRulesWithOperator(listOfRules,operator):
    '''
    takes a list of rules and makes an overall rule that ties them together with and or or
    :param listOfRules: a list of trees [rule1, rule2]
    :param operator: either "and" or "or"
    :return:
    '''
    if len(listOfRules) == 1:
        return listOfRules[0]

    total = listOfRules[0]
    for i in range(1,len(listOfRules)):
        total = operator + "("+total+", "+listOfRules[i]+")"
    return total

def combineListOfRules(ruleList):
    '''
    takes a 2d list of rules and makes an overall rule that ands any inner lists and ors any outer lists
    :param ruleList: a one-dimensional or two-dimensional list of rules
    :return: the resulting tree
    '''
    if type(ruleList[0]) is not list:
        #it is a one-dimensional list, so just and everything together
        for i in range(len(ruleList)):
            ruleList[i] = str(ruleList[i])
        return parse(combineRulesWithOperator(ruleList,"and"))

    or_list = []
    for a_list in ruleList:
        #change everything to string form first
        for i in range(len(a_list)):
            a_list[i] = str(a_list[i])
        #combine them with and
        or_list.append(combineRulesWithOperator(a_list,"and"))
    #combine the whole thing with or
    total_rule = combineRulesWithOperator(or_list,"or")
    return parse(total_rule)


def getRandomRule():
    '''
    Creates a random rule
    (For testing purposes)
    :return:
    '''
    theRule = getMiniRandomRule()  # "iff("+self.getMiniRandomRule()+", True, False)"
    print(theRule)
    return parse(theRule)


def getMiniRandomRule(rand=0):
    '''

    :param rand: this tells the function which type of rule to make. This is only
    set when a larger rule wants to create specific smaller rules
    :return:
    '''
    possible_cards = ["current", "previous", "previous2"]
    possible_values = ["color", "suit", "is_royal", "even", 'odd', "value"]
    possible_value_dict = {"color": ["R", "B"],
                           "suit": ["D", "H", "S", "C"],
                           "is_royal": ["True", "False"],
                           "even": ["True", "False"],
                           "odd": ["True", "False"],
                           "value": ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]}
    two_items_rules = ["equal", "greater", "less"]
    two_items_rules_dict = {"equal": ["value", "suit", "color", "is_royal", "even"],
                            "greater": ["value"],
                            "less": ["value"]}
    #not using plus1 or minus1 because they are a bit more complicated

    conjunctions = ["and", "or"]
    # generate a random number between 1 and 10
    if rand == 0:
        rand = random.randint(1, 11)
    if rand <= 4:
        # return a 1-item rule of some property applied to one card
        value = random.choice(possible_values)
        card = random.choice(possible_cards)
        return "equal(" + value + "(" + card + "), " + random.choice(possible_value_dict[value]) + ")"
    elif rand <= 9:
        # Return a 2-item rule of some property
        comparison = random.choice(two_items_rules)
        value = random.choice(two_items_rules_dict[comparison])
        card1 = "current"
        card2 = random.choice(["previous", "previous2"])

        return comparison + "(" + value + "(" + card1 + "), " + value + "(" + card2 + "))"
    else:
        # return a conjunctive rule
        conjunction = random.choice(conjunctions)

        return conjunction + "(" + getMiniRandomRule(6) + "," + getMiniRandomRule(6) + ")"