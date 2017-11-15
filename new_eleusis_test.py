import unittest
from new_eleusis import *


class TestNewEleusis(unittest.TestCase):

    def test_is_suit(self):
        for c in "CDHS":
            self.assertTrue(is_suit(c))
        self.assertFalse(is_suit("B"))

    def test_is_color(self):
        for c in "BR":
            self.assertTrue(is_color(c))
        self.assertFalse(is_color("H"))

    def test_is_value(self):
        for c in "A234JQK":
            self.assertTrue(is_value(c))
        self.assertFalse(is_value("D"))
        self.assertFalse(is_value("KD"))

    def test_is_card(self):
        for c in ["2C", "10D", "JH", "AS"]:
            self.assertTrue(is_card(c))
        self.assertFalse(is_card("H"))
        self.assertFalse(is_card("10"))

    def test_value_to_number(self):
        self.assertEqual(1, value_to_number("A"))
        self.assertEqual(5, value_to_number("5"))
        self.assertEqual(10, value_to_number("10"))
        self.assertEqual(11, value_to_number("J"))
        self.assertEqual(12, value_to_number("Q"))
        self.assertEqual(13, value_to_number("K"))

    def test_number_to_value(self):
        self.assertEqual("A", number_to_value(1))
        self.assertEqual("5", number_to_value(5))
        self.assertEqual("10", number_to_value(10))
        self.assertEqual("J", number_to_value(11))
        self.assertEqual("Q", number_to_value(12))
        self.assertEqual("K", number_to_value(13))

    def test_suit(self):
        self.assertEqual('S', suit("AS"))
        self.assertEqual('D', suit("10D"))

    def test_color(self):
        self.assertEqual('B', color("2C"))
        self.assertEqual('R', color("6D"))
        self.assertEqual('R', color("10H"))
        self.assertEqual('B', color("AS"))

    def test_value(self):
        self.assertEqual(1, value("AS"))
        self.assertEqual(2, value("2C"))
        self.assertEqual(10, value("10D"))
        self.assertEqual(11, value("JH"))
        self.assertEqual(12, value("QD"))
        self.assertEqual(13, value("KC"))

    def test_suit(self):
        self.assertEqual('C', suit("2C"))
        self.assertEqual('D', suit("6D"))
        self.assertEqual('H', suit("10H"))
        self.assertEqual('S', suit("AS"))

    def test_is_royal(self):
        for c in ["QC", "JD", "KH"]:
            self.assertTrue(is_royal(c))
        self.assertFalse(is_royal("AS"))
        self.assertFalse(is_royal("10C"))

    def test_equal(self):
        self.assertEqual("R", "R")
        self.assertEqual(13, value("KD"))

    def test_less(self):
        self.assertTrue(less("3C", "10C"))
        self.assertTrue(less("10C", "2D"))
        self.assertFalse(less("3C", "AC"))

        self.assertTrue(less("C", "D"))
        self.assertFalse(less("C", "C"))

        self.assertTrue(less("B", "R"))
        self.assertFalse(less("R", "B"))

        self.assertTrue(less("A", "2"))
        self.assertFalse(less("2", "A"))
        self.assertTrue(less("A", "J"))
        self.assertTrue(less("J", "Q"))
        self.assertTrue(less("Q", "K"))

    def test_plus1(self):
        self.assertEqual("2", plus1("A"))
        self.assertEqual("J", plus1("10"))
        self.assertEqual("S", plus1("H"))
        self.assertEqual("KC", plus1("QC"))
        self.assertEqual("B", plus1("R"))
        self.assertEqual("R", plus1("B"))

    def test_minus1(self):
        self.assertEqual("A", minus1("2"))
        self.assertEqual("10", minus1("J"))
        self.assertEqual("H", minus1("S"))
        self.assertEqual("QC", minus1("KC"))
        self.assertEqual("B", minus1("R"))
        self.assertEqual("R", minus1("B"))

    def test_even(self):
        self.assertFalse(even("AS"))
        self.assertTrue(even("2D"))
        self.assertFalse(even("JC"))
        self.assertTrue(even("QH"))
        self.assertFalse(even("KD"))

    def test_odd(self):
        self.assertTrue(odd("AS"))
        self.assertFalse(odd("2D"))
        self.assertTrue(odd("JC"))
        self.assertFalse(odd("QH"))
        self.assertTrue(odd("KD"))

    def eval_tree(self, root, left=None, right=None,
                  cards=("3H", "5D", "AS")):
        """Shortcut for creating and evaluating a Tree"""
        return Tree(root, left, right).evaluate(cards)

    def eval_if_tree(self, root, left=None, right=None, test=True,
                     cards=("3H", "5D", "AS")):
        """Shortcut for creating and evaluating a Tree"""
        return Tree(root, left, right, test).evaluate(cards)

# def test_simple_evaluate(self):
#        self.assertEqual("AS", self.eval_tree("current"))
#        self.assertEqual("5D", self.eval_tree("previous"))
#        self.assertEqual("3H", self.eval_tree("previous2"))
#        self.assertEqual("9C", self.eval_tree("9C"))
#        self.assertEqual(True, self.eval_tree(True))
#        self.assertEqual(False, self.eval_tree(False))

    def test_unary_evaluate(self):
        self.assertEqual("S", self.eval_tree(suit, "AS"))
        self.assertEqual("B", self.eval_tree(color, "AS"))
        self.assertEqual(1, self.eval_tree(value, "AS"))
        self.assertEqual(12, self.eval_tree(value, "QS"))
        self.assertTrue(self.eval_tree(is_royal, "JD"))
        self.assertFalse(self.eval_tree(is_royal, "3D"))
        self.assertFalse(self.eval_tree(is_royal, "AD"))
        self.assertEqual("10D", self.eval_tree(minus1, "JD"))
        self.assertEqual("QD", self.eval_tree(plus1, "JD"))
        self.assertTrue(self.eval_tree(even, "QH"))
        self.assertFalse(self.eval_tree(even, "3H"))
        self.assertTrue(self.eval_tree(odd, "AC"))
        self.assertFalse(self.eval_tree(odd, "8C"))

    def test_card_evaluate(self):
        self.assertEqual('R', self.eval_tree(color, "7H"))
        self.assertEqual('H', self.eval_tree(suit, "7H"))
        self.assertEqual(7, self.eval_tree(value, "7H"))
        self.assertFalse(self.eval_tree(is_royal, "7H"))
        self.assertTrue(self.eval_tree(is_royal, "JH"))
        self.assertEqual('6H', self.eval_tree(minus1, "7H"))
        self.assertEqual('8H', self.eval_tree(plus1, "7H"))
        self.assertEqual('JH', self.eval_tree(plus1, "10H"))
        self.assertFalse(self.eval_tree(even, "7H"))
        self.assertTrue(self.eval_tree(odd, "7H"))

    def test_binary_evaluate(self):
        self.assertTrue(self.eval_tree(equal, "AC", "AC"))
        self.assertFalse(self.eval_tree(equal, "8C", "8H"))

        self.assertTrue(self.eval_tree(less, "AD", "KD"))
        self.assertFalse(self.eval_tree(less, "8C", "8C"))
        self.assertFalse(self.eval_tree(less, "2D", "KC"))

        self.assertTrue(self.eval_tree(greater, "AH", "KD"))
        self.assertFalse(self.eval_tree(greater, "8C", "8C"))
        self.assertFalse(self.eval_tree(greater, "3C", "KC"))

    def test_logic_evaluate(self):
        self.assertTrue(self.eval_tree(andf, True, True))
        self.assertFalse(self.eval_tree(andf, True, False))

        self.assertTrue(self.eval_tree(orf, True, True))
        self.assertTrue(self.eval_tree(orf, True, False))
        self.assertTrue(self.eval_tree(orf, False, True))
        self.assertFalse(self.eval_tree(orf, False, False))

        self.assertTrue(self.eval_tree(notf, False))
        self.assertFalse(self.eval_tree(notf, True))

        cards = ("3D", "7H", "AC")
        self.assertEqual("5H", self.eval_if_tree(iff, True, "5H", "AS"), cards)
        self.assertEqual("AS", self.eval_if_tree(
            iff, False, "5H", "AS"), cards)

# def test_tree(self):
# self.assertEqual("""Tree(iff(Tree(equal(Tree(suit('previous')),
# Tree(suit('previous2')))),
# Tree(is_royal('current')),
# Tree(notf(Tree(is_royal('current'))))))""",
# tree("""iff(equal(suit(previous), suit(previous2)),
# is_royal(current), notf(is_royal(current)))"""))

    def test_evaluate_rules(self):
        cards1 = ("3D", "7D", "AH")
        cards2 = ("3D", "7S", "AC")
        cards3 = ("4H", "5H", "KH")

        # Red must follow black
        self.assertTrue(parse(
            """or(equal(color(previous), R),
            equal(color(current), R))""").evaluate(cards1))
        self.assertTrue(Tree(
            orf,
            Tree(equal, Tree(color, "previous"), "R"),
            Tree(equal, Tree(color, "current"), "R")).evaluate(cards1))
        self.assertFalse(Tree(
            orf,
            Tree(equal, Tree(color, "previous"), "R"),
            Tree(equal, Tree(color, "current"), "R")).evaluate(cards2))
        # Red must follow black, using parser
        p = parse(
            "iff(equal(color(previous), B), equal(color(current), R), True)")
        self.assertTrue(p.evaluate(cards1))
        self.assertFalse(p.evaluate(cards2))
        self.assertTrue(p.evaluate(cards3))

        # Must play royalty after two cards of same suit, and only then
        p = parse("""iff(equal(suit(previous), suit(previous2)),
                     is_royal(current),
                     not(is_royal(current)))""")
        self.assertFalse(p.evaluate(cards1))
        self.assertTrue(p.evaluate(cards2))
        self.assertTrue(p.evaluate(cards3))
        self.assertFalse(p.evaluate(("5H", "5D", "QC")))

        # Cannot have three in a row of either colors or values
        p = parse("""and(
                        not(and(equal(color(previous), color(previous2)),
                                equal(color(previous), color(current))) ),
                        not(and(equal(value(previous), value(previous2)),
                                equal(value(previous), value(current))) ) )""")
        self.assertFalse(p.evaluate(cards1))
        self.assertTrue(p.evaluate(cards2))
        self.assertFalse(p.evaluate(cards3))
        self.assertTrue(p.evaluate(("5H", "5D", "QC")))
        self.assertFalse(p.evaluate(("5H", "5D", "5C")))

    def test_scan(self):
        self.assertEqual(
            ['equal', '(', 'color', '(', 'previous', ')', 'R', ')'],
            list(scan("equal(color(previous), R)")))
        self.assertEqual(
            ['iff', '(', 'equal', '(', 'previous', 'B', ')', 'equal', '(',
             'current', '(', 'R', ')', ')', 'False', ')'],
            list(scan("iff(equal(previous, B), equal(current(R)), False)")))

    def test_parse(self):
        self.assertEqual(str(Tree(equal, Tree(color, 'previous'), 'R')),
                         str(parse("equal(color(previous), R)")))
        self.assertEqual(repr(Tree(equal, Tree(color, 'previous'), 'R')),
                         repr(parse("equal(color(previous), R)")))


if __name__ == '__main__':
    unittest.main()
