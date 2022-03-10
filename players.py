from abc import abstractmethod
from deck import Deck, Hand, val_dict
from basic_strategy import soft_or_pair_outcome, other_outcome
from numpy.random import random

deck = Deck()  # avoid SyntaxError


class SplitError(TypeError):
    pass


def move_options(hand: Hand):
    out = "hit/stand/"
    hand_sum = sum(hand)
    if (hand_sum == 9 or hand_sum == 10 or hand_sum == 11) and len(hand.hand_up) == 2:
        out += "double down/"
    # if hand.hand_up[0] == hand.hand_up[1]:
    #     out += "split/"
    out += "basic strategy"
    return out


class Player:
    def __init__(self):
        self.hand = Hand()
        self.balance = 1000
        self.blackjack = False
        self.spl = False
        self.double = False
        self.bet = 0
        self.bet2 = 0

    @abstractmethod
    def move(self):
        pass

    @property
    def total(self):
        self.sum = sum(self.hand)
        return self.sum

    def initial_deal(self, deck: Deck):
        self.hand.hand_up.append(deck.deal())
        if type(self) == Dealer:
            self.hand.hand_down.append(deck.deal())
        else:
            self.hand.hand_up.append(deck.deal())

    def hit(self, deck: Deck):
        new_card = deck.deal()
        print(f"\nA {new_card} has been drawn!")
        self.hand.hand_up.append(new_card)
        return self.total

    def stand(self):
        return 0

    # def split(self):
    #     self.spl = True
    #     self.bet2 = self.bet
    #     self.hand2 = Hand()
    #     self.hand2.hand_up.append(self.hand.hand_up[1])
    #     self.hand.hand_up.pop()

    def double_down(self, deck: Deck):
        self.hand.hand_down.append(deck.deal())
        self.double = True
        self.bet *= 2
        return self.total

    def basic_strategy(self, deck, dealer_card):
        if not val_dict[self.hand.hand_up[0]] > val_dict[self.hand.hand_up[1]]:
            self.hand.hand_up = self.hand.hand_up[::-1]
        try:
            play_state = (
                val_dict[self.hand.hand_up[0]],
                val_dict[self.hand.hand_up[1]],
                val_dict[dealer_card],
            )
            decision = soft_or_pair_outcome[play_state]
        except KeyError:
            sum_state = (sum(self.hand), val_dict[dealer_card])
            decision = other_outcome[sum_state]
        if decision == "H":
            print("\nYou hit!")
            hand_sum = self.hit(deck)
        elif decision == "S":
            print("\nYou stand!")
            hand_sum = self.stand()
        elif decision == "SP":
            raise SplitError("Basic strategy tried to split!")
        # elif decision == "SP":
        #     print("\nYou split!")
        #     hand_sum = self.split()
        elif decision == "D":
            print("\nYou double down!")
            hand_sum = self.double_down(deck)
        return hand_sum


class Dealer(Player):
    def move(self, deck):
        self.bust = False
        if self.hand.hand_down:
            face_down = self.hand.hand_down[0]
            self.hand.hand_up.append(face_down)
            print(f"\nThe dealer's second card is {face_down}")
            self.hand.hand_down = []
        if sum(self.hand) == 21 and len(self.hand.hand_up) == 2:
            self.blackjack = True
        while sum(self.hand) < 17:
            self.hit(deck)
        if sum(self.hand) > 21:
            if "A" in self.hand.hand_up:
                self.hand.hand_up.remove("A")
                self.hand.hand_up.append("1")
                self.move(deck)
            else:
                self.bust = True


dealer = Dealer()  # avoid SyntaxError


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self, deck, dealer: Dealer):
        options = move_options(self.hand)
        decision = input(
            f"\nThe Dealer has:\n\n{dealer.hand.hand_up}\n\nYou have {self.hand.hand_up}\n\nYour options are:\n\n{options}\n\nWhat do you want to do?\n\n"
        )
        dec = decision.lower()
        if dec == "hit":
            sum = self.hit(deck)
        elif dec == "stand":
            sum = self.stand()
        # elif dec == "split":
        #     sum = self.split(deck)
        elif dec == "double down":
            sum = self.double_down(deck)
        elif dec == "basic strategy":
            sum = self.basic_strategy(deck, dealer.hand.hand_up[0])
        else:
            print(f"{decision} is not a valid input. Try again:")
            self.move()
        return sum

    def place_bet(self, player_number, balance):
        self.bet = int(
            input(
                f"\n{player_number} has {balance} remaining. How much do you want to bet?\n\n"
            )
        )


class BasicStrategyPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self, dealer: Dealer):
        decision = self.basic_strategy(dealer.hand.hand_up)
        if decision == "H":
            sum = self.hit(deck)
        elif decision == "S":
            sum = self.stand()
        elif decision == "D":
            sum = self.double_down(deck)
        elif decision == "SP":
            sum = self.split()
        return sum

    def place_bet(self, player_number, balance):
        self.bet = 10  # implement bet choice function


class SemiRandomPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self, deck, dealer: Dealer):
        print(
            f"\nThe dealer has\n\n{dealer.hand.hand_up}\n\nYou have\n\n{self.hand.hand_up}"
        )
        sum = self.total
        P = (21 - sum) / 10
        random_number = random()
        if P > random_number:
            print("\nYou hit!")
            hand_sum = self.hit(deck)
        else:
            print("\nYou stand!")
            hand_sum = self.stand()
        return hand_sum

    def place_bet(self, player_number, balance):
        self.bet = 20  # implement bet choice function
