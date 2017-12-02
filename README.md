# The Game of New Eleusis
Final project for the CMSC 671 class - New Eleusis game.

## Card representation

| Suit/Number | Character Representation |
|-------------|--------------------------|
| Spades ♠️    | S                        |
| Heart ♥️     | H                        |
| Diamond ♦️   | D                        |
| Club ♣️      | C                        |
| Ace         | A                        |
| 2           | 2                        |
| 3           | 3                        |
| 4           | 4                        |
| 5           | 5                        |
| 6           | 6                        |
| 7           | 7                        |
| 8           | 8                        |
| 9           | 9                        |
| 10          | 10                       |
| Jack        | J                        |
| Queen       | Q                        |
| King        | K                        |


## Phase I Implementation

For our implementation, we created a Game class that stores the true rule for that game, the game board, and the current set of hypotheses.
You can access the code for the first phase from the Releases section ([Phase I](https://github.com/erfannoury/new-eleusis/releases/tag/v0.1)).

You can run the code for Phase I as follows:

```
$ python main.py
```

### For Phase I, the strategy is as follows:
1. The scientist takes two valid cards from the user, and finds all possible rules that describe those cards. These rules are stored as a two dimensional list of strings, where items in the inner lists are “and’d” together, and lists of items are “or’d” together logically.
2. The scientist then plays by alternating between a proposed accepted card and a proposed rejected card.
3.
    - If the card is accepted, then the function applyAcceptedCard checks for any lists of rules that all accept this card. If there is one, then it is done. Otherwise, it searches in each list of rules for inner rules that would accept the card. The list is then reduced to just the rules that would accept the cards. If there is no list of “and’d” rules that would accept it, a new list of rules is created from the properties of the card and the sequence that led up to it.
    - If the card is rejected, then the function applyRejectedCard checks for any lists of rules that would accept the card. If there are none, then it is done. Otherwise, it searches through the list of accepted sequences for a particular rule and try to find some properties of the rejected sequence that the accepted sequences did not have. These properties are added to this list with a “not”.
4. The scientist runs this algorithm one hundred times and returns the rule it found at the end of this.
5. The proposed rule is scored against the actual rule by comparing lists of all accepted sequences. The two rules are equal if they accept the same sequences.


## Phase II Implementation
The master branch contains the latest code implemented for Phase II. You can start the game as follows:

```
$ python main.py
```
