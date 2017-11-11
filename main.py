'''
This file tests the runnning of the game
'''
from Game import *

def main():
    print("Hello! Welcome to the main for new_eleusis.py")
    #default, red must follow black
    rule = "or(equal(color(previous), R),equal(color(current), R))"
    #rule = input("Please input in a rule:")
    theGame = Game()
    print("The rule is",rule)
    theGame.setRule(rule)
    endRule = theGame.scientist()
    print("The final rule was ",endRule)



main()