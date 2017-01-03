# NEEDED UPDATES
# - add unit abilities
#   - Tight Bond - The power of this card multiplies by the number of identical cards in the same row
# - add heroes
# - graphics!!!!
# - add commander abilities
# - add faction abilities

# Known bugs
# - how does weather impact horn?
# - how does horn impact scorch?
# - revive doesn't perform the abilities of the revived card
# - add function for the main loop
#   - it currently repeats code for p1 and then p2

import random

def clearScreen():
    print('\n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n')

def lookupCardType(card_name, card_database):
    first_comma_index = 0
    second_comma_index = 0
    third_comma_index = 0
    commas_found = 0
    description_indicator_index = 0

    for card in card_database:  # look through card database
        if card[:len(card_name)] == card_name:  # find matching card in database
            for i in card:  # look for commas
                if i == ',' and commas_found == 0:
                    second_comma_index += 1
                    third_comma_index += 1
                    commas_found += 1
                elif i == ',' and commas_found == 1:
                    third_comma_index += 1
                    commas_found += 1
                elif i ==',' and commas_found == 2:
                    break
                elif commas_found == 0:
                    first_comma_index += 1
                    second_comma_index += 1
                    third_comma_index += 1
                elif commas_found == 1:
                    second_comma_index += 1
                    third_comma_index += 1
                elif commas_found == 2:
                    third_comma_index += 1
            for i in card:  # look for description indicator
                if i == '#':
                    break
                else:
                    description_indicator_index += 1

            return(card[first_comma_index+1:second_comma_index])  # determine text between first 2 commas

def lookupCardAbility(card_name, card_database):
    first_comma_index = 0
    second_comma_index = 0
    third_comma_index = 0
    commas_found = 0
    description_indicator_index = 0

    for card in card_database:  # look through card database
        if card[:len(card_name)] == card_name:  # find matching card in database
            for i in card:  # look for commas
                if i == ',' and commas_found == 0:
                    second_comma_index += 1
                    third_comma_index += 1
                    commas_found += 1
                elif i == ',' and commas_found == 1:
                    third_comma_index += 1
                    commas_found += 1
                elif i ==',' and commas_found == 2:
                    break
                elif commas_found == 0:
                    first_comma_index += 1
                    second_comma_index += 1
                    third_comma_index += 1
                elif commas_found == 1:
                    second_comma_index += 1
                    third_comma_index += 1
                elif commas_found == 2:
                    third_comma_index += 1
            for i in card:  # look for description indicator
                if i == '#':
                    break
                else:
                    description_indicator_index += 1

            return(card[second_comma_index+1:third_comma_index])  # determine text between first 2 commas

def lookupCardStrength(card_name, card_database):
    first_comma_index = 0
    second_comma_index = 0
    third_comma_index = 0
    commas_found = 0
    description_indicator_index = 0

    for card in card_database:  # look through card database
        if card[:len(card_name)] == card_name:  # find matching card in database
            for i in card:  # look for commas
                if i == ',' and commas_found == 0:
                    second_comma_index += 1
                    third_comma_index += 1
                    commas_found += 1
                elif i == ',' and commas_found == 1:
                    third_comma_index += 1
                    commas_found += 1
                elif i ==',' and commas_found == 2:
                    break
                elif commas_found == 0:
                    first_comma_index += 1
                    second_comma_index += 1
                    third_comma_index += 1
                elif commas_found == 1:
                    second_comma_index += 1
                    third_comma_index += 1
                elif commas_found == 2:
                    third_comma_index += 1
            for i in card:  # look for description indicator
                if i == '#':
                    break
                else:
                    description_indicator_index += 1

            return int(card[third_comma_index+1:description_indicator_index])  # determine text between first 2 commas

def updateBoard():
    biting_frost = False
    impenetrable_fog = False
    torrential_rain = False

    p1_melee_horn = False
    p1_ranged_horn = False
    p1_siege_horn = False
    p1_melee_score = 0
    p1_ranged_score = 0
    p1_siege_score = 0

    p2_melee_horn = False
    p2_ranged_horn = False
    p2_siege_horn = False
    p2_melee_score = 0
    p2_ranged_score = 0
    p2_siege_score = 0

    # determine weather effects
    for i in weather:
        if i == 'biting frost':
            biting_frost = True
        elif i == 'impenetrable fog':
            impenetrable_fog = True
        elif i == 'torrential rain':
            torrential_rain = True

    # determine p1 round score
    for card in p1_melee_line:     # check for commander horn in player melee row
        if card == 'commander horn':
            p1_melee_horn = True
            break
    for card in p1_melee_line:             # look through played melee line cards
        for card_info in card_database:         # match the melee card to its database entry
            if card_info[:len(card)] == card and card != 'commander horn':
                if biting_frost == True:
                    print(card)
                    p1_melee_score += 1
                elif p1_melee_horn == True:
                    p1_melee_score += 2 * lookupCardStrength(card, card_database)  # add card strength
                else:
                    p1_melee_score += lookupCardStrength(card, card_database)  # add card strength

    for card in p1_ranged_line:  # check for commander horn in player melee row
        if card == 'commander horn':
            p1_ranged_horn = True
            break
    for card in p1_ranged_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card and card != 'commander horn':
                if impenetrable_fog == True:
                    p1_ranged_score += 1
                elif p1_ranged_horn == True:
                    p1_ranged_score += 2 * lookupCardStrength(card, card_database)  # add card strength
                else:
                    p1_ranged_score += lookupCardStrength(card, card_database)  # add card strength

    for card in p1_siege_line:  # check for commander horn in player melee row
        if card == 'commander horn':
            p1_siege_horn = True
            break
    for card in p1_siege_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card and card != 'commander horn':
                if torrential_rain == True:
                    p1_siege_score += 1
                elif p1_siege_horn == True:
                    p1_siege_score += 2 * lookupCardStrength(card, card_database)  # add card strength
                else:
                    p1_siege_score += lookupCardStrength(card, card_database)  # add card strength

    p1_round_score = p1_melee_score + p1_ranged_score + p1_siege_score

    # determine p2 round score
    for card in p2_melee_line:     # check for commander horn in player melee row
        if card == 'commander horn':
            p2_melee_horn = True
            break
    for card in p2_melee_line:             # look through played melee line cards
        for card_info in card_database:         # match the melee card to its database entry
            if card_info[:len(card)] == card and card != 'commander horn':
                if biting_frost == True:
                    p2_siege_score += 1
                elif p2_melee_horn == True:
                    p2_melee_score += 2 * lookupCardStrength(card, card_database)  # add card strength
                else:
                    p2_melee_score += lookupCardStrength(card, card_database)  # add card strength

    for card in p2_ranged_line:  # check for commander horn in player melee row
        if card == 'commander horn':
            p2_ranged_horn = True
            break
    for card in p2_ranged_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card and card != 'commander horn':
                if impenetrable_fog == True:
                    p2_ranged_score += 1
                elif p2_ranged_horn == True:
                    p2_ranged_score += 2 * lookupCardStrength(card, card_database)  # add card strength
                else:
                    p2_ranged_score += lookupCardStrength(card, card_database)  # add card strength

    for card in p2_siege_line:  # check for commander horn in player melee row
        if card == 'commander horn':
            p2_siege_horn = True
            break
    for card in p2_siege_line:  # look through played melee line cards
        for card_info in card_database:  # match the melee card to its database entry
            if card_info[:len(card)] == card and card != 'commander horn':
                if torrential_rain == True:
                    p2_siege_score += 1
                elif p2_siege_horn == True:
                    p2_siege_score += 2 * lookupCardStrength(card, card_database)  # add card strength
                else:
                    p2_siege_score += lookupCardStrength(card, card_database)  # add card strength

    p2_round_score = p2_melee_score + p2_ranged_score + p2_siege_score

    print('======================================================')
    print('player 1 siege line:  %s' % p1_siege_line)
    print('player 1 ranged line: %s' % p1_ranged_line)
    print('player 1 melee line:  %s' % p1_melee_line)
    print('\n')
    print('player 2 melee line:  %s' % p2_melee_line)
    print('player 2 ranged line: %s' % p2_ranged_line)
    print('player 2 siege line:  %s' % p2_siege_line)
    print('======================================================')

    print('Current Weather:  %s' % weather)
    print('Player 1 Score: %s' % p1_round_score)
    print('Player 2 Score: %s' % p2_round_score)
    print('\n')
    return(p1_round_score, p2_round_score)

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

def scorch(card_database, p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line):
    # find highest strength
    highest_strength = 0
    for card in p1_melee_line:
        if lookupCardStrength(card, card_database) > highest_strength:
            highest_strength = lookupCardStrength(card, card_database)
    for card in p1_ranged_line:
        if lookupCardStrength(card, card_database) > highest_strength:
            highest_strength = lookupCardStrength(card, card_database)
    for card in p1_siege_line:
        if lookupCardStrength(card, card_database) > highest_strength:
            highest_strength = lookupCardStrength(card, card_database)
    for card in p2_melee_line:
        if lookupCardStrength(card, card_database) > highest_strength:
            highest_strength = lookupCardStrength(card, card_database)
    for card in p2_ranged_line:
        if lookupCardStrength(card, card_database) > highest_strength:
            highest_strength = lookupCardStrength(card, card_database)
    for card in p2_siege_line:
        if lookupCardStrength(card, card_database) > highest_strength:
            highest_strength = lookupCardStrength(card, card_database)

    # destroy cards with strength == highest_strength
    for card in p1_melee_line[:]:
        if lookupCardStrength(card, card_database) == highest_strength:
            p1_discard_pile.append(card)
            p1_melee_line.remove(card)
    for card in p1_ranged_line[:]:
        if lookupCardStrength(card, card_database) == highest_strength:
            p1_discard_pile.append(card)
            p1_ranged_line.remove(card)
    for card in p1_siege_line[:]:
        if lookupCardStrength(card, card_database) == highest_strength:
            p1_discard_pile.append(card)
            p1_siege_line.remove(card)

    for card in p2_melee_line[:]:
        if lookupCardStrength(card, card_database) == highest_strength:
            p2_discard_pile.append(card)
            p2_melee_line.remove(card)
    for card in p2_ranged_line[:]:
        if lookupCardStrength(card, card_database) == highest_strength:
            p2_discard_pile.append(card)
            p2_ranged_line.remove(card)
    for card in p2_siege_line[:]:
        if lookupCardStrength(card, card_database) == highest_strength:
            p2_discard_pile.append(card)
            p2_siege_line.remove(card)

    return (p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)

def revive(player_turn, card_database, p1_hand, p2_hand, p1_deck, p2_deck, p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line):
    # create graveyard from discard pile that removes any special cards
    graveyard = []
    if player_turn == 1:
        new_discard_pile = p1_discard_pile
    elif player_turn == 2:
        new_discard_pile = p2_discard_pile

    if len(new_discard_pile) > 0:
        for card in new_discard_pile:
            if lookupCardType(card, card_database) != 'special':
                graveyard.append(card)

        # check if graveyard > 0
        if len(graveyard) > 0:
            # print out the graveyard
            print('PLAYER %s GRAVEYARD:  ' % player_turn)
            print(graveyard)

            # ask for input of card to revive
            revive_card = input('PLAYER %s: What card would you like to revive:  ' % player_turn)

            # make sure requested card is in graveyard
            revive_card_valid = False
            while revive_card_valid == False:
                for card in graveyard:
                    if card == revive_card:
                        revive_card_valid = True
                        break
                if revive_card_valid == False:
                    print(graveyard)
                    revive_card = input('PLAYER %s: Invalid card. What card would you like to revive:  ' % player_turn)

            # determine requested card's line
            revive_card_line = lookupCardType(revive_card,card_database)

            # remove the requested card from the discard pile (not the graveyard)
            if len(new_discard_pile) == 1:
                new_discard_pile = []
            else:
                new_discard_pile.remove(revive_card)

            if player_turn == 1:
                p1_discard_pile = new_discard_pile
            elif player_turn == 2:
                p2_discard_pile = new_discard_pile

            # ======================================================================
            # check for abilities
            card_ability = lookupCardAbility(revive_card, card_database)
            play_card_as_normal = True

            if card_ability == 'revive':
                # p1_discard_pile = revive(p1_discard_pile, 1, card_database)
                revive_action = revive(player_turn, card_database, p1_hand, p2_hand, p1_deck, p2_deck,
                                       p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line,
                                       p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                p1_hand = revive_action[0]
                p2_hand = revive_action[1]
                p1_deck = revive_action[2]
                p2_deck = revive_action[3]
                p1_discard_pile = revive_action[4]
                p2_discard_pile = revive_action[5]
                p1_melee_line = revive_action[6]
                p1_ranged_line = revive_action[7]
                p1_siege_line = revive_action[8]
                p2_melee_line = revive_action[9]
                p2_ranged_line = revive_action[10]
                p2_siege_line = revive_action[11]

            if card_ability == 'scorch':
                scorched_cards = scorch(card_database, p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line,
                                        p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                p1_discard_pile = scorched_cards[0]
                p2_discard_pile = scorched_cards[1]
                p1_melee_line = scorched_cards[2]
                p1_ranged_line = scorched_cards[3]
                p1_siege_line = scorched_cards[4]
                p2_melee_line = scorched_cards[5]
                p2_ranged_line = scorched_cards[6]
                p2_siege_line = scorched_cards[7]

            if card_ability == 'morale boost':
                boosted_action = moraleBoost(revive_card, card_database, player_turn, p1_melee_line, p1_ranged_line,
                                             p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                p1_melee_line = boosted_action[0]
                p1_ranged_line = boosted_action[1]
                p1_siege_line = boosted_action[2]
                p2_melee_line = boosted_action[3]
                p2_ranged_line = boosted_action[4]
                p2_siege_line = boosted_action[5]

            if card_ability == 'spy':
                # prevent from being placed in current player line
                spy_action = spy(revive_card, revive_card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line,
                                 p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                p1_hand = spy_action[0]
                p2_hand = spy_action[1]
                p1_deck = spy_action[2]
                p2_deck = spy_action[3]
                p1_melee_line = spy_action[4]
                p1_ranged_line = spy_action[5]
                p1_siege_line = spy_action[6]
                p2_melee_line = spy_action[7]
                p2_ranged_line = spy_action[8]
                p2_siege_line = spy_action[9]

                play_card_as_normal = False

            if card_ability == 'muster':
                muster_action = muster(revive_card, revive_card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck,
                                       p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line,
                                       p2_siege_line)
                p1_hand = muster_action[0]
                p2_hand = muster_action[1]
                p1_deck = muster_action[2]
                p2_deck = muster_action[3]
                p1_melee_line = muster_action[4]
                p1_ranged_line = muster_action[5]
                p1_siege_line = muster_action[6]
                p2_melee_line = muster_action[7]
                p2_ranged_line = muster_action[8]
                p2_siege_line = muster_action[9]
                play_card_as_normal = False

            if card_ability == 'agility':
                agility_action = agility(revive_card, revive_card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck,
                                         p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line,
                                         p2_ranged_line, p2_siege_line)
                p1_hand = agility_action[0]
                p2_hand = agility_action[1]
                p1_deck = agility_action[2]
                p2_deck = agility_action[3]
                p1_melee_line = agility_action[4]
                p1_ranged_line = agility_action[5]
                p1_siege_line = agility_action[6]
                p2_melee_line = agility_action[7]
                p2_ranged_line = agility_action[8]
                p2_siege_line = agility_action[9]
                play_card_as_normal = False

            # place card in combat line
            if play_card_as_normal == True:
                # place the requested card in the line
                if player_turn == 1:
                    print('1revive card is %s' % revive_card)
                    if revive_card_line == 'melee':
                        p1_melee_line.append(revive_card)
                    if revive_card_line == 'ranged':
                        p1_ranged_line.append(revive_card)
                    if revive_card_line == 'siege':
                        p1_siege_line.append(revive_card)
                elif player_turn == 2:
                    if revive_card_line == 'melee':
                        p2_melee_line.append(revive_card)
                    if revive_card_line == 'ranged':
                        p2_ranged_line.append(revive_card)
                    if revive_card_line == 'siege':
                        p2_siege_line.append(revive_card)

    return(p1_hand, p2_hand, p1_deck, p2_deck, p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)

def spy(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line):
    if player_turn == 1:
        # place spy on opponent line
        if card_line == 'melee':
            p2_melee_line.append(played_card)
        elif card_line == 'ranged':
            p2_ranged_line.append(played_card)
        elif card_line == 'siege':
            p2_siege_line.append(played_card)
        # draw 2 cards
        for i in range(0, 2):
            if len(p1_deck) > 0:
                p1_hand.append(p1_deck[0])
                del (p1_deck[0])
    elif player_turn == 2:
        # place spy on opponent line
        if card_line == 'melee':
            p1_melee_line.append(played_card)
        elif card_line == 'ranged':
            p1_ranged_line.append(played_card)
        elif card_line == 'siege':
            p1_siege_line.append(played_card)
        # draw 2 cards
        for i in range(0, 2):
            if len(p2_deck) > 0:
                p2_hand.append(p2_deck[0])
                del (p2_deck[0])

    return(p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)

def moraleBoost(played_card, card_database, player_turn, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line):
    if player_turn == 1:
        if lookupCardType(played_card, card_database) == 'melee':
            p1_melee_line.append('commander horn')
        elif lookupCardType(played_card, card_database) == 'ranged':
            p1_ranged_line.append('commander horn')
        elif lookupCardType(played_card, card_database) == 'siege':
            p1_siege_line.append('commander horn')
    elif player_turn == 2:
        if lookupCardType(played_card, card_database) == 'melee':
            p2_melee_line.append('commander horn')
        elif lookupCardType(played_card, card_database) == 'ranged':
            p2_ranged_line.append('commander horn')
        elif lookupCardType(played_card, card_database) == 'siege':
            p2_siege_line.append('commander horn')
    return(p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)

def muster(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line):
    removed_from_hand = False # used to add 1 version of the card back into hand so the mainloop removal works correctly

    if player_turn == 1:
        # look through player hand for matching card names
        if len(p1_hand) > 0:
            for card in p1_hand[:]:
                if card == played_card:
                    # set removed_from_hand_flag
                    removed_from_hand = True

                    # remove any matches
                    p1_hand.remove(card)

                    # play matches
                    if card_line == 'melee':
                        p1_melee_line.append(card)
                    elif card_line == 'ranged':
                        p1_ranged_line.append(card)
                    elif card_line == 'siege':
                        p1_siege_line.append(card)

        if removed_from_hand == True:  # add card back into hand for mainloop card removal
            p1_hand.append(played_card)

        # look through player deck for matching card names
        if len(p1_deck) > 0:
            for card in p1_deck[:]:
                if card == played_card:
                    # remove any matches
                    p1_deck.remove(card)

                    # play matches
                    if card_line == 'melee':
                        p1_melee_line.append(card)
                    elif card_line == 'ranged':
                        p1_ranged_line.append(card)
                    elif card_line == 'siege':
                        p1_siege_line.append(card)

    elif player_turn == 2:
        # look through player hand for matching card names
        if len(p2_hand) > 0:
            for card in p2_hand[:]:
                if card == played_card:
                    # set removed_from_hand_flag
                    removed_from_hand = True

                    # remove any matches
                    p2_hand.remove(card)

                    # play matches
                    if card_line == 'melee':
                        p2_melee_line.append(card)
                    elif card_line == 'ranged':
                        p2_ranged_line.append(card)
                    elif card_line == 'siege':
                        p2_siege_line.append(card)

        if removed_from_hand == True:       # add card back into hand for mainloop card removal
            p2_hand.append(played_card)

        # look through player deck for matching card names
        if len(p2_deck) > 0:
            for card in p2_deck[:]:
                if card == played_card:
                    # remove any matches
                    p2_deck.remove(card)

                    # play matches
                    if card_line == 'melee':
                        p2_melee_line.append(card)
                    elif card_line == 'ranged':
                        p2_ranged_line.append(card)
                    elif card_line == 'siege':
                        p2_siege_line.append(card)
    return(p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)

def agility(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line):
    selected_line = input('PLAYER %s: melee or ranged:  ' % player_turn)
    valid_line = False
    while valid_line == False:
        if selected_line == 'melee' or selected_line == 'ranged':
            valid_line = True
        if valid_line == False:
            selected_line = input('PLAYER %s: melee or ranged:  ' % player_turn)

    if player_turn == 1:
        if selected_line == 'melee':
            p1_melee_line.append(played_card)
        elif selected_line == 'ranged':
            p1_ranged_line.append(played_card)
    elif player_turn == 2:
        if selected_line == 'melee':
            p2_melee_line.append(played_card)
        elif selected_line == 'ranged':
            p2_ranged_line.append(played_card)

    return(p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)

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
loaded_deck = loadDeck('p1_deck.txt')
p1_deck = loaded_deck[0]
p1_hand = loaded_deck[1]

loaded_deck = loadDeck('p2_deck.txt')
p2_deck = loaded_deck[0]
p2_hand = loaded_deck[1]

# ======================= Draw New Cards =======================
def drawNewCards(player_hand, player_deck, player_number):
    clearScreen()
    print('Player %s hand:' % player_number)
    print(player_hand)
    print('\n')

    player_redraws = 2

    while player_redraws > 0:
        replaced_card = input('PLAYER %s:  Enter which card you would like to replace or type \'pass\' to keep cards: ' % player_number)
        if replaced_card == 'pass':
            player_redraws = 0
            print('\n')
        else:
            for card in player_hand:
                if card == replaced_card:
                    # remove undesired card from hand
                    player_hand.remove(card)

                    # draw new card from deck
                    player_hand.append(player_deck[0])

                    # remove drawn card from player deck
                    del(player_deck[0])

                    # move undesired card to back to deck
                    player_deck.append(card)

                    # reshuffle deck with undesired card in it
                    random.shuffle(player_deck)

                    # reduce number of available redraws
                    player_redraws -= 1

                    player_hand.sort()
                    break
            clearScreen()
            print('Player %s hand:' % player_number)
            print(player_hand)
            print('\n')
    return(player_hand, player_deck)

p1_redraw = drawNewCards(p1_hand, p1_deck, 1)
p1_hand = p1_redraw[0]
p1_deck = p1_redraw[1]
p1_discard_pile = []

p2_redraw = drawNewCards(p2_hand, p2_deck, 2)
p2_hand = p2_redraw[0]
p2_deck = p2_redraw[1]
p2_discard_pile = []

# =================== Set Up Board ========================
p1_games_won = 0
p2_games_won = 0
games_complete = 0

weather = []

p1_melee_line = []
p1_ranged_line = []
p1_siege_line = []

p2_melee_line = []
p2_ranged_line = []
p2_siege_line = []

player_turn = random.randint(1,2)   # determine player who goes first

p1_pass = False
p2_pass = False

clearScreen()
print('GAME START')
update_scores = updateBoard()
p1_round_score = update_scores[0]
p2_round_score = update_scores[1]

# =================== Start of Game ======================
while (p1_games_won < 2) and (p2_games_won < 2) and (games_complete < 3):
    if player_turn == 1:
        # player 1 takes turn
        if len(p1_hand) == 0:
            p1_pass = True
        elif p1_pass == False:
            print('Player 1 hand:')
            print(p1_hand)
            print('\n')
            played_card = input('PLAYER 1:  Enter which card you would like to play or type \'pass\' to end turn: ')
            if played_card == 'pass':
                p1_pass = True
            else:
                played_card = checkCardInHand(played_card, p1_hand, 1)     # check if played card is in hand

                # make sure decoy can be played
                while (played_card == 'decoy' and (p1_melee_line + p1_ranged_line + p1_siege_line) == []):
                    played_card = input('PLAYER 1:  No cards to decoy. Pick card to play: ')
                    played_card = checkCardInHand(played_card, p1_hand, 1)     # make player pick new card

                # play played_card
                card_line = lookupCardType(played_card, card_database)

                # check for abilities
                card_ability = lookupCardAbility(played_card, card_database)
                play_card_as_normal = True

                if card_ability == 'revive':
                    #p1_discard_pile = revive(p1_discard_pile, 1, card_database)
                    revive_action = revive(player_turn, card_database, p1_hand, p2_hand, p1_deck, p2_deck,
                                           p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line,
                                           p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                    p1_hand = revive_action[0]
                    p2_hand = revive_action[1]
                    p1_deck = revive_action[2]
                    p2_deck = revive_action[3]
                    p1_discard_pile = revive_action[4]
                    p2_discard_pile = revive_action[5]
                    p1_melee_line = revive_action[6]
                    p1_ranged_line = revive_action[7]
                    p1_siege_line = revive_action[8]
                    p2_melee_line = revive_action[9]
                    p2_ranged_line = revive_action[10]
                    p2_siege_line = revive_action[11]

                if card_ability == 'scorch':
                    scorched_cards = scorch(card_database, p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                    p1_discard_pile = scorched_cards[0]
                    p2_discard_pile = scorched_cards[1]
                    p1_melee_line = scorched_cards[2]
                    p1_ranged_line= scorched_cards[3]
                    p1_siege_line= scorched_cards[4]
                    p2_melee_line = scorched_cards[5]
                    p2_ranged_line = scorched_cards[6]
                    p2_siege_line = scorched_cards[7]

                if card_ability == 'morale boost':
                    boosted_action = moraleBoost(played_card, card_database, player_turn, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                    p1_melee_line = boosted_action[0]
                    p1_ranged_line = boosted_action[1]
                    p1_siege_line = boosted_action[2]
                    p2_melee_line = boosted_action[3]
                    p2_ranged_line = boosted_action[4]
                    p2_siege_line = boosted_action[5]

                if card_ability == 'spy':
                    # prevent from being placed in current player line
                    spy_action = spy(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                    p1_hand = spy_action[0]
                    p2_hand = spy_action[1]
                    p1_deck = spy_action[2]
                    p2_deck = spy_action[3]
                    p1_melee_line = spy_action[4]
                    p1_ranged_line = spy_action[5]
                    p1_siege_line = spy_action[6]
                    p2_melee_line = spy_action[7]
                    p2_ranged_line = spy_action[8]
                    p2_siege_line = spy_action[9]

                    play_card_as_normal = False

                if card_ability == 'muster':
                    muster_action = muster(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck,
                                           p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line,
                                           p2_siege_line)
                    p1_hand = muster_action[0]
                    p2_hand = muster_action[1]
                    p1_deck = muster_action[2]
                    p2_deck = muster_action[3]
                    p1_melee_line = muster_action[4]
                    p1_ranged_line = muster_action[5]
                    p1_siege_line = muster_action[6]
                    p2_melee_line = muster_action[7]
                    p2_ranged_line = muster_action[8]
                    p2_siege_line = muster_action[9]
                    play_card_as_normal = False

                if card_ability == 'agility':
                    agility_action = agility(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck,
                                             p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line,
                                             p2_ranged_line, p2_siege_line)
                    p1_hand = agility_action[0]
                    p2_hand = agility_action[1]
                    p1_deck = agility_action[2]
                    p2_deck = agility_action[3]
                    p1_melee_line = agility_action[4]
                    p1_ranged_line = agility_action[5]
                    p1_siege_line = agility_action[6]
                    p2_melee_line = agility_action[7]
                    p2_ranged_line = agility_action[8]
                    p2_siege_line = agility_action[9]
                    play_card_as_normal = False

                # place card in combat line
                if play_card_as_normal == True:
                    if card_line == 'melee':
                        p1_melee_line.append(played_card)
                    elif card_line == 'ranged':
                        p1_ranged_line.append(played_card)
                    elif card_line == 'siege':
                        p1_siege_line.append(played_card)
                    elif card_line == 'special':
                        if played_card == 'commander horn':
                            valid_line = False
                            while valid_line == False:
                                horn_line = input('PLAYER 1:  What line do you want to empower?:  ')
                                if horn_line == 'melee':
                                    p1_melee_line.append(played_card)
                                    valid_line = True
                                elif horn_line == 'ranged':
                                    p1_ranged_line.append(played_card)
                                    valid_line = True
                                elif horn_line == 'siege':
                                    p1_siege_line.append(played_card)
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
                            scorched_cards = scorch(card_database, p1_discard_pile, p2_discard_pile,
                                                    p1_melee_line, p1_ranged_line, p1_siege_line,
                                                    p2_melee_line, p2_ranged_line, p2_siege_line)
                            p1_discard_pile = scorched_cards[0]
                            p2_discard_pile = scorched_cards[1]
                            p1_melee_line = scorched_cards[2]
                            p1_ranged_line = scorched_cards[3]
                            p1_siege_line = scorched_cards[4]
                            p2_melee_line = scorched_cards[5]
                            p2_ranged_line = scorched_cards[6]
                            p2_siege_line = scorched_cards[7]
                        elif played_card == 'decoy':
                            # ask for cards to return
                            return_card = input('PLAYER 1:  Enter which card you would like to return: ')
                            valid_return_card = False
                            while valid_return_card == False:
                                for i in (p1_melee_line + p1_ranged_line + p1_siege_line):
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
                            p1_hand.append(return_card)

                            # add decoy to line removed from and remove old card
                            if return_card_line == 'melee':
                                p1_melee_line.append(played_card)
                                p1_melee_line.remove(return_card)
                            elif return_card_line == 'ranged':
                                p1_ranged_line.append(played_card)
                                p1_ranged_line.remove(return_card)
                            elif return_card_line == 'siege':
                                p1_siege_line.append(played_card)
                                p1_siege_line.remove(return_card)

                # remove played_card from p1_hand
                p1_hand.remove(played_card)
                if (p2_pass == False) and (len(p2_hand) != 0):
                    input('Enter anything for Player 2 to take turn.')

        # update board and scores
        clearScreen()
        update_scores = updateBoard()
        p1_round_score = update_scores[0]
        p2_round_score = update_scores[1]
        player_turn = 2

    if player_turn == 2:
        # player 2 takes turn
        if len(p2_hand) == 0:
            p2_pass = True
        elif p2_pass == False:
            print('Player 2 hand:')
            print(p2_hand)
            print('\n')
            played_card = input('PLAYER 2:  Enter which card you would like to play or type \'pass\' to end turn: ')
            if played_card == 'pass':
                p2_pass = True
            else:
                played_card = checkCardInHand(played_card, p2_hand, 2)     # check if played card is in hand

                # make sure decoy can be played
                while (played_card == 'decoy' and (p2_melee_line + p2_ranged_line + p2_siege_line) == []):
                    played_card = input('PLAYER 2:  No cards to decoy. Pick card to play: ')
                    played_card = checkCardInHand(played_card, p2_hand, 2)     # make player pick new card

                # play played_card
                card_line = lookupCardType(played_card, card_database)

                # check for abilities
                card_ability = lookupCardAbility(played_card, card_database)
                play_card_as_normal = True

                if card_ability == 'revive':
                    #p2_discard_pile = revive(p2_discard_pile, 2, card_database)
                    revive_action = revive(player_turn, card_database, p1_hand, p2_hand, p1_deck, p2_deck,
                                           p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line,
                                           p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                    p1_hand = revive_action[0]
                    p2_hand = revive_action[1]
                    p1_deck = revive_action[2]
                    p2_deck = revive_action[3]
                    p1_discard_pile = revive_action[4]
                    p2_discard_pile = revive_action[5]
                    p1_melee_line = revive_action[6]
                    p1_ranged_line = revive_action[7]
                    p1_siege_line = revive_action[8]
                    p2_melee_line = revive_action[9]
                    p2_ranged_line = revive_action[10]
                    p2_siege_line = revive_action[11]

                if card_ability == 'scorch':
                    scorched_cards = scorch(card_database, p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                    p1_discard_pile = scorched_cards[0]
                    p2_discard_pile = scorched_cards[1]
                    p1_melee_line = scorched_cards[2]
                    p1_ranged_line= scorched_cards[3]
                    p1_siege_line= scorched_cards[4]
                    p2_melee_line = scorched_cards[5]
                    p2_ranged_line = scorched_cards[6]
                    p2_siege_line = scorched_cards[7]

                if card_ability == 'morale boost':
                    boosted_action = moraleBoost(played_card, card_database, player_turn, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                    p1_melee_line = boosted_action[0]
                    p1_ranged_line = boosted_action[1]
                    p1_siege_line = boosted_action[2]
                    p2_melee_line = boosted_action[3]
                    p2_ranged_line = boosted_action[4]
                    p2_siege_line = boosted_action[5]

                if card_ability == 'spy':
                    # prevent from being placed in current player line
                    spy_action = spy(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                    p1_hand = spy_action[0]
                    p2_hand = spy_action[1]
                    p1_deck = spy_action[2]
                    p2_deck = spy_action[3]
                    p1_melee_line = spy_action[4]
                    p1_ranged_line = spy_action[5]
                    p1_siege_line = spy_action[6]
                    p2_melee_line = spy_action[7]
                    p2_ranged_line = spy_action[8]
                    p2_siege_line = spy_action[9]

                    play_card_as_normal = False

                if card_ability == 'muster':
                    muster_action = muster(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck,
                                           p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line,
                                           p2_siege_line)
                    p1_hand = muster_action[0]
                    p2_hand = muster_action[1]
                    p1_deck = muster_action[2]
                    p2_deck = muster_action[3]
                    p1_melee_line = muster_action[4]
                    p1_ranged_line = muster_action[5]
                    p1_siege_line = muster_action[6]
                    p2_melee_line = muster_action[7]
                    p2_ranged_line = muster_action[8]
                    p2_siege_line = muster_action[9]
                    play_card_as_normal = False

                if card_ability == 'agility':
                    agility_action = agility(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck,
                                             p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line,
                                             p2_ranged_line, p2_siege_line)
                    p1_hand = agility_action[0]
                    p2_hand = agility_action[1]
                    p1_deck = agility_action[2]
                    p2_deck = agility_action[3]
                    p1_melee_line = agility_action[4]
                    p1_ranged_line = agility_action[5]
                    p1_siege_line = agility_action[6]
                    p2_melee_line = agility_action[7]
                    p2_ranged_line = agility_action[8]
                    p2_siege_line = agility_action[9]
                    play_card_as_normal = False

                # place card in combat line
                if play_card_as_normal == True:
                    if card_line == 'melee':
                        p2_melee_line.append(played_card)
                    elif card_line == 'ranged':
                        p2_ranged_line.append(played_card)
                    elif card_line == 'siege':
                        p2_siege_line.append(played_card)
                    elif card_line == 'special':
                        if played_card == 'commander horn':
                            valid_line = False
                            while valid_line == False:
                                horn_line = input('PLAYER 2:  What line do you want to empower?:  ')
                                if horn_line == 'melee':
                                    p2_melee_line.append(played_card)
                                    valid_line = True
                                elif horn_line == 'ranged':
                                    p2_ranged_line.append(played_card)
                                    valid_line = True
                                elif horn_line == 'siege':
                                    p2_siege_line.append(played_card)
                                    valid_line = True
                                else:
                                    horn_line = input('PLAYER 2:  Not valid line. What line do you want to empower?:  ')
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
                            scorched_cards = scorch(card_database, p1_discard_pile, p2_discard_pile,
                                                    p1_melee_line, p1_ranged_line, p1_siege_line,
                                                    p2_melee_line, p2_ranged_line, p2_siege_line)
                            p1_discard_pile = scorched_cards[0]
                            p2_discard_pile = scorched_cards[1]
                            p1_melee_line = scorched_cards[2]
                            p1_ranged_line = scorched_cards[3]
                            p1_siege_line = scorched_cards[4]
                            p2_melee_line = scorched_cards[5]
                            p2_ranged_line = scorched_cards[6]
                            p2_siege_line = scorched_cards[7]
                        elif played_card == 'decoy':
                            # ask for cards to return
                            return_card = input('PLAYER 2:  Enter which card you would like to return: ')
                            valid_return_card = False
                            while valid_return_card == False:
                                for i in (p2_melee_line + p2_ranged_line + p2_siege_line):
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
                            p2_hand.append(return_card)

                            # add decoy to line removed from and remove old card
                            if return_card_line == 'melee':
                                p2_melee_line.append(played_card)
                                p2_melee_line.remove(return_card)
                            elif return_card_line == 'ranged':
                                p2_ranged_line.append(played_card)
                                p2_ranged_line.remove(return_card)
                            elif return_card_line == 'siege':
                                p2_siege_line.append(played_card)
                                p2_siege_line.remove(return_card)

                # remove played_card from p2_hand
                p2_hand.remove(played_card)
                if (p1_pass == False) and (len(p1_hand) != 0):
                    input('Enter anything for Player 1 to take turn.')

        # update board and scores
        clearScreen()
        update_scores = updateBoard()
        p1_round_score = update_scores[0]
        p2_round_score = update_scores[1]
        player_turn = 1

    # check if both players have passed
    if (p1_pass == True) and (p2_pass == True):
        clearScreen()
        # increment number of played games
        games_complete += 1

        # determine who won the round
        if p1_round_score > p2_round_score:
            p1_games_won += 1
            player_turn = 1
            print('Player 1 wins the round!')
        elif p2_round_score > p1_round_score:
            p2_games_won += 1
            player_turn = 2
            print('Player 2 wins the round!')
        else:
            player_turn = random.randint(1,2)
            print('This round was a tie!')

        # reset player passed status
        p1_pass = False
        p2_pass = False

        # move line cards to discard piles
        for card in p1_melee_line:
            p1_discard_pile.append(card)
        for card in p1_ranged_line:
            p1_discard_pile.append(card)
        for card in p1_siege_line:
            p1_discard_pile.append(card)

        for card in p2_melee_line:
            p2_discard_pile.append(card)
        for card in p2_ranged_line:
            p2_discard_pile.append(card)
        for card in p2_siege_line:
            p2_discard_pile.append(card)

        # clear line lists
        p1_melee_line = []
        p1_ranged_line = []
        p1_siege_line = []
        p2_melee_line = []
        p2_ranged_line = []
        p2_siege_line = []
        weather = []

        # update scores
        update_scores = updateBoard()
        p1_round_score = update_scores[0]
        p2_round_score = update_scores[1]

clearScreen()
# count who has more wins
if p1_games_won > p2_games_won:
    print('Player 1 Wins!')
elif p2_games_won > p1_games_won:
    print('Player 2 Wins!')
else:
    print('It is a tie!')
