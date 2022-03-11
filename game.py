from deck import Deck, Hand
from players import Dealer, HumanPlayer, BasicStrategyPlayer, SemiRandomPlayer

deck = Deck()
for i in range(10):
    deck.shuffle()
dealer = Dealer()


def player_count(player_type):
    return int(input(f"How many {player_type} do you want?\n\n"))


def get_players():
    try:
        human_players = int(player_count("human players"))
        bs_players = int(0)  # player_count("basic strategy players")
        sr_players = int(player_count("semi random players"))
        if human_players < 0 or bs_players < 0 or sr_players < 0:
            print("Player numbers must be non-negative!")
            human_players, bs_players, sr_players = get_players()
    except ValueError:
        print("That isn't a valid number of players!")
        human_players, bs_players, sr_players = get_players()
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
# for i in range(player_type_count[1]):  # add basic strategy players
#     player_dict[player_number_list[n]] = BasicStrategyPlayer()
#     n += 1
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
            dealer.blackjack = False
        except KeyError:
            break


def collect_bets():
    for i in range(5):
        try:
            player = player_dict[player_number_list[i]]
            balance = player.balance
            player.place_bet(player_number_list[i], balance)
            if balance - player.bet < 0:
                print(
                    f"Insufficient funds to bet {player.bet}, you were only able to bet {player.balance}."
                )
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


# def split_turn(player, deck, dealer):
#     player.hand1.hand_up.append(deck.draw())
#     player.hand2.hand_up.append(deck.draw())
#     print(player.hand1.hand_up, player.hand2.hand_up)
#     #hand1
#     end = False
#     if sum(player.hand1.hand_up) == 21:
#         end = True
#     while not end:
#         pass


def turn(player):
    end = False
    blackjack_check(player)
    if player.blackjack:
        end = True
    while not end:
        sum = player.move(deck, dealer)
        # if player.spl:
        #     split_turn(player, deck, dealer)
        if player.double:
            end = True
        elif sum == 0:
            end = True
        elif sum > 21:
            soft = soft_hand_check(player)
            if not soft:
                player.bust = True
                end = True
                print(f"\nYou bust with {player.hand.hand_up}!")


def player_turns():
    for i in range(5):
        try:
            player = player_dict[player_number_list[i]]
            print(f"\nIt's {player_number_list[i]}'s turn!")
            turn(player)
            if player.blackjack:
                print(f"{player_number_list[i]} has got blackjack!")
        except KeyError:
            break


def dealer_turn():
    dealer.move(deck)


def check_hands():
    if dealer.blackjack:
        print(f"\nThe dealer got blackjack with {dealer.hand.hand_up}")
        for i in range(5):
            try:
                player = player_dict[player_number_list[i]]
                if player.blackjack:
                    print(f"{player_number_list[i]} ties with the dealer.")
                    player.balance += player.bet
                else:
                    print(f"\n{player_number_list[i]} loses!")
            except KeyError:
                break
    else:
        for i in range(5):
            try:
                player = player_dict[player_number_list[i]]
                if player.hand.hand_down:
                    player.hand.hand_up.append(player.hand.hand_down[0])
                    player.hand.hand_down = []
                    print(f"\nYour final hand is {player.hand.hand_up}")
                    if player.total == 22:
                        player.hand.hand_up.remove("A")
                        player.hand.hand_up.append("1")
                if player.bust:
                    continue
                elif player.blackjack:
                    winnings = player.bet * 2.5
                    player.balance += winnings
                    print(
                        f"\n{player_number_list[i]} got blackjack with {player.hand.hand_up} and wins {winnings}!"
                    )
                    continue
                if dealer.bust:
                    winnings = player.bet * 2
                    player.balance += winnings
                    print(
                        f"\nDealer busts with {dealer.hand.hand_up}, you win {winnings}!"
                    )
                elif player.total > dealer.total:
                    winnings = player.bet * 2
                    player.balance += winnings
                    print(
                        f"\n{player_number_list[i]} got {player.hand.hand_up} beating the dealer with {dealer.hand.hand_up} and wins {winnings}!"
                    )
                elif player.total == dealer.total:
                    player.balance += player.bet
                    print(f"\n{player_number_list[i]} ties with the dealer.")
                else:
                    print(
                        f"\nThe dealer got {dealer.hand.hand_up} but {player_number_list[i]} got {player.hand.hand_up} so lost."
                    )
            except KeyError:
                break


def new_game():
    again = input("\nDo you want to play again? y/n\n\n")
    if again == "y":
        return True
    elif again == "n":
        return False
    else:
        print(f"\n{again} is not a valid response, please enter 'y' or 'n'.")
        return new_game()


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
