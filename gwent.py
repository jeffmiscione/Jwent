# NEEDED UPDATES
# - add unit abilities
#   - Tight Bond - The power of this card multiplies by the number of identical cards in the same row
#   - Scorch - Some units can use Scorch, their version of Scorch is bound to different rules
#   - Revive - This units may revive a discarded unit
#   - Morale Boost - This unit empower units in the same row, but only if they were played first
#   - Muster - This card summons certain other units to his/her row. These units may be drawn from your deck or your hand
#   - Agility - This unit may be placed in one of two possible rows
#   - Spy - This units will lend its power to the opposing side. In exchange you may draw two cards
# - add heroes
# - graphics!!!!
# - add commander abilities
# - add faction abilities

# Known bugs
# - how does weather impact horn?
# - how does horn impact scorch?
# - add function for the main loop
#   - it currently repeats code for player1 and then player2

import random

def clearScreen():
    print('\n \n \n \n \n \n \n \n \n \n \n')

def lookupCardType(card_name, card_database):
    first_comma_index = 0
    second_comma_index = 0
    first_index_found = False

    for card in card_database:  # look through card database
        if card[:len(card_name)] == card_name:  # find matching card in database
            for i in card:  # look for commas
                if i == ',' and first_index_found == False:
                    second_comma_index += 1
                    first_index_found = True
                elif i == ',' and first_index_found == True:
                    break
                elif first_index_found == True:
                    second_comma_index += 1
                else:
                    second_comma_index += 1
                    first_comma_index += 1

            return card[first_comma_index + 1: second_comma_index]  # determine text between first 2 commas

def lookupCardStrength(card_name, card_database):
    first_comma_index = 0
    second_comma_index = 0
    description_indicator_index = 0
    first_index_found = False

    for card in card_database:  # look through card database
        if card[:len(card_name)] == card_name:  # find matching card in database
            for i in card:  # look for commas
                if i == ',' and first_index_found == False:
                    second_comma_index += 1
                    first_index_found = True
                elif i == ',' and first_index_found == True:
                    break
                elif first_index_found == True:
                    second_comma_index += 1
                else:
                    second_comma_index += 1
                    first_comma_index += 1
            for i in card:  # look for description indicator
                if i == '#':
                    break
                else:
                    description_indicator_index += 1

            return int(card[second_comma_index + 1:description_indicator_index])  # determine text between first 2 commas

def updateBoard():
    biting_frost = False
    impenetrable_fog = False
    torrential_rain = False

    player1_melee_horn = False
    player1_ranged_horn = False
    player1_siege_horn = False
    player1_melee_score = 0
    player1_ranged_score = 0
    player1_siege_score = 0

    player2_melee_horn = False
    player2_ranged_horn = False
    player2_siege_horn = False
    player2_melee_score = 0
    player2_ranged_score = 0
    player2_siege_score = 0

    # determine weather effects
    for i in weather:
        if i == 'biting frost':
            biting_frost = True
        elif i == 'impenetrable fog':
            impenetrable_fog = True
        elif i == 'torrential rain':
            torrential_rain = True

    # determine player1 round score
    for card in player1_melee_line:     # check for commander horn in player melee row
        if card == 'commander horn':
            player1_melee_horn = True
            break
    for card in player1_melee_line:             # look through played melee line cards
        for card_info in card_database:         # match the melee card to its database entry
            if card_info[:len(card)] == card:
                if biting_frost == True:
                    player1_melee_score += 1
                elif player1_melee_horn == True:
                    player1_melee_score += 2 * lookupCardStrength(card, card_database)  # add card strength
                else:
                    player1_melee_score += lookupCardStrength(card, card_database)  # add card strength

    for card in player1_ranged_line:  # check for commander horn in player melee row
        if card == 'commander horn':
            player1_ranged_horn = True
            break
    for card in player1_ranged_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card:
                if impenetrable_fog == True:
                    player1_ranged_score += 1
                elif player1_ranged_horn == True:
                    player1_ranged_score += 2 * lookupCardStrength(card, card_database)  # add card strength
                else:
                    player1_ranged_score += lookupCardStrength(card, card_database)  # add card strength

    for card in player1_siege_line:  # check for commander horn in player melee row
        if card == 'commander horn':
            player1_siege_horn = True
            break
    for card in player1_siege_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card:
                if torrential_rain == True:
                    player1_siege_score += 1
                elif player1_siege_horn == True:
                    player1_siege_score += 2 * lookupCardStrength(card, card_database)  # add card strength
                else:
                    player1_siege_score += lookupCardStrength(card, card_database)  # add card strength

    player1_round_score = player1_melee_score + player1_ranged_score + player1_siege_score

    # determine player2 round score
    for card in player2_melee_line:     # check for commander horn in player melee row
        if card == 'commander horn':
            player2_melee_horn = True
            break
    for card in player2_melee_line:             # look through played melee line cards
        for card_info in card_database:         # match the melee card to its database entry
            if card_info[:len(card)] == card:
                if biting_frost == True:
                    player2_siege_score += 1
                elif player2_melee_horn == True:
                    player2_melee_score += 2 * lookupCardStrength(card, card_database)  # add card strength
                else:
                    player2_melee_score += lookupCardStrength(card, card_database)  # add card strength

    for card in player2_ranged_line:  # check for commander horn in player melee row
        if card == 'commander horn':
            player2_ranged_horn = True
            break
    for card in player2_ranged_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card:
                if impenetrable_fog == True:
                    player2_ranged_score += 1
                elif player2_ranged_horn == True:
                    player2_ranged_score += 2 * lookupCardStrength(card, card_database)  # add card strength
                else:
                    player2_ranged_score += lookupCardStrength(card, card_database)  # add card strength

    for card in player2_siege_line:  # check for commander horn in player melee row
        if card == 'commander horn':
            player2_siege_horn = True
            break
    for card in player2_siege_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card:
                if torrential_rain == True:
                    player2_siege_score += 1
                elif player2_siege_horn == True:
                    player2_siege_score += 2 * lookupCardStrength(card, card_database)  # add card strength
                else:
                    player2_siege_score += lookupCardStrength(card, card_database)  # add card strength

    player2_round_score = player2_melee_score + player2_ranged_score + player2_siege_score

    print('======================================================')
    print('player 1 siege line:  %s' % player1_siege_line)
    print('player 1 ranged line: %s' % player1_ranged_line)
    print('player 1 melee line:  %s' % player1_melee_line)
    print('\n')
    print('player 2 melee line:  %s' % player2_melee_line)
    print('player 2 ranged line: %s' % player2_ranged_line)
    print('player 2 siege line:  %s' % player2_siege_line)
    print('======================================================')

    print('Current Weather:  %s' % weather)
    print('Player 1 Score: %s' % player1_round_score)
    print('Player 2 Score: %s' % player2_round_score)
    print('\n')
    return(player1_round_score, player2_round_score)

def checkWeather(weather_to_check):
    for i in weather:
        if i == weather_to_check:
            return True
    return False

def checkCardInHand(played_card, player_hand, player_number):
    card_in_hand = False  # temporary flag to ensure the card is in the player's hand
    while card_in_hand == False:
        for card in player_hand:
            if card == played_card:
                card_in_hand = True
                break
        if card_in_hand == False:
            # pick new card to play
            played_card = input('PLAYER %s:  That card is not in your hand. What card would you like to play: ' % player_number)
    return played_card

def getDecoyList(melee_line, ranged_line, siege_line):
    return melee_line + ranged_line + siege_line

def scorch(card_database):
    # find highest strength
    highest_strength = 0
    for card in player1_melee_line:
        if lookupCardStrength(card, card_database) > highest_strength:
            highest_strength = lookupCardStrength(card, card_database)
    for card in player1_ranged_line:
        if lookupCardStrength(card, card_database) > highest_strength:
            highest_strength = lookupCardStrength(card, card_database)
    for card in player1_siege_line:
        if lookupCardStrength(card, card_database) > highest_strength:
            highest_strength = lookupCardStrength(card, card_database)
    for card in player2_melee_line:
        if lookupCardStrength(card, card_database) > highest_strength:
            highest_strength = lookupCardStrength(card, card_database)
    for card in player2_ranged_line:
        if lookupCardStrength(card, card_database) > highest_strength:
            highest_strength = lookupCardStrength(card, card_database)
    for card in player2_siege_line:
        if lookupCardStrength(card, card_database) > highest_strength:
            highest_strength = lookupCardStrength(card, card_database)

    # destroy cards with strength == highest_strength
    for card in player1_melee_line[:]:
        if lookupCardStrength(card, card_database) == highest_strength:
            player1_discard_pile.append(card)
            player1_melee_line.remove(card)
    for card in player1_ranged_line[:]:
        if lookupCardStrength(card, card_database) == highest_strength:
            player1_discard_pile.append(card)
            player1_ranged_line.remove(card)
    for card in player1_siege_line[:]:
        if lookupCardStrength(card, card_database) == highest_strength:
            player1_discard_pile.append(card)
            player1_siege_line.remove(card)

    for card in player2_melee_line[:]:
        if lookupCardStrength(card, card_database) == highest_strength:
            player2_discard_pile.append(card)
            player2_melee_line.remove(card)
    for card in player2_ranged_line[:]:
        if lookupCardStrength(card, card_database) == highest_strength:
            player2_discard_pile.append(card)
            player2_ranged_line.remove(card)
    for card in player2_siege_line[:]:
        if lookupCardStrength(card, card_database) == highest_strength:
            player2_discard_pile.append(card)
            player2_siege_line.remove(card)

# =================== Load Cards ===============
def loadCardDatabase(database_name):
    card_database_file = open(database_name, "r")
    imported_database = list(card_database_file)
    card_database = []
    for card in imported_database:
        if card[len(card) - 1:len(card)] == '\n':
            clean_card = card[:len(card) - 1]
            card_database.append(clean_card)
        else:
            card_database.append(card)
    card_database_file.close()

    return(card_database)
card_database = loadCardDatabase('card_database.txt')

def loadDeck(deck_name):    # loads in a text file deck
    player_deck = []
    imported_deck = open(deck_name, "r")        # load player deck from text file

    for card in imported_deck:                  # remove carriage returns from card names
        if card[len(card) - 1:len(card)] == '\n':
            clean_card = card[:len(card) - 1]
            player_deck.append(clean_card)
        else:
            player_deck.append(card)
    imported_deck.close()   # close text file

    # check to make sure deck size is correct

    random.shuffle(player_deck)     # shuffle deck

    player_hand = player_deck[:10]     # create player hand
    player_deck = player_deck[10:]     # remove cards in player hand from top of deck
    player_hand.sort()                # alphabetically sort hand

    return(player_deck, player_hand)
loaded_deck = loadDeck('player1_deck.txt')
player1_deck = loaded_deck[0]
player1_hand = loaded_deck[1]

loaded_deck = loadDeck('player2_deck.txt')
player2_deck = loaded_deck[0]
player2_hand = loaded_deck[1]

# ======================= Draw New Cards =======================
def drawNewCards(player_hand, player_deck, player_number):
    clearScreen()
    print('Player %s hand:' % player_number)
    print(player_hand)
    print('\n')

    player_discard_pile = []
    player_redraws = 2

    while player_redraws > 0:
        replaced_card = input('PLAYER %s:  Enter which card you would like to replace or type \'pass\' to keep cards: ' % player_number)
        if replaced_card == 'pass':
            player_redraws = 0
            print('\n')
        else:
            for card in player_hand:
                if card == replaced_card:
                    # remove card from hand
                    player_hand.remove(card)

                    # move card to discard_pile
                    player_discard_pile.append(card)

                    # draw new card from deck
                    player_hand.append(player_deck[0])

                    # remove drawn card from player deck
                    player_deck = player_deck[1:]

                    # reduce number of available redraws
                    player_redraws -= 1

                    player_hand.sort()
                    break
            clearScreen()
            print('Player %s hand:' % player_number)
            print(player_hand)
            print('\n')
    return(player_hand, player_deck, player_discard_pile)

player1_redraw = drawNewCards(player1_hand, player1_deck, 1)
player1_hand = player1_redraw[0]
player1_deck = player1_redraw[1]
player1_discard_pile = player1_redraw[2]

player2_redraw = drawNewCards(player2_hand, player2_deck, 2)
player2_hand = player2_redraw[0]
player2_deck = player2_redraw[1]
player2_discard_pile = player2_redraw[2]

# =================== Set Up Board ========================
player1_games_won = 0
player2_games_won = 0
games_complete = 0

weather = []

player1_melee_line = []
player1_ranged_line = []
player1_siege_line = []

player2_melee_line = []
player2_ranged_line = []
player2_siege_line = []

player_turn = random.randint(1,2)   # determine player who goes first

player1_pass = False
player2_pass = False

clearScreen()
print('GAME START')
update_scores = updateBoard()
player1_round_score = update_scores[0]
player2_round_score = update_scores[1]

# =================== Start of Game ======================
while (player1_games_won < 2) and (player2_games_won < 2) and (games_complete < 3):
    if player_turn == 1:
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
                played_card = checkCardInHand(played_card, player1_hand, 1)     # check if played card is in hand

                # make sure decoy can be played
                while (played_card == 'decoy' and (player1_melee_line + player1_ranged_line + player1_siege_line) == []):
                    played_card = input('PLAYER 1:  No cards to decoy. Pick card to play: ')
                    played_card = checkCardInHand(played_card, player1_hand, 1)     # make player pick new card

                # play played_card
                card_line = lookupCardType(played_card, card_database)

                if card_line == 'melee':
                    player1_melee_line.append(played_card)
                elif card_line == 'ranged':
                    player1_ranged_line.append(played_card)
                elif card_line == 'siege':
                    player1_siege_line.append(played_card)
                elif card_line == 'special':
                    if played_card == 'commander horn':
                        valid_line = False
                        while valid_line == False:
                            horn_line = input('PLAYER 1:  What line do you want to empower?:  ')
                            if horn_line == 'melee':
                                player1_melee_line.append(played_card)
                                valid_line = True
                            elif horn_line == 'ranged':
                                player1_ranged_line.append(played_card)
                                valid_line = True
                            elif horn_line == 'siege':
                                player1_siege_line.append(played_card)
                                valid_line = True
                            else:
                                horn_line = input('PLAYER 1:  Not valid line. What line do you want to empower?:  ')
                    elif played_card == 'biting frost':
                        if checkWeather('biting frost') == False:   # check if the weather card was already in play
                            weather.append(played_card)
                            if len(weather) == 3:
                                weather = weather[1:3]
                    elif played_card == 'impenetrable fog':
                        if checkWeather('impenetrable fog') == False:   # check if the weather card was already in play
                            weather.append(played_card)
                            if len(weather) == 3:
                                weather = weather[1:3]
                    elif played_card == 'torrential rain':
                        if checkWeather('torrential rain') == False:   # check if the weather card was already in play
                            weather.append(played_card)
                            if len(weather) == 3:
                                weather = weather[1:3]
                    elif played_card == 'clear weather':
                        weather = []
                    elif played_card == 'scorch':
                        scorch(card_database)
                    elif played_card == 'decoy':
                        # ask for cards to return
                        return_card = input('PLAYER 1:  Enter which card you would like to return: ')
                        valid_return_card = False
                        while valid_return_card == False:
                            for i in (player1_melee_line + player1_ranged_line + player1_siege_line):
                                if i == return_card:
                                    print(i)
                                    valid_return_card = True
                                    break
                            if valid_return_card == False:
                                return_card = input('PLAYER 1:  Not valid. Enter which card you would like to return: ')
                                print(return_card)

                        # determine line the return card is in
                        return_card_line = lookupCardType(return_card, card_database)

                        # add return card to player hand
                        player1_hand.append(return_card)

                        # add decoy to line removed from and remove old card
                        if return_card_line == 'melee':
                            player1_melee_line.append(played_card)
                            player1_melee_line.remove(return_card)
                        elif return_card_line == 'ranged':
                            player1_ranged_line.append(played_card)
                            player1_ranged_line.remove(return_card)
                        elif return_card_line == 'siege':
                            player1_siege_line.append(played_card)
                            player1_siege_line.remove(return_card)

                # remove played_card from player1_hand
                player1_hand.remove(played_card)

        # update board and scores
        clearScreen()
        update_scores = updateBoard()
        player1_round_score = update_scores[0]
        player2_round_score = update_scores[1]
        player_turn = 2

    if player_turn == 2:
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
                played_card = checkCardInHand(played_card, player2_hand, 2)     # check if played card is in hand

                while (played_card == 'decoy' and (player2_melee_line + player2_ranged_line + player2_siege_line) == []):
                    played_card = input('PLAYER 2:  No cards to decoy. Pick card to play: ')
                    played_card = checkCardInHand(played_card, player2_hand, 2)     # make player pick new card

                # play played_card
                card_line = lookupCardType(played_card, card_database)

                if card_line == 'melee':
                    player2_melee_line.append(played_card)
                elif card_line == 'ranged':
                    player2_ranged_line.append(played_card)
                elif card_line == 'siege':
                    player2_siege_line.append(played_card)
                elif card_line == 'special':
                    if played_card == 'commander horn':
                        valid_line = False
                        while valid_line == False:
                            horn_line = input('PLAYER 2:  What line do you want to empower?:  ')
                            if horn_line == 'melee':
                                player2_melee_line.append(played_card)
                                valid_line = True
                            elif horn_line == 'ranged':
                                player2_ranged_line.append(played_card)
                                valid_line = True
                            elif horn_line == 'siege':
                                player2_siege_line.append(played_card)
                                valid_line = True
                            else:
                                horn_line = input('PLAYER 1:  Not valid line. What line do you want to empower?:  ')
                    elif played_card == 'biting frost':
                        if checkWeather('biting frost') == False:   # check if the weather card was already in play
                            weather.append(played_card)
                            if len(weather) == 3:
                                weather = weather[1:3]
                    elif played_card == 'impenetrable fog':
                        if checkWeather('impenetrable fog') == False:   # check if the weather card was already in play
                            weather.append(played_card)
                            if len(weather) == 3:
                                weather = weather[1:3]
                    elif played_card == 'torrential rain':
                        if checkWeather('torrential rain') == False:   # check if the weather card was already in play
                            weather.append(played_card)
                            if len(weather) == 3:
                                weather = weather[1:3]
                    elif played_card == 'clear weather':
                        weather = []
                    elif played_card == 'scorch':
                        scorch(card_database)
                    elif played_card == 'decoy':
                        # ask for cards to return
                        return_card = input('PLAYER 2:  Enter which card you would like to return: ')
                        valid_return_card = False
                        while valid_return_card == False:
                            for i in (player2_melee_line + player2_ranged_line + player2_siege_line):
                                if i == return_card:
                                    print(i)
                                    valid_return_card = True
                                    break
                            if valid_return_card == False:
                                return_card = input('PLAYER 2:  Not valid. Enter which card you would like to return: ')
                                print(return_card)

                        # determine line the return card is in
                        return_card_line = lookupCardType(return_card, card_database)

                        # add return card to player hand
                        player2_hand.append(return_card)

                        # add decoy to line removed from and remove old card
                        if return_card_line == 'melee':
                            player2_melee_line.append(played_card)
                            player2_melee_line.remove(return_card)
                        elif return_card_line == 'ranged':
                            player2_ranged_line.append(played_card)
                            player2_ranged_line.remove(return_card)
                        elif return_card_line == 'siege':
                            player2_siege_line.append(played_card)
                            player2_siege_line.remove(return_card)

                # remove played_card from player1_hand
                player2_hand.remove(played_card)

        # update board and scores
        clearScreen()
        update_scores = updateBoard()
        player1_round_score = update_scores[0]
        player2_round_score = update_scores[1]
        player_turn = 1

    # check if both players have passed
    if (player1_pass == True) and (player2_pass == True):
        clearScreen()
        # increment number of played games
        games_complete += 1

        # determine who won the round
        if player1_round_score > player2_round_score:
            player1_games_won += 1
            player_turn = 1
            print('Player 1 wins the round!')
        elif player2_round_score > player1_round_score:
            player2_games_won += 1
            player_turn = 2
            print('Player 2 wins the round!')
        else:
            player_turn = random.randint(1,2)
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
        weather = []

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
