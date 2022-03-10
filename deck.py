from numpy.random import shuffle

vals = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
val_dict = dict(
    {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
        "A": 11,
    }
)


class Deck:
    def __init__(self):
        self.deck = [v for v in vals] * 4 * 4

    def deal(self):
        deal = self.deck.pop()
        return deal

    def shuffle(self):
        shuffle(self.deck)


class Hand:
    def __init__(self):
        self.hand_up = []
        self.hand_down = []

    def __str__(self):
        hand = ""
        for card in self.hand_up:
            hand += f"{card} "
        return hand[:-1]

    def __iter__(self):
        self.n = 0
        self.l = len(self.hand_up)
        return self

    def __next__(self):
        if self.n < self.l:
            cardval = val_dict[(self.hand_up[self.n])]
            self.n += 1
            return cardval
        else:
            raise StopIteration
