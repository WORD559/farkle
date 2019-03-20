## Farkle game code

import Dice

class Player(object):
    def __init__(self,name="Player",max_dice=6):
        """Initialises a player. New player has no wins, no
           losses, no cash, and no custom dice. First arg
           specifies max number of dice player can use in
           one game."""

        self.name = name
        self.max_dice = max_dice
        self.wins = 0
        self.losses = 0
        self.cash = 0
        self.custom_dice = []
        self.selected_dice = []

        ## initialise lists of dice being used in a game
        self.dice = [] # will be populated with fair dice
        self.dice_in_hand = [] # dice not being scored

        ## initialise in-game vars
        self.score = 0
        self.turn_score = 0

    def new_game(self):
        self.score = 0
        self.turn_score = 0

    def end_game(self):
        self.score += self.turn_score

    def start_turn(self, hot_dice=False):
        """Populate self.dice with the dice that will be
           used, and fill the hand with these dice. This
           should be executed every time the player
           starts a new turn!"""
        self.dice = self.selected_dice[:self.max_dice]
        while len(self.dice) < self.max_dice:
            self.dice.append(Dice.FairDie())
        self.dice_in_hand = self.dice[:]
        if not hot_dice:
            self.turn_score = 0

    def throw_dice(self, debug=False):
        """Returns False if "bust", otherwise returns a
           dict of the rolled values for the player to
           select from. Dict has structure:
               key: Dice object
               val: value rolled"""

        rolls = dict([(d, d.roll()) for d in self.dice_in_hand])
        if debug:
            print(rolls)
            
        if turn_playable(list(rolls.values())):
            return rolls
        self.turn_score = 0
        return False

    def score_and_remove(self, rolls, chosen):
        chosen_nums = [rolls[d] for d in chosen]
        score = calculate_score(chosen_nums)
        if score == 0:
            raise ValueError("Chosen values give score 0, not allowed")
        self.turn_score += score
        for d in chosen:
            self.dice_in_hand.remove(d)
        if len(self.dice_in_hand) == 0:
            self.start_turn()

def turn_playable(rolled_nums):
    if 5 in rolled_nums or 1 in rolled_nums:
        return True
    for i in rolled_nums:
        if rolled_nums.count(i) >= 3:
            return True
    return False

def calculate_score(chosen_nums):
    """Calculates the player's score based on the
       rolled numbers that they chose. Score is
       calculated based on the following:

       1 = 100 points
       5 = 50 points

       Triples are worth 100 times the number, so
       triple 3 = 300 points, triple 1 = 1000 points,
       etc. This is multiplied by the number of same
       number dice minus 2. So triple 1 = 1000, but
       four 1s = 2000 (1000*(4-2)), and five 1s is
       3000 (1000*(5-2)).

       1 through 5 is worth 500
       2 through 6 is worth 750
       1 through 6 is worth 1500

       Any lone dice that don't meet any of the scoring
       criteria nullify the whole score."""

    chosen_nums = chosen_nums[:]
    null = False
    score = 0

    # identify straights first
    full_straight = True
    for i in range(1,7):
        if i not in chosen_nums:
            full_straight = False
            break
    if full_straight:
        score += 1500
        for i in range(1,7):
            chosen_nums.remove(i)

    high_straight = True
    for i in range(2,7):
        if i not in chosen_nums:
            high_straight = False
            break
    if high_straight:
        score += 750
        for i in range(2,7):
            chosen_nums.remove(i)

    low_straight = True
    for i in range(1,6):
        if i not in chosen_nums:
            low_straight = False
            break
    if low_straight:
        score += 500
        for i in range(1,6):
            chosen_nums.remove(i)

    # now fives and ones (including triples)
    fives = chosen_nums.count(5)
    if fives < 3:
        score += 50*fives
    else:
        score += 500*(fives-2)

    ones = chosen_nums.count(1)
    if ones < 3:
        score += 100*ones
    else:
        score += 1000*(ones-2)

    # now others
    for i in range(1,7):
        if i == 1 or i == 5:
            continue
        count = chosen_nums.count(i)
        if count >= 3:
            score += (100*i)*(count-2)
        elif count != 0:
            null = True
            break

    if null:
        return 0
    return score
        
