"""
This file tests the runnning of the game
"""
from Game import *
import numpy

def main():
    rule_1 = [
        "equal(value(current), 5)",
        "equal(color(current), R)",
        "greater(value(current), 9)",
        "or (equal(color(current), R), and (odd(current), equal(color(current), B)))",
        "or ( and (is_royal(current), equal(suit(current), S)), and (not (is_royal(current)), equal(suit(current), H)))",
        "and (odd(current), is_royal(current))",
        "not ( and (equal(value(current), 1), equal(suit(current), H)))",
        "or (is_royal(current), equal(value(current), 3))",
        "and (even(current), equal(suit(current), D))",
        "and ( and (even(current), equal(suit(current), H)), greater(value(current), 5))"]

    rule_2 = ["not(equal(suit(current), suit(previous)))",
              "or(and(equal(color(current), R), equal(color(previous), B)), and(equal(color(current), B), equal(color(previous), R)))",
              "or(greater(value(current), value(previous)), equal(value(current), value(previous)))",
              "not(and(equal(suit(previous), H), equal(suit(current), D)))",
              "not(and(even(previous), and(not(equal(value(current), 7)), not(equal(value(current), 1)))))"]

    rule_3 = ["and(and(not(equal(suit(current), suit(previous))), not(equal(suit(previous), suit(previous2)))), not(equal(suit(current), suit(previous2))))",
              "and(and(equal(value(current), value(previous)), equal(value(previous), value(previous2))), equal(value(current), value(previous2)))",
              "not(and(and(equal(color(previous2), B), equal(color(previous), B)), equal(color(current), R)))",
              "not(and(is_royal(current), greater(value(previous2),value(current))))",
              "or(equal(value(current), plus1(value(previous2))),equal(value(current), value(previous2)))"]
    rules = rule_1 + rule_2 + rule_3


    output_test = open("testing_phase1.csv","w")
    output_test.write("Rule,Num_real,Num_guessed,Real_not_guessed,Guessed_not_real\n")
    for rule in rules:
        score = []
        num_guessed = []
        items_guessed_not_real = []
        items_real_not_guessed = []
        given_set = set(getAllValidSequences(parse(rule)))
        num_real = len(given_set)
        for i in range(3):
            theGame = Game()
            theGame.setRule(rule)
            endRule = theGame.scientist()
            print('The given rule is')
            print(theGame.rule())
            print('The guessed rule is')
            print(parse(endRule))
            guessed_set = set(getAllValidSequences(parse(endRule)))
            num_guessed.append(len(guessed_set))
            #score.append(theGame.score())
            #print('Number of sequences of cards that are in the given rule, but not in'
                  #' the guessed rule')
            items_real_not_guessed.append(len(given_set - guessed_set))
            items_guessed_not_real.append(len(guessed_set - given_set))
            print('===================================')
            #print('Number of sequences of cards that are in the guessed rule, but not'
                  #' in the given rule')
            #print(len(guessed_set - given_set), 'Error rate: {}%'.format(
                #len(guessed_set - given_set) / 52 ** 3 * 100))
        num_guessed = numpy.mean(num_guessed)
        #score = numpy.mean(score)
        items_real_not_guessed = numpy.mean(items_real_not_guessed)
        items_guessed_not_real = numpy.mean(items_guessed_not_real)
        output_test.write(rule.replace(",","")+","+str(num_real)+","+str(num_guessed)+","+
                          str(items_real_not_guessed)+","+str(items_guessed_not_real)+"\n")

if __name__ == '__main__':
    main()
