# https://nikolak.com/pyqt-qt-designer-getting-started/
# https://www.youtube.com/watch?v=o81Q3oyz6rg
# https://nikolak.com/pyqt-threading-tutorial/

# make the ui into a .py file
# pyuic4 board.ui -o board.py

# make the resource list from the ui file into a .py
# http://stackoverflow.com/questions/15864762/pyqt4-how-do-i-compile-and-import-a-qrc-file-into-my-program
# http://stackoverflow.com/questions/15864762/pyqt4-how-do-i-compile-and-import-a-qrc-file-into-my-program

# TO DO:
# pop-up window that shows larger version of the card
# clickable cards
# add more card slots
# set the card slots to disabled when not displaying anything (see p1 draw hand)
# smaller cards (can't fit on screen at the moment)

from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL, Qt
import sys
import board       # the ui file that has been converted to python
import random
import os

class playGame(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
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
                        elif i == ',' and commas_found == 2:
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

                    return (card[first_comma_index + 1:second_comma_index])  # determine text between first 2 commas

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
                        elif i == ',' and commas_found == 2:
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

                    return (card[second_comma_index + 1:third_comma_index])  # determine text between first 2 commas

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
                        elif i == ',' and commas_found == 2:
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

                    return int(card[
                               third_comma_index + 1:description_indicator_index])  # determine text between first 2 commas

        def updateBoard(card_database, weather, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line,
                        p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line):
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

            # determine tight bond cards
            p1_melee_tight_bond_dict = {}
            for card in p1_melee_line:
                if lookupCardAbility(card, card_database) == 'tight bond':
                    if card in p1_melee_tight_bond_dict:  # check if already in dictionary
                        p1_melee_tight_bond_dict[card] += 1  # if already there, add 1 to count
                    else:
                        p1_melee_tight_bond_dict[card] = 1  # if not already in dictionary, add to list
            p1_ranged_tight_bond_dict = {}
            for card in p1_ranged_line:
                if lookupCardAbility(card, card_database) == 'tight bond':
                    if card in p1_ranged_tight_bond_dict:  # check if already in dictionary
                        p1_ranged_tight_bond_dict[card] += 1  # if already there, add 1 to count
                    else:
                        p1_ranged_tight_bond_dict[card] = 1  # if not already in dictionary, add to list
            p1_siege_tight_bond_dict = {}
            for card in p1_siege_line:
                if lookupCardAbility(card, card_database) == 'tight bond':
                    if card in p1_siege_tight_bond_dict:  # check if already in dictionary
                        p1_siege_tight_bond_dict[card] += 1  # if already there, add 1 to count
                    else:
                        p1_siege_tight_bond_dict[card] = 1  # if not already in dictionary, add to list

            p2_melee_tight_bond_dict = {}
            for card in p2_melee_line:
                if lookupCardAbility(card, card_database) == 'tight bond':
                    if card in p2_melee_tight_bond_dict:  # check if already in dictionary
                        p2_melee_tight_bond_dict[card] += 1  # if already there, add 1 to count
                    else:
                        p2_melee_tight_bond_dict[card] = 1  # if not already in dictionary, add to list
            p2_ranged_tight_bond_dict = {}
            for card in p2_ranged_line:
                if lookupCardAbility(card, card_database) == 'tight bond':
                    if card in p2_ranged_tight_bond_dict:  # check if already in dictionary
                        p2_ranged_tight_bond_dict[card] += 1  # if already there, add 1 to count
                    else:
                        p2_ranged_tight_bond_dict[card] = 1  # if not already in dictionary, add to list
            p2_siege_tight_bond_dict = {}
            for card in p2_siege_line:
                if lookupCardAbility(card, card_database) == 'tight bond':
                    if card in p2_siege_tight_bond_dict:  # check if already in dictionary
                        p2_siege_tight_bond_dict[card] += 1  # if already there, add 1 to count
                    else:
                        p2_siege_tight_bond_dict[card] = 1  # if not already in dictionary, add to list

            # determine p1 round score
            for card in p1_melee_line[:]:  # check for commander horn in player melee row
                if p1_melee_horn == True and card == 'commander horn':
                    p1_melee_line.remove('commander horn')  # remove horn if there is more than 1
                if card == 'commander horn':
                    p1_melee_horn = True
            p1_melee_line.sort()
            for card in p1_melee_line:  # look through played melee line cards
                points = 0
                for card_info in card_database:  # match the melee card to its database entry
                    if card_info[
                       :len(card)] == card and card != 'commander horn' and biting_frost == True:  # weather condition
                        points = 1
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p1_melee_tight_bond_dict[card] * points  # add card strength
                        if p1_melee_horn == True:
                            points = 2 * points

                    elif card_info[:len(
                            card)] == card and card != 'commander horn' and biting_frost == False:  # no weather condition
                        points = lookupCardStrength(card, card_database)
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p1_melee_tight_bond_dict[card] * points  # add card strength
                        if p1_melee_horn == True:
                            points = 2 * points
                p1_melee_score += points

            for card in p1_ranged_line[:]:  # check for commander horn in player melee row
                if p1_ranged_horn == True and card == 'commander horn':
                    p1_ranged_line.remove('commander horn')  # remove horn if there is more than 1
                if card == 'commander horn':
                    p1_ranged_horn = True
            p1_ranged_line.sort()
            for card in p1_ranged_line:  # look through played melee line cards
                points = 0
                for card_info in card_database:  # match the melee card to its database entry
                    if card_info[:len(
                            card)] == card and card != 'commander horn' and impenetrable_fog == True:  # weather condition
                        points = 1
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p1_ranged_tight_bond_dict[card] * points  # add card strength
                        if p1_ranged_horn == True:
                            points = 2 * points

                    elif card_info[:len(
                            card)] == card and card != 'commander horn' and impenetrable_fog == False:  # no weather condition
                        points = lookupCardStrength(card, card_database)
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p1_ranged_tight_bond_dict[card] * points  # add card strength
                        if p1_ranged_horn == True:
                            points = 2 * points
                p1_ranged_score += points

            for card in p1_siege_line[:]:  # check for commander horn in player melee row
                if p1_siege_horn == True and card == 'commander horn':
                    p1_siege_line.remove('commander horn')  # remove horn if there is more than 1
                if card == 'commander horn':
                    p1_siege_horn = True
            p1_siege_line.sort()
            for card in p1_siege_line:  # look through played melee line cards
                points = 0
                for card_info in card_database:  # match the melee card to its database entry
                    if card_info[:len(
                            card)] == card and card != 'commander horn' and torrential_rain == True:  # weather condition
                        points = 1
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p1_siege_tight_bond_dict[card] * points  # add card strength
                        if p1_siege_horn == True:
                            points = 2 * points

                    elif card_info[:len(
                            card)] == card and card != 'commander horn' and torrential_rain == False:  # no weather condition
                        points = lookupCardStrength(card, card_database)
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p1_siege_tight_bond_dict[card] * points  # add card strength
                        if p1_siege_horn == True:
                            points = 2 * points
                p1_siege_score += points

            p1_round_score = p1_melee_score + p1_ranged_score + p1_siege_score

            # determine p2 round score
            for card in p2_melee_line[:]:  # check for commander horn in player melee row
                if p2_melee_horn == True and card == 'commander horn':
                    p2_melee_line.remove('commander horn')  # remove horn if there is more than 1
                if card == 'commander horn':
                    p2_melee_horn = True
            p2_melee_line.sort()
            for card in p2_melee_line:  # look through played melee line cards
                points = 0
                for card_info in card_database:  # match the melee card to its database entry
                    if card_info[
                       :len(card)] == card and card != 'commander horn' and biting_frost == True:  # weather condition
                        points = 1
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p2_melee_tight_bond_dict[card] * points  # add card strength
                        if p2_melee_horn == True:
                            points = 2 * points

                    elif card_info[
                         :len(
                             card)] == card and card != 'commander horn' and biting_frost == False:  # no weather condition
                        points = lookupCardStrength(card, card_database)
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p2_melee_tight_bond_dict[card] * points  # add card strength
                        if p2_melee_horn == True:
                            points = 2 * points
                p2_melee_score += points

            for card in p2_ranged_line[:]:  # check for commander horn in player melee row
                if p2_ranged_horn == True and card == 'commander horn':
                    p2_ranged_line.remove('commander horn')  # remove horn if there is more than 1
                if card == 'commander horn':
                    p2_ranged_horn = True
            p2_ranged_line.sort()
            for card in p2_ranged_line:  # look through played melee line cards
                points = 0
                for card_info in card_database:  # match the melee card to its database entry
                    if card_info[
                       :len(
                           card)] == card and card != 'commander horn' and impenetrable_fog == True:  # weather condition
                        points = 1
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p2_ranged_tight_bond_dict[card] * points  # add card strength
                        if p2_ranged_horn == True:
                            points = 2 * points

                    elif card_info[
                         :len(
                             card)] == card and card != 'commander horn' and impenetrable_fog == False:  # no weather condition
                        points = lookupCardStrength(card, card_database)
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p2_ranged_tight_bond_dict[card] * points  # add card strength
                        if p2_ranged_horn == True:
                            points = 2 * points
                p2_ranged_score += points

            for card in p2_siege_line[:]:  # check for commander horn in player melee row
                if p2_siege_horn == True and card == 'commander horn':
                    p2_siege_line.remove('commander horn')  # remove horn if there is more than 1
                if card == 'commander horn':
                    p2_siege_horn = True
            p2_siege_line.sort()
            for card in p2_siege_line:  # look through played melee line cards
                points = 0
                for card_info in card_database:  # match the melee card to its database entry
                    if card_info[
                       :len(
                           card)] == card and card != 'commander horn' and torrential_rain == True:  # weather condition
                        points = 1
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p2_siege_tight_bond_dict[card] * points  # add card strength
                        if p2_siege_horn == True:
                            points = 2 * points

                    elif card_info[
                         :len(
                             card)] == card and card != 'commander horn' and torrential_rain == False:  # no weather condition
                        points = lookupCardStrength(card, card_database)
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p2_siege_tight_bond_dict[card] * points  # add card strength
                        if p2_siege_horn == True:
                            points = 2 * points
                p2_siege_score += points

            p2_round_score = p2_melee_score + p2_ranged_score + p2_siege_score

            # print('======================================================')
            # print('player 1 siege line:  %s' % p1_siege_line)
            # print('player 1 ranged line: %s' % p1_ranged_line)
            # print('player 1 melee line:  %s' % p1_melee_line)
            # print('\n')
            # print('player 2 melee line:  %s' % p2_melee_line)
            # print('player 2 ranged line: %s' % p2_ranged_line)
            # print('player 2 siege line:  %s' % p2_siege_line)
            # print('======================================================')
            #
            # print('Current Weather:  %s' % weather)
            # print('Player 1 Score: %s' % p1_round_score)
            # print('Player 2 Score: %s' % p2_round_score)
            # print('\n')

            self.emit(SIGNAL('getP1Hand(QStringList)'), p1_hand)
            self.emit(SIGNAL('getP2Hand(QStringList)'), p2_hand)
            self.emit(SIGNAL('getP1MeleeLine(QStringList)'), p1_melee_line)
            self.emit(SIGNAL('getP1RangedLine(QStringList)'), p1_ranged_line)
            self.emit(SIGNAL('getP1SiegeLine(QStringList)'), p1_siege_line)
            self.emit(SIGNAL('getP2MeleeLine(QStringList)'), p2_melee_line)
            self.emit(SIGNAL('getP2RangedLine(QStringList)'), p2_ranged_line)
            self.emit(SIGNAL('getP2SiegeLine(QStringList)'), p2_siege_line)
            self.emit(SIGNAL('getWeather(QStringList)'), weather)
            self.emit(SIGNAL('getP1RoundScore(int)'), p1_round_score)
            self.emit(SIGNAL('getP2RoundScore(int)'), p2_round_score)
            self.emit(SIGNAL('getP1MeleeScore(int)'), p1_melee_score)
            self.emit(SIGNAL('getP1RangedScore(int)'), p1_ranged_score)
            self.emit(SIGNAL('getP1SiegeScore(int)'), p1_siege_score)
            self.emit(SIGNAL('getP2MeleeScore(int)'), p2_melee_score)
            self.emit(SIGNAL('getP2RangedScore(int)'), p2_ranged_score)
            self.emit(SIGNAL('getP2SiegeScore(int)'), p2_siege_score)

            return (p1_round_score, p2_round_score, weather, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line,
                    p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)

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
                    played_card = input(
                        'PLAYER %s:  That card is not in your hand. What card would you like to play:  ' % player_number)
            return played_card

        def getDecoyList(melee_line, ranged_line, siege_line):
            return melee_line + ranged_line + siege_line

        def scorch(card_database, p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line, p1_siege_line,
                   p2_melee_line, p2_ranged_line, p2_siege_line):
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

            return (p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line,
                    p2_ranged_line, p2_siege_line)

        def revive(player_turn, card_database, p1_hand, p2_hand, p1_deck, p2_deck, p1_discard_pile, p2_discard_pile,
                   p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line):
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
                            revive_card = input(
                                'PLAYER %s: Invalid card. What card would you like to revive:  ' % player_turn)

                    # determine requested card's line
                    revive_card_line = lookupCardType(revive_card, card_database)

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
                        scorched_cards = scorch(card_database, p1_discard_pile, p2_discard_pile, p1_melee_line,
                                                p1_ranged_line,
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
                        boosted_action = moraleBoost(revive_card, card_database, player_turn, p1_melee_line,
                                                     p1_ranged_line,
                                                     p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                        p1_melee_line = boosted_action[0]
                        p1_ranged_line = boosted_action[1]
                        p1_siege_line = boosted_action[2]
                        p2_melee_line = boosted_action[3]
                        p2_ranged_line = boosted_action[4]
                        p2_siege_line = boosted_action[5]

                    if card_ability == 'spy':
                        # prevent from being placed in current player line
                        spy_action = spy(revive_card, revive_card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck,
                                         p1_melee_line,
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
                        muster_action = muster(revive_card, revive_card_line, player_turn, p1_hand, p2_hand, p1_deck,
                                               p2_deck,
                                               p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line,
                                               p2_ranged_line,
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
                        agility_action = agility(revive_card, revive_card_line, player_turn, p1_hand, p2_hand, p1_deck,
                                                 p2_deck,
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

            return (p1_hand, p2_hand, p1_deck, p2_deck, p1_discard_pile, p2_discard_pile, p1_melee_line, p1_ranged_line,
                    p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)

        def spy(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line,
                p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line):
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

            return (p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line,
                    p2_ranged_line, p2_siege_line)

        def moraleBoost(played_card, card_database, player_turn, p1_melee_line, p1_ranged_line, p1_siege_line,
                        p2_melee_line, p2_ranged_line, p2_siege_line):
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
            return (p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)

        def muster(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line,
                   p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line):
            removed_from_hand = False  # used to add 1 version of the card back into hand so the mainloop removal works correctly

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

                if removed_from_hand == True:  # add card back into hand for mainloop card removal
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
            return (p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line,
                    p2_ranged_line, p2_siege_line)

        def agility(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line,
                    p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line):
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

            return (p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line,
                    p2_ranged_line, p2_siege_line)

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

            return (card_database)

        card_database = loadCardDatabase('card_database.txt')

        def loadDeck(deck_name):  # loads in a text file deck
            player_deck = []
            imported_deck = open(deck_name, "r")  # load player deck from text file

            for card in imported_deck:  # remove carriage returns from card names
                if card[len(card) - 1:len(card)] == '\n':
                    clean_card = card[:len(card) - 1]
                    player_deck.append(clean_card)
                else:
                    player_deck.append(card)
            imported_deck.close()  # close text file

            # check to make sure deck size is correct

            random.shuffle(player_deck)  # shuffle deck

            player_hand = player_deck[:10]  # create player hand
            player_deck = player_deck[10:]  # remove cards in player hand from top of deck
            player_hand.sort()  # alphabetically sort hand

            return (player_deck, player_hand)
        # get list of decks
        cwd = os.getcwd()           # get current directory
        fileList = os.listdir(cwd)  # create fileList of current directory
        deckList = [x[0:len(x)-5] for x in fileList if x[len(x)-5:len(x)] == '.deck']   # make list only have decks in it

        # p1 chooses
        print('Available decks:  %s' % deckList)
        print('\n')
        deckName = input('PLAYER 1: Select deck to use:  ')
        deckNameValid = False

        while deckNameValid == False:
            for deck in deckList:
                if deckName == deck:
                    deckNameValid = True
            if deckNameValid == False:
                deckName = input('PLAYER 1: Invalid deck name. Select deck to use:  ')

        loaded_deck = loadDeck(deckName + '.deck')
        p1_deck = loaded_deck[0]
        p1_hand = loaded_deck[1]

        clearScreen()

        # p2 chooses
        print('Available decks:  %s' % deckList)
        print('\n')
        deckName = input('PLAYER 2: Select deck to use:  ')
        deckNameValid = False

        while deckNameValid == False:
            for deck in deckList:
                if deckName == deck:
                    deckNameValid = True
            if deckNameValid == False:
                deckName = input('PLAYER 2: Invalid deck name. Select deck to use:  ')

        loaded_deck = loadDeck(deckName + '.deck')
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
                if player_number == 1:
                    self.emit(SIGNAL('getP1Hand(QStringList)'), player_hand)
                elif player_number == 2:
                    self.emit(SIGNAL('getP2Hand(QStringList)'), player_hand)
                replaced_card = input(
                    'PLAYER %s:  Enter which card you would like to replace or type \'pass\' to keep cards:  ' % player_number)
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
                            del (player_deck[0])

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
            return (player_hand, player_deck)

        player_turn = 1
        self.emit(SIGNAL('getP1Hand(QStringList)'), [])
        input('Press ENTER for player 1 to choose hand  ')
        self.emit(SIGNAL('getPlayerTurn(int)'), player_turn)
        p1_redraw = drawNewCards(p1_hand, p1_deck, player_turn)
        p1_hand = p1_redraw[0]
        p1_deck = p1_redraw[1]
        p1_discard_pile = []

        # create pause between player 1 and 2 (so can't see hand)
        self.emit(SIGNAL('getP1Hand(QStringList)'), [])
        input('Press ENTER for player 2 to choose hand  ')

        player_turn = 2
        self.emit(SIGNAL('getPlayerTurn(int)'), player_turn)
        p2_redraw = drawNewCards(p2_hand, p2_deck, player_turn)
        p2_hand = p2_redraw[0]
        p2_deck = p2_redraw[1]
        p2_discard_pile = []

        # create pause between choosing cards and start of game
        self.emit(SIGNAL('getP2Hand(QStringList)'), [])
        player_turn = random.randint(1, 2)  # determine player who goes first
        input('Player %s will go first. Press ENTER to start game  ' % player_turn)
        self.emit(SIGNAL('getPlayerTurn(int)'), player_turn)

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

        p1_pass = False
        p2_pass = False

        # update board and scores
        clearScreen()
        update_action = updateBoard(card_database, weather, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line,
                                    p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
        p1_round_score = update_action[0]
        p2_round_score = update_action[1]
        weather = update_action[2]
        p1_hand = update_action[3]
        p2_hand = update_action[4]
        p1_deck = update_action[5]
        p2_deck = update_action[6]
        p1_melee_line = update_action[7]
        p1_ranged_line = update_action[8]
        p1_siege_line = update_action[9]
        p2_melee_line = update_action[10]
        p2_ranged_line = update_action[11]
        p2_siege_line = update_action[12]

        # =================== Start of Game ======================
        while (p1_games_won < 2) and (p2_games_won < 2) and (games_complete < 3):
            if player_turn == 1:
                self.emit(SIGNAL('getPlayerTurn(int)'), player_turn)
                # player 1 takes turn
                if len(p1_hand) == 0:
                    p1_pass = True
                elif p1_pass == False:
                    self.emit(SIGNAL('getP1Hand(QStringList)'), p1_hand)
                    print('Player 1 hand:')
                    print(p1_hand)
                    print('\n')
                    played_card = input(
                        'PLAYER 1:  Enter which card you would like to play or type \'pass\' to end turn:  ')
                    if played_card == 'pass':
                        p1_pass = True
                        input('Enter anything for Player 2 to take turn.  ')
                    else:
                        played_card = checkCardInHand(played_card, p1_hand, 1)  # check if played card is in hand

                        # make sure decoy can be played
                        while (played_card == 'decoy' and (p1_melee_line + p1_ranged_line + p1_siege_line) == []):
                            played_card = input('PLAYER 1:  No cards to decoy. Pick card to play:  ')
                            played_card = checkCardInHand(played_card, p1_hand, 1)  # make player pick new card

                        # play played_card
                        card_line = lookupCardType(played_card, card_database)

                        # check for abilities
                        card_ability = lookupCardAbility(played_card, card_database)
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
                            scorched_cards = scorch(card_database, p1_discard_pile, p2_discard_pile, p1_melee_line,
                                                    p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line,
                                                    p2_siege_line)
                            p1_discard_pile = scorched_cards[0]
                            p2_discard_pile = scorched_cards[1]
                            p1_melee_line = scorched_cards[2]
                            p1_ranged_line = scorched_cards[3]
                            p1_siege_line = scorched_cards[4]
                            p2_melee_line = scorched_cards[5]
                            p2_ranged_line = scorched_cards[6]
                            p2_siege_line = scorched_cards[7]

                        if card_ability == 'morale boost':
                            boosted_action = moraleBoost(played_card, card_database, player_turn, p1_melee_line,
                                                         p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line,
                                                         p2_siege_line)
                            p1_melee_line = boosted_action[0]
                            p1_ranged_line = boosted_action[1]
                            p1_siege_line = boosted_action[2]
                            p2_melee_line = boosted_action[3]
                            p2_ranged_line = boosted_action[4]
                            p2_siege_line = boosted_action[5]

                        if card_ability == 'spy':
                            # prevent from being placed in current player line
                            spy_action = spy(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck,
                                             p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line,
                                             p2_ranged_line, p2_siege_line)
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
                            muster_action = muster(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck,
                                                   p2_deck,
                                                   p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line,
                                                   p2_ranged_line,
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
                            agility_action = agility(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck,
                                                     p2_deck,
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
                                    horn_line = input('PLAYER 1:  What line do you want to empower?:  ')
                                    while valid_line == False:
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
                                            horn_line = input(
                                                'PLAYER 1:  Not valid line. What line do you want to empower?:  ')
                                elif played_card == 'biting frost':
                                    if checkWeather(
                                            'biting frost') == False:  # check if the weather card was already in play
                                        weather.append(played_card)
                                        if len(weather) == 3:
                                            weather = weather[1:3]
                                elif played_card == 'impenetrable fog':
                                    if checkWeather(
                                            'impenetrable fog') == False:  # check if the weather card was already in play
                                        weather.append(played_card)
                                        if len(weather) == 3:
                                            weather = weather[1:3]
                                elif played_card == 'torrential rain':
                                    if checkWeather(
                                            'torrential rain') == False:  # check if the weather card was already in play
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
                                    return_card = input('PLAYER 1:  Enter which card you would like to return:  ')
                                    valid_return_card = False
                                    while valid_return_card == False:
                                        for i in (p1_melee_line + p1_ranged_line + p1_siege_line):
                                            if i == return_card:
                                                print(i)
                                                valid_return_card = True
                                                break
                                        if valid_return_card == False:
                                            return_card = input(
                                                'PLAYER 1:  Not valid. Enter which card you would like to return:  ')
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
                            self.emit(SIGNAL('getP1Hand(QStringList)'), [])
                            input('Enter anything for Player 2 to take turn.  ')

                # update board and scores
                clearScreen()
                update_action = updateBoard(card_database, weather, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line,
                                            p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                p1_round_score = update_action[0]
                p2_round_score = update_action[1]
                weather = update_action[2]
                p1_hand = update_action[3]
                p2_hand = update_action[4]
                p1_deck = update_action[5]
                p2_deck = update_action[6]
                p1_melee_line = update_action[7]
                p1_ranged_line = update_action[8]
                p1_siege_line = update_action[9]
                p2_melee_line = update_action[10]
                p2_ranged_line = update_action[11]
                p2_siege_line = update_action[12]
                player_turn = 2

            if player_turn == 2:
                self.emit(SIGNAL('getPlayerTurn(int)'), player_turn)
                # player 2 takes turn
                if len(p2_hand) == 0:
                    p2_pass = True
                elif p2_pass == False:
                    print('Player 2 hand:')
                    self.emit(SIGNAL('getP2Hand(QStringList)'), p2_hand)
                    print(p2_hand)
                    print('\n')
                    played_card = input(
                        'PLAYER 2:  Enter which card you would like to play or type \'pass\' to end turn:  ')
                    if played_card == 'pass':
                        p2_pass = True
                        input('Enter anything for Player 1 to take turn.  ')
                    else:
                        played_card = checkCardInHand(played_card, p2_hand, 2)  # check if played card is in hand

                        # make sure decoy can be played
                        while (played_card == 'decoy' and (p2_melee_line + p2_ranged_line + p2_siege_line) == []):
                            played_card = input('PLAYER 2:  No cards to decoy. Pick card to play:  ')
                            played_card = checkCardInHand(played_card, p2_hand, 2)  # make player pick new card

                        # play played_card
                        card_line = lookupCardType(played_card, card_database)

                        # check for abilities
                        card_ability = lookupCardAbility(played_card, card_database)
                        play_card_as_normal = True

                        if card_ability == 'revive':
                            # p2_discard_pile = revive(p2_discard_pile, 2, card_database)
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
                            scorched_cards = scorch(card_database, p1_discard_pile, p2_discard_pile, p1_melee_line,
                                                    p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line,
                                                    p2_siege_line)
                            p1_discard_pile = scorched_cards[0]
                            p2_discard_pile = scorched_cards[1]
                            p1_melee_line = scorched_cards[2]
                            p1_ranged_line = scorched_cards[3]
                            p1_siege_line = scorched_cards[4]
                            p2_melee_line = scorched_cards[5]
                            p2_ranged_line = scorched_cards[6]
                            p2_siege_line = scorched_cards[7]

                        if card_ability == 'morale boost':
                            boosted_action = moraleBoost(played_card, card_database, player_turn, p1_melee_line,
                                                         p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line,
                                                         p2_siege_line)
                            p1_melee_line = boosted_action[0]
                            p1_ranged_line = boosted_action[1]
                            p1_siege_line = boosted_action[2]
                            p2_melee_line = boosted_action[3]
                            p2_ranged_line = boosted_action[4]
                            p2_siege_line = boosted_action[5]

                        if card_ability == 'spy':
                            # prevent from being placed in current player line
                            spy_action = spy(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck, p2_deck,
                                             p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line,
                                             p2_ranged_line, p2_siege_line)
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
                            muster_action = muster(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck,
                                                   p2_deck,
                                                   p1_melee_line, p1_ranged_line, p1_siege_line, p2_melee_line,
                                                   p2_ranged_line,
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
                            agility_action = agility(played_card, card_line, player_turn, p1_hand, p2_hand, p1_deck,
                                                     p2_deck,
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
                                    horn_line = input('PLAYER 2:  What line do you want to empower?:  ')
                                    while valid_line == False:
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
                                            horn_line = input(
                                                'PLAYER 2:  Not valid line. What line do you want to empower?:  ')
                                elif played_card == 'biting frost':
                                    if checkWeather(
                                            'biting frost') == False:  # check if the weather card was already in play
                                        weather.append(played_card)
                                        if len(weather) == 3:
                                            weather = weather[1:3]
                                elif played_card == 'impenetrable fog':
                                    if checkWeather(
                                            'impenetrable fog') == False:  # check if the weather card was already in play
                                        weather.append(played_card)
                                        if len(weather) == 3:
                                            weather = weather[1:3]
                                elif played_card == 'torrential rain':
                                    if checkWeather(
                                            'torrential rain') == False:  # check if the weather card was already in play
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
                                    return_card = input('PLAYER 2:  Enter which card you would like to return:  ')
                                    valid_return_card = False
                                    while valid_return_card == False:
                                        for i in (p2_melee_line + p2_ranged_line + p2_siege_line):
                                            if i == return_card:
                                                print(i)
                                                valid_return_card = True
                                                break
                                        if valid_return_card == False:
                                            return_card = input(
                                                'PLAYER 2:  Not valid. Enter which card you would like to return:  ')
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
                            self.emit(SIGNAL('getP2Hand(QStringList)'), [])
                            input('Enter anything for Player 1 to take turn.  ')

                # update board and scores
                clearScreen()
                update_action = updateBoard(card_database, weather, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line,
                                            p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                p1_round_score = update_action[0]
                p2_round_score = update_action[1]
                weather = update_action[2]
                p1_hand = update_action[3]
                p2_hand = update_action[4]
                p1_deck = update_action[5]
                p2_deck = update_action[6]
                p1_melee_line = update_action[7]
                p1_ranged_line = update_action[8]
                p1_siege_line = update_action[9]
                p2_melee_line = update_action[10]
                p2_ranged_line = update_action[11]
                p2_siege_line = update_action[12]
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
                    player_turn = random.randint(1, 2)
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

                # update board and scores
                clearScreen()
                update_action = updateBoard(card_database, weather, p1_hand, p2_hand, p1_deck, p2_deck, p1_melee_line,
                                            p1_ranged_line, p1_siege_line, p2_melee_line, p2_ranged_line, p2_siege_line)
                p1_round_score = update_action[0]
                p2_round_score = update_action[1]
                weather = update_action[2]
                p1_hand = update_action[3]
                p2_hand = update_action[4]
                p1_deck = update_action[5]
                p2_deck = update_action[6]
                p1_melee_line = update_action[7]
                p1_ranged_line = update_action[8]
                p1_siege_line = update_action[9]
                p2_melee_line = update_action[10]
                p2_ranged_line = update_action[11]
                p2_siege_line = update_action[12]

        clearScreen()
        # count who has more wins
        if p1_games_won > p2_games_won:
            print('Player 1 Wins!')
        elif p2_games_won > p1_games_won:
            print('Player 2 Wins!')
        else:
            print('It is a tie!')

class mainWindow(QtGui.QMainWindow, board.Ui_MainWindow):   # main thread
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.player_turn = 0
        self.game = playGame()   # create game thread
        self.game.start()        # start game thread

        # Set the background image
        palette = QtGui.QPalette()
        backgroundImage = 'images/background.jpg'
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap(backgroundImage)))
        self.setPalette(palette)

        # checking player turn
        self.connect(self.game, SIGNAL('getPlayerTurn(int)'), self.getPlayerTurn)

        # drawing player hands
        self.connect(self.game, SIGNAL('getP1Hand(QStringList)'), self.drawCurrentP1Hand)
        self.connect(self.game, SIGNAL('getP2Hand(QStringList)'), self.drawCurrentP2Hand)

        # drawing played cards
        self.connect(self.game, SIGNAL('getP1MeleeLine(QStringList)'), self.drawCurrentP1MeleeLine)
        self.connect(self.game, SIGNAL('getP1RangedLine(QStringList)'), self.drawCurrentP1RangedLine)
        self.connect(self.game, SIGNAL('getP1SiegeLine(QStringList)'), self.drawCurrentP1SiegeLine)
        self.connect(self.game, SIGNAL('getP2MeleeLine(QStringList)'), self.drawCurrentP2MeleeLine)
        self.connect(self.game, SIGNAL('getP2RangedLine(QStringList)'), self.drawCurrentP2RangedLine)
        self.connect(self.game, SIGNAL('getP2SiegeLine(QStringList)'), self.drawCurrentP2SiegeLine)

        # drawing weather cards
        self.connect(self.game, SIGNAL('getWeather(QStringList)'), self.drawWeather)

        # drawing scores
        self.connect(self.game, SIGNAL('getP1RoundScore(int)'), self.drawCurrentP1RoundScore)
        self.connect(self.game, SIGNAL('getP2RoundScore(int)'), self.drawCurrentP2RoundScore)
        self.connect(self.game, SIGNAL('getP1MeleeScore(int)'), self.drawCurrentP1MeleeScore)
        self.connect(self.game, SIGNAL('getP1RangedScore(int)'), self.drawCurrentP1RangedScore)
        self.connect(self.game, SIGNAL('getP1SiegeScore(int)'), self.drawCurrentP1SiegeScore)
        self.connect(self.game, SIGNAL('getP2MeleeScore(int)'), self.drawCurrentP2MeleeScore)
        self.connect(self.game, SIGNAL('getP2RangedScore(int)'), self.drawCurrentP2RangedScore)
        self.connect(self.game, SIGNAL('getP2SiegeScore(int)'), self.drawCurrentP2SiegeScore)


    def getPlayerTurn(self, player_turn):
        self.player_turn = player_turn

    def drawCurrentP1RoundScore(self, p1_round_score):
        self.p1_score_text.setText(str(p1_round_score))

    def drawCurrentP2RoundScore(self, p2_round_score):
        self.p2_score_text.setText(str(p2_round_score))

    def drawCurrentP1MeleeScore(self, p1_melee_score):
        self.p1_melee_score_text.setText(str(p1_melee_score))

    def drawCurrentP1RangedScore(self, p1_ranged_score):
        self.p1_ranged_score_text.setText(str(p1_ranged_score))

    def drawCurrentP1SiegeScore(self, p1_siege_score):
        self.p1_siege_score_text.setText(str(p1_siege_score))

    def drawCurrentP2MeleeScore(self, p2_melee_score):
        self.p2_melee_score_text.setText(str(p2_melee_score))

    def drawCurrentP2RangedScore(self, p2_ranged_score):
        self.p2_ranged_score_text.setText(str(p2_ranged_score))

    def drawCurrentP2SiegeScore(self, p2_siege_score):
        self.p2_siege_score_text.setText(str(p2_siege_score))

    def drawWeather(self, weather):
        weatherSize = len(weather)

        if weatherSize > 0:
            self.weather_1.setPixmap(QtGui.QPixmap('images/' + weather[0] + '.jpg'))
        else:
            self.weather_1.setPixmap(QtGui.QPixmap('images/blank.jpg'))
        if weatherSize > 1:
            self.weather_2.setPixmap(QtGui.QPixmap('images/' + weather[1] + '.jpg'))
        else:
            self.weather_2.setPixmap(QtGui.QPixmap('images/blank.jpg'))

    def drawCurrentP1Hand(self, p1_hand):
        if self.player_turn == 1:

            handSize = len(p1_hand)

            if handSize > 0:
                self.hand_1.setPixmap(QtGui.QPixmap('images/' + p1_hand[0] + '.jpg'))
                self.hand_1.show()
            else:
                # self.hand_1.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_1.hide()

            if handSize > 1:
                self.hand_2.setPixmap(QtGui.QPixmap('images/' + p1_hand[1] + '.jpg'))
                self.hand_2.show()
            else:
                # self.hand_2.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_2.hide()

            if handSize > 2:
                self.hand_3.setPixmap(QtGui.QPixmap('images/' + p1_hand[2] + '.jpg'))
                self.hand_3.show()
            else:
                # self.hand_3.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_3.hide()

            if handSize > 3:
                self.hand_4.setPixmap(QtGui.QPixmap('images/' + p1_hand[3] + '.jpg'))
                self.hand_4.show()
            else:
                # self.hand_4.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_4.hide()

            if handSize > 4:
                self.hand_5.setPixmap(QtGui.QPixmap('images/' + p1_hand[4] + '.jpg'))
                self.hand_5.show()
            else:
                # self.hand_5.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_5.hide()

            if handSize > 5:
                self.hand_6.setPixmap(QtGui.QPixmap('images/' + p1_hand[5] + '.jpg'))
                self.hand_6.show()
            else:
                # self.hand_6.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_6.hide()

            if handSize > 6:
                self.hand_7.setPixmap(QtGui.QPixmap('images/' + p1_hand[6] + '.jpg'))
                self.hand_7.show()
            else:
                # self.hand_7.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_7.hide()

            if handSize > 7:
                self.hand_8.setPixmap(QtGui.QPixmap('images/' + p1_hand[7] + '.jpg'))
                self.hand_8.show()
            else:
                # self.hand_8.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_8.hide()

            if handSize > 8:
                self.hand_9.setPixmap(QtGui.QPixmap('images/' + p1_hand[8] + '.jpg'))
                self.hand_9.show()
            else:
                # self.hand_9.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_9.hide()

            if handSize > 9:
                self.hand_10.setPixmap(QtGui.QPixmap('images/' + p1_hand[9] + '.jpg'))
                self.hand_10.show()
            else:
                # self.hand_10.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_10.hide()

            if handSize > 10:
                self.hand_11.setPixmap(QtGui.QPixmap('images/' + p1_hand[10] + '.jpg'))
                self.hand_11.show()
            else:
                # self.hand_11.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_11.hide()

            if handSize > 11:
                self.hand_12.setPixmap(QtGui.QPixmap('images/' + p1_hand[11] + '.jpg'))
                self.hand_12.show()
            else:
                # self.hand_12.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_12.hide()

            if handSize > 12:
                self.hand_13.setPixmap(QtGui.QPixmap('images/' + p1_hand[12] + '.jpg'))
                self.hand_13.show()
            else:
                # self.hand_13.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_13.hide()

            if handSize > 13:
                self.hand_14.setPixmap(QtGui.QPixmap('images/' + p1_hand[13] + '.jpg'))
                self.hand_14.show()
            else:
                # self.hand_14.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_14.hide()

            if handSize > 14:
                self.hand_15.setPixmap(QtGui.QPixmap('images/' + p1_hand[14] + '.jpg'))
                self.hand_15.show()
            else:
                #self.hand_15.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_15.hide()

    def drawCurrentP2Hand(self, p2_hand):
        if self.player_turn == 2:

            handSize = len(p2_hand)

            if handSize > 0:
                self.hand_1.setPixmap(QtGui.QPixmap('images/' + p2_hand[0] + '.jpg'))
                self.hand_1.show()
            else:
                # self.hand_1.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_1.hide()

            if handSize > 1:
                self.hand_2.setPixmap(QtGui.QPixmap('images/' + p2_hand[1] + '.jpg'))
                self.hand_2.show()
            else:
                # self.hand_2.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_2.hide()

            if handSize > 2:
                self.hand_3.setPixmap(QtGui.QPixmap('images/' + p2_hand[2] + '.jpg'))
                self.hand_3.show()
            else:
                # self.hand_3.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_3.hide()

            if handSize > 3:
                self.hand_4.setPixmap(QtGui.QPixmap('images/' + p2_hand[3] + '.jpg'))
                self.hand_4.show()
            else:
                # self.hand_4.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_4.hide()

            if handSize > 4:
                self.hand_5.setPixmap(QtGui.QPixmap('images/' + p2_hand[4] + '.jpg'))
                self.hand_5.show()
            else:
                # self.hand_5.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_5.hide()

            if handSize > 5:
                self.hand_6.setPixmap(QtGui.QPixmap('images/' + p2_hand[5] + '.jpg'))
                self.hand_6.show()
            else:
                # self.hand_6.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_6.hide()

            if handSize > 6:
                self.hand_7.setPixmap(QtGui.QPixmap('images/' + p2_hand[6] + '.jpg'))
                self.hand_7.show()
            else:
                # self.hand_7.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_7.hide()

            if handSize > 7:
                self.hand_8.setPixmap(QtGui.QPixmap('images/' + p2_hand[7] + '.jpg'))
                self.hand_8.show()
            else:
                # self.hand_8.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_8.hide()

            if handSize > 8:
                self.hand_9.setPixmap(QtGui.QPixmap('images/' + p2_hand[8] + '.jpg'))
                self.hand_9.show()
            else:
                # self.hand_9.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_9.hide()

            if handSize > 9:
                self.hand_10.setPixmap(QtGui.QPixmap('images/' + p2_hand[9] + '.jpg'))
                self.hand_10.show()
            else:
                # self.hand_10.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_10.hide()

            if handSize > 10:
                self.hand_11.setPixmap(QtGui.QPixmap('images/' + p2_hand[10] + '.jpg'))
                self.hand_11.show()
            else:
                # self.hand_11.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_11.hide()

            if handSize > 11:
                self.hand_12.setPixmap(QtGui.QPixmap('images/' + p2_hand[11] + '.jpg'))
                self.hand_12.show()
            else:
                # self.hand_12.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_12.hide()

            if handSize > 12:
                self.hand_13.setPixmap(QtGui.QPixmap('images/' + p2_hand[12] + '.jpg'))
                self.hand_13.show()
            else:
                # self.hand_13.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_13.hide()

            if handSize > 13:
                self.hand_14.setPixmap(QtGui.QPixmap('images/' + p2_hand[13] + '.jpg'))
                self.hand_14.show()
            else:
                # self.hand_14.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_14.hide()

            if handSize > 14:
                self.hand_15.setPixmap(QtGui.QPixmap('images/' + p2_hand[14] + '.jpg'))
                self.hand_15.show()
            else:
                # self.hand_15.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))
                self.hand_15.hide()

    def drawCurrentP1MeleeLine(self, p1_melee_line):
        p1_melee_line_size = len(p1_melee_line)

        if p1_melee_line_size > 0:
            self.p1_melee_row1.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[0] + '.jpg'))
        else:
            self.p1_melee_row1.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_melee_line_size > 1:
            self.p1_melee_row2.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[1] + '.jpg'))
        else:
            self.p1_melee_row2.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_melee_line_size > 2:
            self.p1_melee_row3.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[2] + '.jpg'))
        else:
            self.p1_melee_row3.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_melee_line_size > 3:
            self.p1_melee_row4.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[3] + '.jpg'))
        else:
            self.p1_melee_row4.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_melee_line_size > 4:
            self.p1_melee_row5.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[4] + '.jpg'))
        else:
            self.p1_melee_row5.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_melee_line_size > 5:
            self.p1_melee_row6.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[5] + '.jpg'))
        else:
            self.p1_melee_row6.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_melee_line_size > 6:
            self.p1_melee_row7.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[6] + '.jpg'))
        else:
            self.p1_melee_row7.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_melee_line_size > 7:
            self.p1_melee_row8.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[7] + '.jpg'))
        else:
            self.p1_melee_row8.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_melee_line_size > 8:
            self.p1_melee_row9.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[8] + '.jpg'))
        else:
            self.p1_melee_row9.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_melee_line_size > 9:
            self.p1_melee_row10.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[9] + '.jpg'))
        else:
            self.p1_melee_row10.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_melee_line_size > 10:
            self.p1_melee_row11.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[10] + '.jpg'))
        else:
            self.p1_melee_row11.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_melee_line_size > 11:
            self.p1_melee_row12.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[11] + '.jpg'))
        else:
            self.p1_melee_row12.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_melee_line_size > 12:
            self.p1_melee_row13.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[12] + '.jpg'))
        else:
            self.p1_melee_row13.setPixmap(QtGui.QPixmap('blank.jpg'))

        if p1_melee_line_size > 13:
            self.p1_melee_row14.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[13] + '.jpg'))
        else:
            self.p1_melee_row14.setPixmap(QtGui.QPixmap('blank.jpg'))

        if p1_melee_line_size > 14:
            self.p1_melee_row15.setPixmap(QtGui.QPixmap('images/' + p1_melee_line[14] + '.jpg'))
        else:
            self.p1_melee_row15.setPixmap(QtGui.QPixmap('blank.jpg'))

    def drawCurrentP1RangedLine(self, p1_ranged_line):
        p1_ranged_line_size = len(p1_ranged_line)

        if p1_ranged_line_size > 0:
            self.p1_ranged_row1.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[0] + '.jpg'))
        else:
            self.p1_ranged_row1.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 1:
            self.p1_ranged_row2.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[1] + '.jpg'))
        else:
            self.p1_ranged_row2.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 2:
            self.p1_ranged_row3.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[2] + '.jpg'))
        else:
            self.p1_ranged_row3.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 3:
            self.p1_ranged_row4.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[3] + '.jpg'))
        else:
            self.p1_ranged_row4.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 4:
            self.p1_ranged_row5.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[4] + '.jpg'))
        else:
            self.p1_ranged_row5.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 5:
            self.p1_ranged_row6.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[5] + '.jpg'))
        else:
            self.p1_ranged_row6.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 6:
            self.p1_ranged_row7.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[6] + '.jpg'))
        else:
            self.p1_ranged_row7.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 7:
            self.p1_ranged_row8.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[7] + '.jpg'))
        else:
            self.p1_ranged_row8.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 8:
            self.p1_ranged_row9.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[8] + '.jpg'))
        else:
            self.p1_ranged_row9.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 9:
            self.p1_ranged_row10.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[9] + '.jpg'))
        else:
            self.p1_ranged_row10.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 10:
            self.p1_ranged_row11.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[10] + '.jpg'))
        else:
            self.p1_ranged_row11.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 11:
            self.p1_ranged_row12.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[11] + '.jpg'))
        else:
            self.p1_ranged_row12.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 12:
            self.p1_ranged_row13.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[12] + '.jpg'))
        else:
            self.p1_ranged_row13.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 13:
            self.p1_ranged_row14.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[13] + '.jpg'))
        else:
            self.p1_ranged_row14.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_ranged_line_size > 14:
            self.p1_ranged_row15.setPixmap(QtGui.QPixmap('images/' + p1_ranged_line[14] + '.jpg'))
        else:
            self.p1_ranged_row15.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

    def drawCurrentP1SiegeLine(self, p1_siege_line):
        p1_siege_line_size = len(p1_siege_line)

        if p1_siege_line_size > 0:
            self.p1_siege_row1.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[0] + '.jpg'))
        else:
            self.p1_siege_row1.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 1:
            self.p1_siege_row2.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[1] + '.jpg'))
        else:
            self.p1_siege_row2.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 2:
            self.p1_siege_row3.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[2] + '.jpg'))
        else:
            self.p1_siege_row3.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 3:
            self.p1_siege_row4.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[3] + '.jpg'))
        else:
            self.p1_siege_row4.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 4:
            self.p1_siege_row5.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[4] + '.jpg'))
        else:
            self.p1_siege_row5.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 5:
            self.p1_siege_row6.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[5] + '.jpg'))
        else:
            self.p1_siege_row6.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 6:
            self.p1_siege_row7.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[6] + '.jpg'))
        else:
            self.p1_siege_row7.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 7:
            self.p1_siege_row8.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[7] + '.jpg'))
        else:
            self.p1_siege_row8.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 8:
            self.p1_siege_row9.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[8] + '.jpg'))
        else:
            self.p1_siege_row9.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 9:
            self.p1_siege_row10.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[9] + '.jpg'))
        else:
            self.p1_siege_row10.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 10:
            self.p1_siege_row11.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[10] + '.jpg'))
        else:
            self.p1_siege_row11.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 11:
            self.p1_siege_row12.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[11] + '.jpg'))
        else:
            self.p1_siege_row12.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 12:
            self.p1_siege_row13.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[12] + '.jpg'))
        else:
            self.p1_siege_row13.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 13:
            self.p1_siege_row14.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[13] + '.jpg'))
        else:
            self.p1_siege_row14.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p1_siege_line_size > 14:
            self.p1_siege_row15.setPixmap(QtGui.QPixmap('images/' + p1_siege_line[14] + '.jpg'))
        else:
            self.p1_siege_row15.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

    def drawCurrentP2MeleeLine(self, p2_melee_line):
        p2_melee_line_size = len(p2_melee_line)

        if p2_melee_line_size > 0:
            self.p2_melee_row1.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[0] + '.jpg'))
        else:
            self.p2_melee_row1.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 1:
            self.p2_melee_row2.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[1] + '.jpg'))
        else:
            self.p2_melee_row2.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 2:
            self.p2_melee_row3.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[2] + '.jpg'))
        else:
            self.p2_melee_row3.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 3:
            self.p2_melee_row4.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[3] + '.jpg'))
        else:
            self.p2_melee_row4.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 4:
            self.p2_melee_row5.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[4] + '.jpg'))
        else:
            self.p2_melee_row5.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 5:
            self.p2_melee_row6.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[5] + '.jpg'))
        else:
            self.p2_melee_row6.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 6:
            self.p2_melee_row7.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[6] + '.jpg'))
        else:
            self.p2_melee_row7.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 7:
            self.p2_melee_row8.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[7] + '.jpg'))
        else:
            self.p2_melee_row8.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 8:
            self.p2_melee_row9.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[8] + '.jpg'))
        else:
            self.p2_melee_row9.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 9:
            self.p2_melee_row10.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[9] + '.jpg'))
        else:
            self.p2_melee_row10.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 10:
            self.p2_melee_row11.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[10] + '.jpg'))
        else:
            self.p2_melee_row11.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 11:
            self.p2_melee_row12.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[11] + '.jpg'))
        else:
            self.p2_melee_row12.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 12:
            self.p2_melee_row13.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[12] + '.jpg'))
        else:
            self.p2_melee_row13.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 13:
            self.p2_melee_row14.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[13] + '.jpg'))
        else:
            self.p2_melee_row14.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_melee_line_size > 14:
            self.p2_melee_row15.setPixmap(QtGui.QPixmap('images/' + p2_melee_line[14] + '.jpg'))
        else:
            self.p2_melee_row15.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

    def drawCurrentP2RangedLine(self, p2_ranged_line):
        p2_ranged_line_size = len(p2_ranged_line)

        if p2_ranged_line_size > 0:
            self.p2_ranged_row1.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[0] + '.jpg'))
        else:
            self.p2_ranged_row1.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 1:
            self.p2_ranged_row2.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[1] + '.jpg'))
        else:
            self.p2_ranged_row2.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 2:
            self.p2_ranged_row3.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[2] + '.jpg'))
        else:
            self.p2_ranged_row3.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 3:
            self.p2_ranged_row4.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[3] + '.jpg'))
        else:
            self.p2_ranged_row4.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 4:
            self.p2_ranged_row5.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[4] + '.jpg'))
        else:
            self.p2_ranged_row5.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 5:
            self.p2_ranged_row6.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[5] + '.jpg'))
        else:
            self.p2_ranged_row6.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 6:
            self.p2_ranged_row7.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[6] + '.jpg'))
        else:
            self.p2_ranged_row7.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 7:
            self.p2_ranged_row8.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[7] + '.jpg'))
        else:
            self.p2_ranged_row8.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 8:
            self.p2_ranged_row9.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[8] + '.jpg'))
        else:
            self.p2_ranged_row9.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 9:
            self.p2_ranged_row10.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[9] + '.jpg'))
        else:
            self.p2_ranged_row10.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 10:
            self.p2_ranged_row11.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[10] + '.jpg'))
        else:
            self.p2_ranged_row11.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 11:
            self.p2_ranged_row12.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[11] + '.jpg'))
        else:
            self.p2_ranged_row12.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 12:
            self.p2_ranged_row13.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[12] + '.jpg'))
        else:
            self.p2_ranged_row13.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 13:
            self.p2_ranged_row14.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[13] + '.jpg'))
        else:
            self.p2_ranged_row14.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_ranged_line_size > 14:
            self.p2_ranged_row15.setPixmap(QtGui.QPixmap('images/' + p2_ranged_line[14] + '.jpg'))
        else:
            self.p2_ranged_row15.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

    def drawCurrentP2SiegeLine(self, p2_siege_line):
        p2_siege_line_size = len(p2_siege_line)

        if p2_siege_line_size > 0:
            self.p2_siege_row1.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[0] + '.jpg'))
        else:
            self.p2_siege_row1.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 1:
            self.p2_siege_row2.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[1] + '.jpg'))
        else:
            self.p2_siege_row2.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 2:
            self.p2_siege_row3.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[2] + '.jpg'))
        else:
            self.p2_siege_row3.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 3:
            self.p2_siege_row4.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[3] + '.jpg'))
        else:
            self.p2_siege_row4.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 4:
            self.p2_siege_row5.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[4] + '.jpg'))
        else:
            self.p2_siege_row5.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 5:
            self.p2_siege_row6.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[5] + '.jpg'))
        else:
            self.p2_siege_row6.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 6:
            self.p2_siege_row7.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[6] + '.jpg'))
        else:
            self.p2_siege_row7.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 7:
            self.p2_siege_row8.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[7] + '.jpg'))
        else:
            self.p2_siege_row8.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 8:
            self.p2_siege_row9.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[8] + '.jpg'))
        else:
            self.p2_siege_row9.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 9:
            self.p2_siege_row10.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[9] + '.jpg'))
        else:
            self.p2_siege_row10.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 10:
            self.p2_siege_row11.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[10] + '.jpg'))
        else:
            self.p2_siege_row11.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 11:
            self.p2_siege_row12.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[11] + '.jpg'))
        else:
            self.p2_siege_row12.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 12:
            self.p2_siege_row13.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[12] + '.jpg'))
        else:
            self.p2_siege_row13.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 13:
            self.p2_siege_row14.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[13] + '.jpg'))
        else:
            self.p2_siege_row14.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

        if p2_siege_line_size > 14:
            self.p2_siege_row15.setPixmap(QtGui.QPixmap('images/' + p2_siege_line[14] + '.jpg'))
        else:
            self.p2_siege_row15.setPixmap(QtGui.QPixmap('images/' + 'blank.jpg'))

def main():
    app = QtGui.QApplication(sys.argv)
    form = mainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()                          # run the main function