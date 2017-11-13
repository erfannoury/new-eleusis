'''
Contains the Game class
'''
from new_eleusis import *
import random
from itertools import product
'''
Game has these private variables:
rule - the rule from the user
played - the list of tuples with accepted and rejected cards ex: [( "5H",["QS"]),( "6C",[])]
rule_set - 

'''
ALL_CARDS = []
for suite in ["D","H","S","C"]:
    for value in ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]:
        ALL_CARDS.append(value+suite)



class Game:
    def __init__(self, board_state = None, hypothesis_set = None):
        '''
        The constructor for the Game class
        :param board_state: the set of tuples representing the cards played
         = [(a1, [r1,r2]), .... etc.]
        :param hypothesis_set: A 2D list of mini-rules. The inner list gets and'd together and
        the result of that gets or'd together (the random implementation does not support this currently)
        '''
        #Note the true rule gets defined later
        self.board_state = board_state
        self.hypothesis_set = hypothesis_set

        #If they are not initialized, make them empty lists
        if board_state is None:
            self.board_state = []
            self.hypothesis_set = []
        if hypothesis_set is None:
            self.hypothesis_set = []


    def rule(self):
        '''
        This function returns the game rule to the user
        :return:
        '''
        return self.true_rule

    def setRule(self, rule_expr):
        '''
        This function sets the rule for a game
        :param rule_expr: takes in the string rule from the user
        :return:
        '''
        try:
            rule_tree = parse(rule_expr)
            self.true_rule = rule_tree
            self.true_valid = self.getAllValidSequences(rule_tree)
        except:
            raise ValueError("Invalid Rule")

    def boardState(self):
        '''
        This function returns the list of cards played so far
        :return:
        '''
        return self.board_state

    def chooseCard(self):
        '''
        This function chooses which card to play next
        :return:
        '''
        #return random card for now
        return random.choice(ALL_CARDS)

    def applyAcceptedCard(self,card):
        '''
        This function adapts the rules for when a card is accepted
        (if necessary)
        :param card: the card that was accepted
        :return:
        '''
        #Note: Currently, this does nothing
        pass

    def applyRejectedCard(self,card):
        '''
        This function adapts the rules for when a card is rejected
        (if necessary)
        :param card: the card that was rejected
        :return:
        '''
        #Note: Currently, this does nothing
        pass

    def simplifyRules(self):
        '''
        This function gets rid of any redundant rules
        :return:
        '''
        pass


    def scientist(self):
        '''
        The function that runs the game. It plays 20 cards and tries to
        guess the rule
        :return:
        '''
        cards = self.getValidCards()
        print("got valid cards:",cards)
        for card in cards:
            self.board_state.append((card,[]))
            self.applyAcceptedCard(card)
        self.simplifyRules()

        #####CHANGE LATER####
        self.hypothesis_set = [self.getRandomRule()]
        print("The current guess is",self.hypothesis_set[0])
        ####################

        for turn in range(20):
            print("Turn:",turn)
            chosen = self.chooseCard()
            print("Playing",chosen,"card")
            if self.play(chosen):
                print(chosen,"was legal")
                self.applyAcceptedCard(chosen)
            else:
                print(chosen,"was illegal")
                self.applyRejectedCard(chosen)
            self.simplifyRules()
            print("Current Score is", self.score())
            print(self.boardState(),"\n")

        return self.findBestRule()



    def score(self):
        '''
        This function returns a score for this move in the game
        :return:
        '''
        score = 0
        cardsPlayed = 0
        for play in self.board_state:
            #look at legal plays
            cardsPlayed +=1
            if cardsPlayed > 20:
                score += 1
            #look at illegal plays
            for card in play[1]:
                cardsPlayed += 1
                if cardsPlayed > 20:
                    score += 2

        guessedRule = self.findBestRule()
        validReal = set(self.true_valid)
        validGuess = set(self.getAllValidSequences(guessedRule))

        #If the two sets of valid sequences are the same, the rules are the same
        if len(validGuess - validReal) > 0 or len(validReal - validGuess) > 0:
            score += 15
        return score

    def play(self,card):
        '''
        plays the card and returns whether or not it was valid.
        Also adds it to the board state
        :param card: the card that the player plays
        :return:
        '''
        previous = self.board_state[-1][0]
        previous2 = self.board_state[-2][0]
        valid = self.true_rule.evaluate([previous2,previous,card])
        if valid:
            self.board_state.append((card,[]))
        else:
            self.board_state[-1][1].append(card)
        return valid

    def findBestRule(self):
        '''
        Should return the most likely rule
        :return:
        '''
        #NOTE: right now just returns the whole thing
        return self.hypothesis_set[0]

    def findDifferences(self,cardList1,cardList2):
        '''
        This function finds what is different about a card from others
        NOTE: this function may be unnecessary for the 1st strategy
        :param cardList1:
        :param cardList2:
        :return:
        '''
        pass


    def getValidCards(self):
        '''
        Gets a card or set of cards that is valid with the game rule
        (only called for the first turn)
        :return:
        '''
        #Keeps getting sets of three random cards until we have three that have worked as "current"
        #This is because for a 1-card rule, the first two cards don't matter
        shuffleList = ALL_CARDS
        random.shuffle(shuffleList)
        for card1, card2, card3 in product(shuffleList, repeat=3):
            if card3 == card2 or card3 == card1 or card1 == card2:
                continue
            if self.true_rule.evaluate([card1,card2,card3]):
                for card4 in shuffleList:
                    if card4 == card3 or card4 == card2:
                        continue
                    if self.true_rule.evaluate([card2, card3, card4]):
                        #returns two cards that have both been "current"
                        return [card3, card4]



    def getAllValidSequences(self, rule):
        '''
        loops over all possible lists of three cards and returns the list
        :param rule: the rule that we want to find valid cards for
        :return:
        '''
        #print("Evaluating",rule)
        goodList = []
        for card1, card2, card3 in product(ALL_CARDS, repeat=3):
            if card3 == card2 or card3 == card1 or card1 == card2:
                continue
            if rule.evaluate([card1, card2, card3]):
                goodList.append(card1+card2+card3)
        return goodList

    def getRandomRule(self):
        '''
        Creates a random rule
        (For testing purposes)
        :return:
        '''
        theRule = self.getMiniRandomRule()#"iff("+self.getMiniRandomRule()+", True, False)"
        print(theRule)
        return parse(theRule)


    def getMiniRandomRule(self,rand = 0):
        '''

        :param rand: this tells the function which type of rule to make. This is only
        set when a larger rule wants to create specific smaller rules
        :return:
        '''
        possible_cards = ["current", "previous", "previous2"]
        possible_values = ["color","suit","is_royal","even",'odd',"value"]
        possible_value_dict = {"color": ["R", "B"],
                               "suit": ["D", "H", "S", "C"],
                               "is_royal": ["True", "False"],
                               "even": ["True", "False"],
                               "odd": ["True", "False"],
                               "value": ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]}
        two_items_rules = ["equal","greater","less","plus1","minus1"]
        two_items_rules_dict = {"equal": ["value", "suit", "color", "is_royal", "even"],
                           "greater": ["value"],
                           "less": ["value"]}
                            #TOOK out these two as they were constantly throwing errors
                           #"plus1": ["value"],
                           #"minus1": ["value"]}

        conjunctions = ["and", "or"]
        # generate a random number between 1 and 10
        if rand == 0:
            rand = random.randint(1, 11)
        if rand <= 4:
            #return a 1-item rule of some property applied to one card
            value = random.choice(possible_values)
            card = random.choice(possible_cards)
            return "equal("+value + "(" + card + "), " + random.choice(possible_value_dict[value]) + ")"
        elif rand <= 9:
            #Return a 2-item rule of some property
            comparison = random.choice(two_items_rules)
            value = random.choice(two_items_rules_dict[comparison])
            card1 = "current"
            card2 = random.choice(["previous","previous2"])

            return comparison+"("+value+"("+card1+"), "+value+"("+card2+"))"
        else:
            #return a conjunctive rule
            conjunction = random.choice(conjunctions)

            return conjunction + "("+self.getMiniRandomRule(6)+","+self.getMiniRandomRule(6)+")"

