# NEEDED UPDATES
# - add weather cards
# - add warhorn cards
# - add commander abilities
# - add unit abilities

import random

def clearScreen():
    print('\n \n \n \n \n \n \n \n \n \n \n')

def updateBoard():
    print('======================================================')
    print('player 1 siege line:  %s' % player1_siege_line)
    print('player 1 ranged line: %s' % player1_ranged_line)
    print('player 1 melee line:  %s' % player1_melee_line)
    print('\n')
    print('player 2 melee line:  %s' % player2_melee_line)
    print('player 2 ranged line: %s' % player2_ranged_line)
    print('player 2 siege line:  %s' % player2_siege_line)
    print('======================================================')

    player1_round_score = 0
    player2_round_score = 0

    # determine player1 round score
    for card in player1_melee_line:             # look through played melee line cards
        for card_info in card_database:         # match the melee card to its database entry
            if card_info[:len(card)] == card:
                player1_round_score += int(card_info[len(card_info) - 1:])         # add card strength
    for card in player1_ranged_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card:
                player1_round_score += int(card_info[len(card_info) - 1:])  # add card strength
    for card in player1_siege_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card:
                player1_round_score += int(card_info[len(card_info) - 1:])  # add card strength

    # determine player2 round score
    for card in player2_melee_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card:
                player2_round_score += int(card_info[len(card_info) - 1:])  # add card strength
    for card in player2_ranged_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card:
                player2_round_score += int(card_info[len(card_info) - 1:])  # add card strength
    for card in player2_siege_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card:
                player2_round_score += int(card_info[len(card_info) - 1:])  # add card strength

    print('Player 1 Score: %s' % player1_round_score)
    print('Player 2 Score: %s' % player2_round_score)
    print('\n')
    return(player1_round_score, player2_round_score)

# =================== Load Card Database ===============
card_database_file = open("card_database.txt", "r")
imported_database = list(card_database_file)
card_database = []
for card in imported_database:
    if card[len(card) - 1:len(card)] == '\n':
        clean_card = card[:len(card) - 1]
        card_database.append(clean_card)
    else:
        card_database.append(card)
card_database_file.close()

# ==================== Load Decks ======================
# load player 1 deck from text file
player1_deck = []
imported_deck = open("player1_deck.txt", "r")
for card in imported_deck:
    if card[len(card)-1:len(card)] == '\n':
        clean_card = card[:len(card)-1]
        player1_deck.append(clean_card)
    else:
        player1_deck.append(card)
imported_deck.close()
    # check to make sure deck size is correct

# load player 2 deck from text file
player2_deck = []
imported_deck = open("player2_deck.txt", "r")
for card in imported_deck:
    if card[len(card)-1:len(card)] == '\n':
        clean_card = card[:len(card)-1]
        player2_deck.append(clean_card)
    else:
        player2_deck.append(card)
imported_deck.close()
    # check to make sure deck size is correct

# shuffle decks
random.shuffle(player1_deck)
random.shuffle(player2_deck)

# ======================= Draw Hands =======================
# draw player 1 hand
player1_hand = player1_deck[:10]
player1_deck = player1_deck[10:]
player1_hand.sort()

# draw player 2 hand
player2_hand = player2_deck[:10]
player2_deck = player2_deck[10:]
player2_hand.sort()

# ======================= Draw New Cards=======================
# player 1 select new cards
clearScreen()
print('Player 1 hand:')
print(player1_hand)
print('\n')

player1_discard_pile = []
player1_redraws = 2

while player1_redraws > 0:
    replaced_card = input('PLAYER 1:  Enter which card you would like to replace or type \'pass\' to keep cards: ')
    if replaced_card == 'pass':
        player1_redraws = 0
        print('\n')
    else:
        for card in player1_hand:
            if card == replaced_card:
                # remove card from hand
                player1_hand.remove(card)

                # move card to discard_pile
                player1_discard_pile.append(card)

                # draw new card from deck
                player1_hand.append(player1_deck[0])

                # remove drawn card from player deck
                player1_deck = player1_deck[1:]

                # reduce number of available redraws
                player1_redraws -= 1

                player1_hand.sort()
                break
        clearScreen()
        print('Player 1 hand:')
        print(player1_hand)
        print('\n')

# player 2 select new cards
clearScreen()
print('Player 2 hand:')
print(player2_hand)
print('\n')

player2_discard_pile = []
player2_redraws = 2

while player2_redraws > 0:
    replaced_card = input('PLAYER 2:  Enter which card you would like to replace or type \'pass\' to keep cards: ')
    if replaced_card == 'pass':
        player2_redraws = 0
        print('\n')
    else:
        for card in player2_hand:
            if card == replaced_card:
                # remove card from hand
                player2_hand.remove(card)

                # move card to discard_pile
                player2_discard_pile.append(card)

                # draw new card from deck
                player2_hand.append(player2_deck[0])

                # remove drawn card from player deck
                player2_deck = player2_deck[1:]

                # reduce number of available redraws
                player2_redraws -= 1

                player2_hand.sort()
                break
        clearScreen()
        print('Player 2 hand:')
        print(player2_hand)
        print('\n')

# =================== Set Up Board ========================
player1_games_won = 0
player2_games_won = 0
games_complete = 0

player1_melee_line = []
player1_ranged_line = []
player1_siege_line = []

player2_melee_line = []
player2_ranged_line = []
player2_siege_line = []

# determine starting player
starting_player = random.randint(0,2)

player1_pass = False
player2_pass = False

clearScreen()
print('GAME START')
update_scores = updateBoard()
player1_round_score = update_scores[0]
player2_round_score = update_scores[1]

# =================== Start of Game ======================
while (player1_games_won < 2) and (player2_games_won < 2) and (games_complete < 3):
    if starting_player == 1:
        # player 1 takes turn
        if len(player1_hand) == 0:
            player1_pass = True
        elif player1_pass == False:
            print('Player 1 hand:')
            print(player1_hand)
            print('\n')
            played_card = input('PLAYER 1:  Enter which card you would like to play or type \'pass\' to end turn: ')
            if played_card == 'pass':
                player1_pass = True
            else:
                # check if played card is valid
                card_valid = False      # temporary flag to ensure the card is in the player's hand
                while card_valid == False:
                    for card in player1_hand:
                        if card == played_card:
                            card_valid = True
                            break
                    if card_valid == False:
                        # pick new card to play
                        played_card = input('PLAYER 1:  That card is not in your hand. What card would you like to play: ')

                # add played_card to player1 line
                lower_comma_index = 0
                upper_comma_index = 0
                lower_index_found = False

                for card in card_database:                                  # look through card database
                    if card[:len(played_card)] == played_card:              # find matching card in database
                        for i in card:                                      # look for commas
                            if i == ',' and lower_index_found == False:
                                upper_comma_index += 1
                                lower_index_found = True
                            elif i == ',' and lower_index_found == True:
                                break
                            elif lower_index_found == True:
                                upper_comma_index += 1
                            else:
                                upper_comma_index += 1
                                lower_comma_index += 1

                        card_line = card[lower_comma_index + 1: upper_comma_index]  # determine text between first 2 commas

                print('cardline is %s' % card_line)

                if card_line == 'melee':
                    player1_melee_line.append(played_card)
                elif card_line == 'ranged':
                    player1_ranged_line.append(played_card)
                else:
                    player1_siege_line.append(played_card)

                # remove played_card from player1_hand
                player1_hand.remove(played_card)

        # update board and scores
        clearScreen()
        update_scores = updateBoard()
        player1_round_score = update_scores[0]
        player2_round_score = update_scores[1]

        # player 2 takes turn
        if len(player2_hand) == 0:
            player2_pass = True
        elif player2_pass == False:
            print('Player 2 hand:')
            print(player2_hand)
            print('\n')
            played_card = input('PLAYER 2:  Enter which card you would like to play or type \'pass\' to end turn: ')
            if played_card == 'pass':
                player2_pass = True
            else:
                # check if played card is valid
                card_valid = False      # temporary flag to ensure the card is in the player's hand
                while card_valid == False:
                    for card in player2_hand:
                        if card == played_card:
                            card_valid = True
                            break
                    if card_valid == False:
                        # pick new card to play
                        played_card = input('PLAYER 2:  That card is not in your hand. What card would you like to play: ')

                # add played_card to player2 line
                lower_comma_index = 0
                upper_comma_index = 0
                lower_index_found = False

                for card in card_database:                                  # look through card database
                    if card[:len(played_card)] == played_card:              # find matching card in database
                        for i in card:                                      # look for commas
                            if i == ',' and lower_index_found == False:
                                upper_comma_index += 1
                                lower_index_found = True
                            elif i == ',' and lower_index_found == True:
                                break
                            elif lower_index_found == True:
                                upper_comma_index += 1
                            else:
                                upper_comma_index += 1
                                lower_comma_index += 1

                        card_line = card[lower_comma_index + 1: upper_comma_index]  # determine text between first 2 commas

                print('cardline is %s' % card_line)

                if card_line == 'melee':
                    player2_melee_line.append(played_card)
                elif card_line == 'ranged':
                    player2_ranged_line.append(played_card)
                else:
                    player2_siege_line.append(played_card)

                # remove played_card from player2_hand
                player2_hand.remove(played_card)

        # update scores
        clearScreen()
        update_scores = updateBoard()
        player1_round_score = update_scores[0]
        player2_round_score = update_scores[1]

    if starting_player == 2:
        # player 2 takes turn
        if len(player2_hand) == 0:
            player2_pass = True
        elif player2_pass == False:
            print('Player 2 hand:')
            print(player2_hand)
            print('\n')
            played_card = input('PLAYER 2:  Enter which card you would like to play or type \'pass\' to end turn: ')
            if played_card == 'pass':
                player2_pass = True
            else:
                # check if played card is valid
                card_valid = False  # temporary flag to ensure the card is in the player's hand
                while card_valid == False:
                    for card in player2_hand:
                        if card == played_card:
                            card_valid = True
                            break
                    if card_valid == False:
                        # pick new card to play
                        played_card = input(
                            'PLAYER 2:  That card is not in your hand. What card would you like to play: ')

                # add played_card to player2 line
                lower_comma_index = 0
                upper_comma_index = 0
                lower_index_found = False

                for card in card_database:  # look through card database
                    if card[:len(played_card)] == played_card:  # find matching card in database
                        for i in card:  # look for commas
                            if i == ',' and lower_index_found == False:
                                upper_comma_index += 1
                                lower_index_found = True
                            elif i == ',' and lower_index_found == True:
                                break
                            elif lower_index_found == True:
                                upper_comma_index += 1
                            else:
                                upper_comma_index += 1
                                lower_comma_index += 1

                        card_line = card[
                                    lower_comma_index + 1: upper_comma_index]  # determine text between first 2 commas

                print('cardline is %s' % card_line)

                if card_line == 'melee':
                    player2_melee_line.append(played_card)
                elif card_line == 'ranged':
                    player2_ranged_line.append(played_card)
                else:
                    player2_siege_line.append(played_card)

                # remove played_card from player2_hand
                player2_hand.remove(played_card)

        # update scores
        clearScreen()
        update_scores = updateBoard()
        player1_round_score = update_scores[0]
        player2_round_score = update_scores[1]

        # player 1 takes turn
        if len(player1_hand) == 0:
            player1_pass = True
        elif player1_pass == False:
            print('Player 1 hand:')
            print(player1_hand)
            print('\n')
            played_card = input('PLAYER 1:  Enter which card you would like to play or type \'pass\' to end turn: ')
            if played_card == 'pass':
                player1_pass = True
            else:
                # check if played card is valid
                card_valid = False  # temporary flag to ensure the card is in the player's hand
                while card_valid == False:
                    for card in player1_hand:
                        if card == played_card:
                            card_valid = True
                            break
                    if card_valid == False:
                        # pick new card to play
                        played_card = input(
                            'PLAYER 1:  That card is not in your hand. What card would you like to play: ')

                # add played_card to player1 line
                lower_comma_index = 0
                upper_comma_index = 0
                lower_index_found = False

                for card in card_database:  # look through card database
                    if card[:len(played_card)] == played_card:  # find matching card in database
                        for i in card:  # look for commas
                            if i == ',' and lower_index_found == False:
                                upper_comma_index += 1
                                lower_index_found = True
                            elif i == ',' and lower_index_found == True:
                                break
                            elif lower_index_found == True:
                                upper_comma_index += 1
                            else:
                                upper_comma_index += 1
                                lower_comma_index += 1

                        card_line = card[
                                    lower_comma_index + 1: upper_comma_index]  # determine text between first 2 commas

                print('cardline is %s' % card_line)

                if card_line == 'melee':
                    player1_melee_line.append(played_card)
                elif card_line == 'ranged':
                    player1_ranged_line.append(played_card)
                else:
                    player1_siege_line.append(played_card)

                # remove played_card from player1_hand
                player1_hand.remove(played_card)

        # update board and scores
        clearScreen()
        update_scores = updateBoard()
        player1_round_score = update_scores[0]
        player2_round_score = update_scores[1]

    # check if both players have passed
    if (player1_pass == True) and (player2_pass == True):
        clearScreen()
        # increment number of played games
        games_complete += 1

        # determine who won the round
        if player1_round_score > player2_round_score:
            player1_games_won += 1
            starting_player = 1
            print('Player 1 wins the round!')
        elif player2_round_score > player1_round_score:
            player2_games_won += 1
            starting_player = 2
            print('Player 2 wins the round!')
        else:
            starting_player = random.randint(0,2)
            print('This round was a tie!')

        # reset player passed status
        player1_pass = False
        player2_pass = False

        # move line cards to discard piles
        for card in player1_melee_line:
            player1_discard_pile.append(card)
        for card in player1_ranged_line:
            player1_discard_pile.append(card)
        for card in player1_siege_line:
            player1_discard_pile.append(card)

        for card in player2_melee_line:
            player1_discard_pile.append(card)
        for card in player2_ranged_line:
            player1_discard_pile.append(card)
        for card in player2_siege_line:
            player1_discard_pile.append(card)

        # clear line lists
        player1_melee_line = []
        player1_ranged_line = []
        player1_siege_line = []
        player2_melee_line = []
        player2_ranged_line = []
        player2_siege_line = []

        # update scores
        update_scores = updateBoard()
        player1_round_score = update_scores[0]
        player2_round_score = update_scores[1]


clearScreen()
# count who has more wins
if player1_games_won > player2_games_won:
    print('Player 1 Wins!')
elif player2_games_won > player1_games_won:
    print('Player 2 Wins!')
else:
    print('It is a tie!')