from deck import Deck, Hand
from players import Dealer, HumanPlayer, BasicStrategyPlayer, SemiRandomPlayer

deck = Deck()
deck.shuffle()
dealer = Dealer()


def player_count(player_type):
    return int(input(f"How many {player_type} do you want?\n\n"))


def get_players():
    dealer = Dealer()
    human_players = player_count("human players")
    bs_players = player_count("basic strategy players")
    sr_players = player_count("semi random players")
    if human_players + bs_players + sr_players > 5:
        print("No more than 5 players allowed!")
        human_players, bs_players, sr_players = get_players()
    return human_players, bs_players, sr_players


player_type_count = get_players()
player_number_list = [f"Player{i+1}" for i in range(5)]
player_dict = dict()
n = 0

for i in range(player_type_count[0]):  # add human players
    player_dict[player_number_list[n]] = HumanPlayer()
    n += 1
for i in range(player_type_count[1]):  # add basic strategy players
    player_dict[player_number_list[n]] = BasicStrategyPlayer()
    n += 1
for i in range(player_type_count[2]):  # add semi random players
    player_dict[player_number_list[n]] = SemiRandomPlayer()
    n += 1


def reset_players():
    dealer.hand = Hand()
    for i in range(5):
        try:
            player = player_dict[player_number_list[i]]
            player.bet = 0
            player.bust = False
            player.blackjack = False
            player.hand = Hand()
        except KeyError:
            break


def collect_bets():
    for i in range(5):
        try:
            player = player_dict[player_number_list[i]]
            balance = player.balance
            player.place_bet(player_number_list[i], balance)
            if balance - player.bet < 0:
                print(f"Insufficient funds to bet {player.bet}, you were only able to bet {player.balance}.")
                player.bet = player.balance
            player.balance -= player.bet
        except KeyError:
            break


def deal_hands():
    dealer.initial_deal(deck)
    for i in range(5):
        try:
            player = player_dict[player_number_list[i]]
            player.initial_deal(deck)
        except KeyError:
            break


def blackjack_check(player):
    if player.total == 21:
        player.blackjack = True


def soft_hand_check(player):
    if "A" in player.hand.hand_up:
        player.hand.hand_up.remove("A")
        player.hand.hand_up.append("1")
        return True
    else:
        return False


def turn(player):
    end = False
    blackjack_check(player)
    if player.blackjack:
        end = True
    while not end:
        sum = player.move(deck, dealer)
        if sum == 0:
            end = True
        elif sum > 21:
            soft = soft_hand_check(player)
            if not soft:
                player.bust = True
                end = True


def player_turns():
    for i in range(5):
        try:
            player = player_dict[player_number_list[i]]
            turn(player)
            if player.blackjack:
                print(f"{player_number_list[i]} has got blackjack!")
        except KeyError:
            break


def dealer_turn():
    dealer.move(deck)


def check_hands():
    print(f"\nThe dealer ended up with {dealer.hand.hand_up}")
    if dealer.blackjack:
        for i in range(5):
            try:
                player = player_dict[player_number_list[i]]
                if player.blackjack:
                    print(f"{player_number_list[i]} ties with the dealer.")
                    player.balance += player.bet
                else:
                    print(f"{player_number_list[i]} loses!")
            except KeyError:
                break
    else:
        for i in range(5):
            try:
                player = player_dict[player_number_list[i]]
                if player.bust:
                    print(f"\n{player_number_list[i]} lost.")
                    continue
                elif player.blackjack:
                    winnings = player.bet*2.5
                    player.balance += winnings
                    print(f"\n{player_number_list[i]} has blackjack and wins {winnings}!")
                    continue
                if dealer.bust:
                    winnings = player.bet*2
                    player.balance += winnings
                    print(f"Dealer busts with {dealer.hand.hand_up}, you win {winnings}!")
                elif player.total > dealer.total:
                    winnings = player.bet*2
                    player.balance += winnings
                    print(f"\n{player_number_list[i]} beat the dealer and wins {winnings}!")
                elif player.total == dealer.total:
                    player.balance += player.bet
                    print(f"\n{player_number_list[i]} ties with the dealer.")
                else:
                    print(f"\n{player_number_list[i]} lost.")
            except KeyError:
                break


def new_game():
    again = input("Do you want to play again? y/n\n\n")
    if again == "y":
        return True
    elif again == "n":
        return False
    else:
        print(f"{again} is not a valid response, please enter 'y' or 'n'.")
        new_game()

def play():
    reset_players()
    collect_bets()
    deal_hands()
    player_turns()
    dealer_turn()
    check_hands()

carry_on = True

while carry_on:
    play()
    carry_on = new_game()
