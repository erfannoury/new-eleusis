"""
This file tests the runnning of the game
"""
from Game import *


def main():
    rules = []
    rules.append("if(greater(value(previous), value(current)), True)")
    rules.append("greater(value(previous), value(current))")
    rules.append("equal(minus1(value(previous)), value(current))")
    rules.append("equal(is_royal(current), False)")
    rules.append('equal(equal(color(previous), B), equal(color(current), R))')
    rules.append("and(equal(color(current), R), even(current))")
    rules.append("""and(not(equal(suit(previous), suit(current))),equal(color
                 (previous), color(current)))""")
    rules.append("""and(equal(suit(current), suit(previous)), greater(value
                 (current), value(previous)))""")

    rule = random.choice(rules)
    theGame = Game()
    theGame.setRule(rule)
    endRule = theGame.scientist()
    given_set = set(getAllValidSequences(theGame.rule()))
    print('The given rule is')
    print(theGame.rule())
    print('The guessed rule is')
    print(parse(endRule))
    guessed_set = set(getAllValidSequences(parse(endRule)))
    print('Number of sequences of cards that are in the given rule, but not in'
          ' the guessed rule')
    print(len(given_set - guessed_set), 'Error rate: {}%'.format(
        len(given_set - guessed_set) / 52 ** 3 * 100))
    print('===================================')
    print('Number of sequences of cards that are in the guessed rule, but not'
          ' in the given rule')
    print(len(guessed_set - given_set), 'Error rate: {}%'.format(
        len(guessed_set - given_set) / 52 ** 3 * 100))


if __name__ == '__main__':
    main()
