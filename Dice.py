## Dice

import random

class FairDie(object):
    def __init__(self,sides=6):
        """Fair die with equal probability of landing on any
           particular number. First argument is number of sides."""

        self.sides = int(sides)
        self.name = "Fair Die"

    def roll(self):
        return random.randint(1,self.sides)


class LoadedDie(object):
    def __init__(self, weights, name="Loaded Die"):
        """Loaded die. First argument is weightings of each
           side. Can be array-like or dict. If array-like,
           the numbers on the die come from the index + 1,
           but if dict the numbers on the die come from the
           dictionary keys. Probabilities will be normalised
           on instantiation."""

        if not isinstance(weights, dict):
            weights = self._make_dict(weights)

        self.weights = self._normalise(weights)

        self.name = name

    def _make_dict(self, weights):
        new = {}
        for num, weight in enumerate(weights):
            new[num+1] = weight
        return new

    def _normalise(self, weights):
        total = sum(weights.values())

        new = {}
        for num, weight in weights.items():
            new[num] = weight/total
        return new

    @property
    def cumulative_weights(self):
        s = 0
        nums = []
        weights = []
        for num, weight in self.weights.items():
            s += weight
            nums.append(num)
            weights.append(s)
        return (nums, weights)

    def roll(self):
        r = random.random()
        cw = self.cumulative_weights
        num = [cw[0][i] for i in range(len(cw[0])) if cw[1][i] >= r][0]
        return num
