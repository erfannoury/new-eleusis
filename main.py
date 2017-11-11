'''
This file tests the runnning of the game
'''
from Game import *

def main():
    print("Hello! Welcome to the main for new_eleusis.py")
    #default, red must follow black

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