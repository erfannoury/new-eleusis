'''
This file tests the runnning of the game
'''
from Game import *

def main():
    print("Hello! Welcome to the main for new_eleusis.py")
    #default, do not allow royal cards
    rule = "iff(is_royal(current), False)"
    #rule = input("Please input in a rule:")
    theGame = Game()
    print("The rule is",rule)
    theGame.setRule(rule)
    endRule = theGame.scientist()
    print("The final rule was ",endRule)



main()