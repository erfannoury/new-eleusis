'''
This file tests the runnning of the game
'''
from Game import *

def main():
    print("Hello! Welcome to the main for new_eleusis.py")
    #default, red must follow black

    cards = ["5S","AH","JH"]

    print("The three cards are:",cards)
    rules = getRulesForSequence(cards)
    print("Their properties and'd together are:")
    print(combineListOfRules(rules))

    cards2 = ["4H", "3S", "QD"]
    print("another set of cards are",cards2)
    rules2 = getRulesForSequence(cards2)
    print("Their properties and'd together are:")
    print(combineListOfRules(rules2))

    print("If we combine both lists of rules we get:")
    print(combineListOfRules([rules,rules2]))


    #The values need to be increasing
    #rule = "if(greater(value(previous), value(current)), True, False)"

    rule = "equal(color(current), R)"
    #rule = input("Please input in a rule:")
    theGame = Game()
    print("The rule is",rule)
    theGame.setRule(rule)
    endRule = theGame.scientist()
    print("The final rule was ",endRule)



main()