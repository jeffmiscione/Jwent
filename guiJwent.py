# https://nikolak.com/pyqt-qt-designer-getting-started/
# https://www.youtube.com/watch?v=o81Q3oyz6rg
# https://nikolak.com/pyqt-threading-tutorial/

# make the ui into a .py file
# pyuic4 board.ui -o board.py

# make the resource list from the ui file into a .py
# http://stackoverflow.com/questions/15864762/pyqt4-how-do-i-compile-and-import-a-qrc-file-into-my-program
# http://stackoverflow.com/questions/15864762/pyqt4-how-do-i-compile-and-import-a-qrc-file-into-my-program

# TO DO:
# fix deckselect    (requires deck buttons)

from numbers import Number
from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL, Qt
import sys
import board       # the ui file that has been converted to python
import random
import os
import time

class playGame(QThread):
    def __init__(self):
        QThread.__init__(self)

        self.currentInput = 0

    def __del__(self):
        self.wait()

    def run(self):
        def getCardName(card_database_entry):
            index = 0
            while card_database_entry[index] != ',':
                index = index + 1

            return card_database_entry[0:index]

        def lookupCardType(card_name, card_database):
            first_comma_index = 0
            second_comma_index = 0
            third_comma_index = 0
            commas_found = 0
            description_indicator_index = 0

            for card in card_database:  # look through card database
                if getCardName(card) == card_name:  # find matching card in database
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
                if getCardName(card) == card_name:  # find matching card in database
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
                if getCardName(card) == card_name:  # find matching card in database
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
                    if getCardName(card_info) == card and card != 'commander horn' and biting_frost == True:  # weather condition
                        points = 1
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p1_melee_tight_bond_dict[card] * points  # add card strength
                        if p1_melee_horn == True:
                            points = 2 * points

                    elif getCardName(card_info) == card and card != 'commander horn' and biting_frost == False:  # no weather condition
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
                    if getCardName(card_info) == card and card != 'commander horn' and impenetrable_fog == True:  # weather condition
                        points = 1
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p1_ranged_tight_bond_dict[card] * points  # add card strength
                        if p1_ranged_horn == True:
                            points = 2 * points

                    elif getCardName(card_info) == card and card != 'commander horn' and impenetrable_fog == False:  # no weather condition
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
                    if getCardName(card_info) == card and card != 'commander horn' and torrential_rain == True:  # weather condition
                        points = 1
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p1_siege_tight_bond_dict[card] * points  # add card strength
                        if p1_siege_horn == True:
                            points = 2 * points

                    elif getCardName(card_info) == card and card != 'commander horn' and torrential_rain == False:  # no weather condition
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
                    if getCardName(card_info) == card and card != 'commander horn' and biting_frost == True:  # weather condition
                        points = 1
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p2_melee_tight_bond_dict[card] * points  # add card strength
                        if p2_melee_horn == True:
                            points = 2 * points

                    elif getCardName(card_info) == card and card != 'commander horn' and biting_frost == False:  # no weather condition
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
                    if getCardName(card_info) == card and card != 'commander horn' and impenetrable_fog == True:  # weather condition
                        points = 1
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p2_ranged_tight_bond_dict[card] * points  # add card strength
                        if p2_ranged_horn == True:
                            points = 2 * points

                    elif getCardName(card_info) == card and card != 'commander horn' and impenetrable_fog == False:  # no weather condition
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
                    if getCardName(card_info) == card and card != 'commander horn' and torrential_rain == True:  # weather condition
                        points = 1
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p2_siege_tight_bond_dict[card] * points  # add card strength
                        if p2_siege_horn == True:
                            points = 2 * points

                    elif getCardName(card_info) == card and card != 'commander horn' and torrential_rain == False:  # no weather condition
                        points = lookupCardStrength(card, card_database)
                        if lookupCardAbility(card, card_database) == 'tight bond':
                            points = p2_siege_tight_bond_dict[card] * points  # add card strength
                        if p2_siege_horn == True:
                            points = 2 * points
                p2_siege_score += points

            p2_round_score = p2_melee_score + p2_ranged_score + p2_siege_score

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
                    # display the graveyard
                    self.emit(SIGNAL('switchGrave(QStringList)'), graveyard)
                    self.emit(SIGNAL('updateGameMessage(QString)'), 'Select card to revive')

                    # ask for input of card to revive
                    revive_card = ''

                    # make sure requested card is in graveyard
                    revive_card_valid = False
                    while revive_card_valid == False:
                        self.currentInput = ''
                        while (self.currentInput == ''):
                            time.sleep(0.25)

                        if (isinstance(self.currentInput, str) == True):  # check if a string input sent
                            if(self.currentInput[0] == 'g'):  # waiting for graveyard input
                                revive_card = graveyard[int(self.currentInput[2:]) - 1]
                                revive_card_valid = True

                    # hide the graveyard
                    self.emit(SIGNAL('hideGraveyard'))

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

            self.currentInput = ''  # sets the current input to nothing in case something was clicked before
            self.emit(SIGNAL('switchMelee(QString)'), 'on')
            self.emit(SIGNAL('switchRanged(QString)'), 'on')
            self.emit(SIGNAL('updateGameMessage(QString)'), 'Choose where to place card')
            while self.currentInput == '':  # waiting for new input
                time.sleep(0.25)
            self.emit(SIGNAL('switchMelee(QString)'), 'off')
            self.emit(SIGNAL('switchRanged(QString)'), 'off')
            selected_line = self.currentInput

            #selected_line = input('PLAYER %s: melee or ranged:  ' % player_turn)
            valid_line = False
            while valid_line == False:
                if selected_line == 'melee' or selected_line == 'ranged':
                    valid_line = True
                if valid_line == False:
                    #selected_line = input('PLAYER %s: melee or ranged:  ' % player_turn)
                    self.currentInput = ''  # sets the current input to nothing in case something was clicked before
                    self.emit(SIGNAL('switchMelee(QString)'), 'on')
                    self.emit(SIGNAL('switchRanged(QString)'), 'on')
                    self.emit(SIGNAL('updateGameMessage(QString)'), 'Choose where to place card')
                    while self.currentInput == '':  # waiting for new input
                        time.sleep(0.25)
                    self.emit(SIGNAL('switchMelee(QString)'), 'off')
                    self.emit(SIGNAL('switchRanged(QString)'), 'off')
                    selected_line = self.currentInput

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

        # populate deckListBox
        time.sleep(1)
        self.emit(SIGNAL('showDecks(QStringList)'), deckList)

        self.emit(SIGNAL('updateGameMessage(QString)'), 'Player 1 select deck')
        self.currentInput = ''
        while(self.currentInput == ''):
            time.sleep(1)

        loaded_deck = loadDeck(self.currentInput + '.deck')
        p1_deck = loaded_deck[0]
        p1_hand = loaded_deck[1]


        # p2 chooses
        self.emit(SIGNAL('updateGameMessage(QString)'), 'Player 2 select deck')
        self.currentInput = ''
        while(self.currentInput == ''):
            time.sleep(1)

        loaded_deck = loadDeck(self.currentInput + '.deck')
        p2_deck = loaded_deck[0]
        p2_hand = loaded_deck[1]

        # hide the deck list
        self.emit(SIGNAL('switchDeckList(QString)'), 'off')

        # ======================= Draw New Cards =======================
        def drawNewCards(player_hand, player_deck, player_number):
            player_redraws = 2

            while player_redraws > 0:
                if player_number == 1:
                    self.emit(SIGNAL('getP1Hand(QStringList)'), player_hand)
                elif player_number == 2:
                    self.emit(SIGNAL('getP2Hand(QStringList)'), player_hand)

                self.currentInput = ''      # sets the current input to nothing in case something was clicked before
                while self.currentInput == '':  # waiting for new input
                    time.sleep(0.25)

                if self.currentInput == 'pass':     # check if player pressed the pass button
                    player_redraws = 0
                else:
                    replaced_card = player_hand[self.currentInput-1]
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
            return (player_hand, player_deck)

        player_turn = 1
        self.emit(SIGNAL('getP1Hand(QStringList)'), [])

        self.currentInput = ''  # sets the current input to nothing in case something was clicked before
        self.emit(SIGNAL('switchNext(QString)'), 'on')
        self.emit(SIGNAL('updateGameMessage(QString)'), 'Press NEXT for player 1 to choose hand')
        while self.currentInput != 'next':  # waiting for new input
            time.sleep(0.25)
        self.emit(SIGNAL('switchNext(QString)'), 'off')

        self.emit(SIGNAL('getPlayerTurn(int)'), player_turn)
        self.emit(SIGNAL('switchPass(QString)'), 'on')
        self.emit(SIGNAL('updateGameMessage(QString)'), 'Select cards to redraw or press Pass')
        p1_redraw = drawNewCards(p1_hand, p1_deck, player_turn)
        p1_hand = p1_redraw[0]
        p1_deck = p1_redraw[1]
        p1_discard_pile = []

        # create pause between player 1 and 2 (so can't see hand)
        self.emit(SIGNAL('switchPass(QString)'), 'off')
        self.emit(SIGNAL('getP1Hand(QStringList)'), [])


        self.currentInput = ''  # sets the current input to nothing in case something was clicked before
        self.emit(SIGNAL('switchNext(QString)'), 'on')
        self.emit(SIGNAL('updateGameMessage(QString)'), 'Press NEXT for player 2 to choose hand')
        while self.currentInput != 'next':  # waiting for new input
            time.sleep(0.25)
        self.emit(SIGNAL('switchNext(QString)'), 'off')

        player_turn = 2
        self.emit(SIGNAL('getPlayerTurn(int)'), player_turn)
        self.emit(SIGNAL('switchPass(QString)'), 'on')
        self.emit(SIGNAL('updateGameMessage(QString)'), 'Select cards to redraw or press Pass')
        p2_redraw = drawNewCards(p2_hand, p2_deck, player_turn)
        p2_hand = p2_redraw[0]
        p2_deck = p2_redraw[1]
        p2_discard_pile = []

        # create pause between choosing cards and start of game
        self.emit(SIGNAL('switchPass(QString)'), 'off')
        self.emit(SIGNAL('getP2Hand(QStringList)'), [])
        player_turn = random.randint(1, 2)  # determine player who goes first


        self.currentInput = ''  # sets the current input to nothing in case something was clicked before
        self.emit(SIGNAL('switchNext(QString)'), 'on')
        self.emit(SIGNAL('updateGameMessage(QString)'), 'Press NEXT for player %s to start game' % player_turn)
        while self.currentInput != 'next':  # waiting for new input
            time.sleep(0.25)
        self.emit(SIGNAL('switchNext(QString)'), 'off')

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
                self.emit(SIGNAL('updateGameMessage(QString)'), 'Player 1 play a card or press Pass')
                self.emit(SIGNAL('getPlayerTurn(int)'), player_turn)
                # player 1 takes turn
                if len(p1_hand) == 0:
                    p1_pass = True
                elif p1_pass == False:
                    self.emit(SIGNAL('getP1Hand(QStringList)'), p1_hand)
                    self.emit(SIGNAL('switchPass(QString)'), 'on')

                    # wait for input of from card
                    self.currentInput = ''  # sets the current input to nothing in case something was clicked before
                    while self.currentInput == '':  # waiting for new input
                        time.sleep(0.25)

                    if self.currentInput == 'pass':
                        p1_pass = True
                        self.emit(SIGNAL('switchPass(QString)'), 'off')
                        
                        if p2_pass == False:
                            self.currentInput = ''  # sets the current input to nothing in case something was clicked before
                            self.emit(SIGNAL('switchNext(QString)'), 'on')
                            self.emit(SIGNAL('getP1Hand(QStringList)'), [])
                            self.emit(SIGNAL('updateGameMessage(QString)'), 'Press NEXT for Player 2 to take turn')
                            while self.currentInput != 'next':  # waiting for new input
                                time.sleep(0.25)
                            self.emit(SIGNAL('switchNext(QString)'), 'off')
                    else:
                        # loop until the currentInput is a number (implying card from hand)
                        while (isinstance(self.currentInput, Number) == False):
                            time.sleep(0.25)

                        played_card = p1_hand[self.currentInput-1]
                        #played_card = checkCardInHand(played_card, p1_hand, 1)  # check if played card is in hand

                        # make sure decoy can be played
                        while (played_card == 'decoy' and (p1_melee_line + p1_ranged_line + p1_siege_line) == []):
                            self.emit(SIGNAL('updateGameMessage(QString)'), 'Cannot play Decoy')
                            self.currentInput = ''
                            while (self.currentInput == ''):  # waiting for new input
                                time.sleep(0.25)   # need to make this allow pass and prevent error on string(clicking played cards)

                            # if input is a pass
                            if (self.currentInput == 'pass'):
                                p1_pass = True
                                if p2_pass == False:
                                    self.currentInput = ''  # sets the current input to nothing in case something was clicked before
                                    self.emit(SIGNAL('switchNext(QString)'), 'on')
                                    self.emit(SIGNAL('switchNext(QString)'), 'off')
                                    self.emit(SIGNAL('getP1Hand(QStringList)'), [])
                                    self.emit(SIGNAL('updateGameMessage(QString)'),
                                              'Press NEXT for Player 2 to take turn')
                                    while self.currentInput != 'next':  # waiting for new input
                                        time.sleep(0.25)
                                    self.emit(SIGNAL('switchNext(QString)'), 'off')
                                break

                            if (isinstance(self.currentInput, Number) == True):
                                played_card = p1_hand[self.currentInput-1]

                        # if p1_pass == False: # skip these steps
                        if p1_pass == False:
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

                                        # turn on buttons to select row
                                        self.emit(SIGNAL('switchMelee(QString)'), 'on')
                                        self.emit(SIGNAL('switchRanged(QString)'), 'on')
                                        self.emit(SIGNAL('switchSiege(QString)'), 'on')

                                        self.currentInput = ''
                                        self.emit(SIGNAL('updateGameMessage(QString)'),
                                                  'Select which line to empower')
                                        while self.currentInput == '':  # waiting for new input
                                            time.sleep(0.25)

                                        self.emit(SIGNAL('switchMelee(QString)'), 'off')
                                        self.emit(SIGNAL('switchRanged(QString)'), 'off')
                                        self.emit(SIGNAL('switchSiege(QString)'), 'off')

                                        #horn_line = input('PLAYER 1:  What line do you want to empower?:  ')
                                        while valid_line == False:
                                            horn_line = self.currentInput
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
                                                self.emit(SIGNAL('switchMelee(QString)'), 'on')
                                                self.emit(SIGNAL('switchRanged(QString)'), 'on')
                                                self.emit(SIGNAL('switchSiege(QString)'), 'on')
                                                self.currentInput = ''
                                                self.emit(SIGNAL('updateGameMessage(QString)'),
                                                          'Not valid line. What line do you want to empower?')
                                                while self.currentInput == '':  # waiting for new input
                                                    time.sleep(0.25)

                                                self.emit(SIGNAL('switchMelee(QString)'), 'off')
                                                self.emit(SIGNAL('switchRanged(QString)'), 'off')
                                                self.emit(SIGNAL('switchSiege(QString)'), 'off')
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
                                        self.emit(SIGNAL('updateGameMessage(QString)'), 'Choose card to return to hand')

                                        valid_return_card = False
                                        while(valid_return_card == False):
                                            # check for a non-empty string
                                            self.currentInput = ''
                                            while(self.currentInput == ''):  # waiting for new input
                                                time.sleep(0.25)

                                            while(isinstance(self.currentInput, str) == False):
                                                time.sleep(0.25)

                                            # check it's p1 starting string
                                            if(self.currentInput[0:2] == 'p1'):
                                                valid_return_card = True
                                                if(self.currentInput[3:4] == 'm'):
                                                    return_card_line = 'melee'
                                                    return_card = p1_melee_line[int(self.currentInput[5:])-1]
                                                elif(self.currentInput[3:4] == 'r'):
                                                    return_card_line = 'ranged'
                                                    return_card = p1_ranged_line[int(self.currentInput[5:]) - 1]
                                                else:
                                                    return_card_line = 'siege'
                                                    return_card = p1_siege_line[int(self.currentInput[5:]) - 1]
                                            else:
                                                self.emit(SIGNAL('updateGameMessage(QString)'),
                                                          'Invalid selection. Choose card to return.')

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
                            self.emit(SIGNAL('switchPass(QString)'), 'off')
                            if (p2_pass == False) and (len(p2_hand) != 0):
                                self.emit(SIGNAL('getP1Hand(QStringList)'), [])
                                
                                self.currentInput = ''  # sets the current input to nothing in case something was clicked before
                                self.emit(SIGNAL('switchNext(QString)'), 'on')
                                self.emit(SIGNAL('updateGameMessage(QString)'), 'Press NEXT for player 2 to take turn')
                                while self.currentInput != 'next':  # waiting for new input
                                    time.sleep(0.25)
                                self.emit(SIGNAL('switchNext(QString)'), 'off')

                # update board and scores
                
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
                self.emit(SIGNAL('updateGameMessage(QString)'), 'Player 2 play a card or press Pass')
                self.emit(SIGNAL('getPlayerTurn(int)'), player_turn)
                # player 2 takes turn
                if len(p2_hand) == 0:
                    p2_pass = True
                elif p2_pass == False:
                    self.emit(SIGNAL('getP2Hand(QStringList)'), p2_hand)
                    self.emit(SIGNAL('switchPass(QString)'), 'on')

                    # wait for input of from card
                    self.currentInput = ''  # sets the current input to nothing in case something was clicked before
                    while self.currentInput == '':  # waiting for new input
                        time.sleep(0.25)

                    if self.currentInput == 'pass':
                        p2_pass = True
                        self.emit(SIGNAL('switchPass(QString)'), 'off')
                        
                        if p1_pass == False:
                            self.currentInput = ''  # sets the current input to nothing in case something was clicked before
                            self.emit(SIGNAL('switchNext(QString)'), 'on')
                            self.emit(SIGNAL('getP2Hand(QStringList)'), [])
                            self.emit(SIGNAL('updateGameMessage(QString)'), 'Press NEXT for Player 1 to take turn')
                            while self.currentInput != 'next':  # waiting for new input
                                time.sleep(0.25)
                            self.emit(SIGNAL('switchNext(QString)'), 'off')
                    else:
                        # loop until the currentInput is a number (implying card from hand)
                        while (isinstance(self.currentInput, Number) == False):
                            time.sleep(0.25)

                        played_card = p2_hand[self.currentInput-1]
                        #played_card = checkCardInHand(played_card, p1_hand, 1)  # check if played card is in hand

                        # make sure decoy can be played
                        while (played_card == 'decoy' and (p2_melee_line + p2_ranged_line + p2_siege_line) == []):
                            self.emit(SIGNAL('updateGameMessage(QString)'), 'Cannot play Decoy')
                            self.currentInput = ''
                            while (self.currentInput == ''):  # waiting for new input
                                time.sleep(0.25)   # need to make this allow pass and prevent error on string(clicking played cards)

                            # if input is a pass
                            if (self.currentInput == 'pass'):
                                p2_pass = True
                                if p1_pass == False:
                                    self.currentInput = ''  # sets the current input to nothing in case something was clicked before
                                    self.emit(SIGNAL('switchNext(QString)'), 'on')
                                    self.emit(SIGNAL('switchNext(QString)'), 'off')
                                    self.emit(SIGNAL('getP2Hand(QStringList)'), [])
                                    self.emit(SIGNAL('updateGameMessage(QString)'),
                                              'Press NEXT for Player 1 to take turn')
                                    while self.currentInput != 'next':  # waiting for new input
                                        time.sleep(0.25)
                                    self.emit(SIGNAL('switchNext(QString)'), 'off')
                                break

                            if (isinstance(self.currentInput, Number) == True):
                                played_card = p2_hand[self.currentInput-1]

                        # if p1_pass == False: # skip these steps
                        if p2_pass == False:
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
                                    p2_melee_line.append(played_card)
                                elif card_line == 'ranged':
                                    p2_ranged_line.append(played_card)
                                elif card_line == 'siege':
                                    p2_siege_line.append(played_card)
                                elif card_line == 'special':
                                    if played_card == 'commander horn':
                                        valid_line = False

                                        # turn on buttons to select row
                                        self.emit(SIGNAL('switchMelee(QString)'), 'on')
                                        self.emit(SIGNAL('switchRanged(QString)'), 'on')
                                        self.emit(SIGNAL('switchSiege(QString)'), 'on')

                                        self.currentInput = ''
                                        self.emit(SIGNAL('updateGameMessage(QString)'),
                                                  'Select which line to empower')
                                        while self.currentInput == '':  # waiting for new input
                                            time.sleep(0.25)

                                        self.emit(SIGNAL('switchMelee(QString)'), 'off')
                                        self.emit(SIGNAL('switchRanged(QString)'), 'off')
                                        self.emit(SIGNAL('switchSiege(QString)'), 'off')

                                        while valid_line == False:
                                            horn_line = self.currentInput
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
                                                self.emit(SIGNAL('switchMelee(QString)'), 'on')
                                                self.emit(SIGNAL('switchRanged(QString)'), 'on')
                                                self.emit(SIGNAL('switchSiege(QString)'), 'on')
                                                self.currentInput = ''
                                                self.emit(SIGNAL('updateGameMessage(QString)'),
                                                          'Not valid line. What line do you want to empower?')
                                                while self.currentInput == '':  # waiting for new input
                                                    time.sleep(0.25)

                                                self.emit(SIGNAL('switchMelee(QString)'), 'off')
                                                self.emit(SIGNAL('switchRanged(QString)'), 'off')
                                                self.emit(SIGNAL('switchSiege(QString)'), 'off')
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
                                        self.emit(SIGNAL('updateGameMessage(QString)'), 'Choose card to return to hand')

                                        valid_return_card = False
                                        while(valid_return_card == False):
                                            # check for a non-empty string
                                            self.currentInput = ''
                                            while(self.currentInput == ''):  # waiting for new input
                                                time.sleep(0.25)

                                            while(isinstance(self.currentInput, str) == False):
                                                time.sleep(0.25)

                                            # check it's p2 starting string
                                            if(self.currentInput[0:2] == 'p2'):
                                                valid_return_card = True
                                                if(self.currentInput[3:4] == 'm'):
                                                    return_card_line = 'melee'
                                                    return_card = p2_melee_line[int(self.currentInput[5:])-1]
                                                elif(self.currentInput[3:4] == 'r'):
                                                    return_card_line = 'ranged'
                                                    return_card = p2_ranged_line[int(self.currentInput[5:]) - 1]
                                                else:
                                                    return_card_line = 'siege'
                                                    return_card = p2_siege_line[int(self.currentInput[5:]) - 1]
                                            else:
                                                self.emit(SIGNAL('updateGameMessage(QString)'),
                                                          'Invalid selection. Choose card to return.')

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

                            # remove played_card from p1_hand
                            p2_hand.remove(played_card)
                            self.emit(SIGNAL('switchPass(QString)'), 'off')
                            if (p1_pass == False) and (len(p1_hand) != 0):
                                self.emit(SIGNAL('getP2Hand(QStringList)'), [])
                                
                                self.currentInput = ''  # sets the current input to nothing in case something was clicked before
                                self.emit(SIGNAL('switchNext(QString)'), 'on')
                                self.emit(SIGNAL('updateGameMessage(QString)'), 'Press NEXT for player 1 to take turn')
                                while self.currentInput != 'next':  # waiting for new input
                                    time.sleep(0.25)
                                self.emit(SIGNAL('switchNext(QString)'), 'off')

                # update board and scores
                
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
                self.emit(SIGNAL('getPlayerTurn(int)'), player_turn)
                if player_turn == 1:
                    self.emit(SIGNAL('getP1Hand(QStringList)'), [])
                elif player_turn == 2:
                    self.emit(SIGNAL('getP2Hand(QStringList)'), [])

                # increment number of played games
                games_complete += 1

                # determine who won the round
                if p1_round_score > p2_round_score:
                    p1_games_won += 1
                    player_turn = 1
                    self.emit(SIGNAL('updateGameMessage(QString)'), 'Player 1 wins the round.')
                elif p2_round_score > p1_round_score:
                    p2_games_won += 1
                    player_turn = 2
                    self.emit(SIGNAL('updateGameMessage(QString)'), 'Player 2 wins the round.')
                else:
                    player_turn = random.randint(1, 2)
                    self.emit(SIGNAL('updateGameMessage(QString)'), 'Round was a tie.')

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

                self.emit(SIGNAL('getP1RoundsWon(int)'), p1_games_won)
                self.emit(SIGNAL('getP2RoundsWon(int)'), p2_games_won)

                # end of game pause
                self.emit(SIGNAL('switchNext(QString)'), 'on')      # turn on NEXT button
                self.currentInput = ''  # sets the current input to nothing in case something was clicked before
                self.emit(SIGNAL('updateGameMessage(QString)'), 'Press NEXT for player %s to take turn ' % player_turn)
                while self.currentInput != 'next':  # waiting for new input
                    time.sleep(0.25)
                self.emit(SIGNAL('switchNext(QString)'), 'off')

        
        # count who has more wins
        if p1_games_won > p2_games_won:
            self.emit(SIGNAL('updateGameMessage(QString)'), 'Player 1 Wins!')
        elif p2_games_won > p1_games_won:
            self.emit(SIGNAL('updateGameMessage(QString)'), 'Player 2 Wins!')
        else:
            self.emit(SIGNAL('updateGameMessage(QString)'), 'Game is a draw!')

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

        # list of decks
        self.connect(self.game, SIGNAL('showDecks(QStringList)'), self.showDecks)
        self.connect(self.game, SIGNAL('switchDeckList(QString)'), self.switchDeckList)
        self.selectDeck.clicked.connect(self.sendSelectedDeck)

        # turn on/off buttons and update the messages
        self.connect(self.game, SIGNAL('switchNext(QString)'), self.switchNext)
        self.connect(self.game, SIGNAL('switchPass(QString)'), self.switchPass)
        self.connect(self.game, SIGNAL('switchGrave(QStringList)'), self.switchGrave)
        self.connect(self.game, SIGNAL('hideGraveyard'), self.hideGraveyard)
        self.connect(self.game, SIGNAL('updateGameMessage(QString)'), self.updateGameMessage)
        self.connect(self.game, SIGNAL('switchMelee(QString)'), self.switchMelee)
        self.connect(self.game, SIGNAL('switchRanged(QString)'), self.switchRanged)
        self.connect(self.game, SIGNAL('switchSiege(QString)'), self.switchSiege)

        # input from clicking on cards
        self.passButton.clicked.connect(lambda: self.updateCurrentInput('pass'))
        self.nextButton.clicked.connect(lambda: self.updateCurrentInput('next'))
        self.meleeButton.clicked.connect(lambda: self.updateCurrentInput('melee'))
        self.rangedButton.clicked.connect(lambda: self.updateCurrentInput('ranged'))
        self.siegeButton.clicked.connect(lambda: self.updateCurrentInput('siege'))

        self.hand_01.clicked.connect(lambda: self.updateCurrentInput(1))
        self.hand_02.clicked.connect(lambda: self.updateCurrentInput(2))
        self.hand_03.clicked.connect(lambda: self.updateCurrentInput(3))
        self.hand_04.clicked.connect(lambda: self.updateCurrentInput(4))
        self.hand_05.clicked.connect(lambda: self.updateCurrentInput(5))
        self.hand_06.clicked.connect(lambda: self.updateCurrentInput(6))
        self.hand_07.clicked.connect(lambda: self.updateCurrentInput(7))
        self.hand_08.clicked.connect(lambda: self.updateCurrentInput(8))
        self.hand_09.clicked.connect(lambda: self.updateCurrentInput(9))
        self.hand_10.clicked.connect(lambda: self.updateCurrentInput(10))
        self.hand_11.clicked.connect(lambda: self.updateCurrentInput(11))
        self.hand_12.clicked.connect(lambda: self.updateCurrentInput(12))
        self.hand_13.clicked.connect(lambda: self.updateCurrentInput(13))
        self.hand_14.clicked.connect(lambda: self.updateCurrentInput(14))
        self.hand_15.clicked.connect(lambda: self.updateCurrentInput(15))
        self.hand_16.clicked.connect(lambda: self.updateCurrentInput(16))
        self.hand_17.clicked.connect(lambda: self.updateCurrentInput(17))
        self.hand_18.clicked.connect(lambda: self.updateCurrentInput(18))
        self.hand_19.clicked.connect(lambda: self.updateCurrentInput(19))
        self.hand_20.clicked.connect(lambda: self.updateCurrentInput(20))

        self.p1_melee_row01.clicked.connect(lambda: self.updateCurrentInput('p1_m_01'))
        self.p1_melee_row02.clicked.connect(lambda: self.updateCurrentInput('p1_m_02'))
        self.p1_melee_row03.clicked.connect(lambda: self.updateCurrentInput('p1_m_03'))
        self.p1_melee_row04.clicked.connect(lambda: self.updateCurrentInput('p1_m_04'))
        self.p1_melee_row05.clicked.connect(lambda: self.updateCurrentInput('p1_m_05'))
        self.p1_melee_row06.clicked.connect(lambda: self.updateCurrentInput('p1_m_06'))
        self.p1_melee_row07.clicked.connect(lambda: self.updateCurrentInput('p1_m_07'))
        self.p1_melee_row08.clicked.connect(lambda: self.updateCurrentInput('p1_m_08'))
        self.p1_melee_row09.clicked.connect(lambda: self.updateCurrentInput('p1_m_09'))
        self.p1_melee_row10.clicked.connect(lambda: self.updateCurrentInput('p1_m_10'))
        self.p1_melee_row11.clicked.connect(lambda: self.updateCurrentInput('p1_m_11'))
        self.p1_melee_row12.clicked.connect(lambda: self.updateCurrentInput('p1_m_12'))
        self.p1_melee_row13.clicked.connect(lambda: self.updateCurrentInput('p1_m_13'))
        self.p1_melee_row14.clicked.connect(lambda: self.updateCurrentInput('p1_m_14'))
        self.p1_melee_row15.clicked.connect(lambda: self.updateCurrentInput('p1_m_15'))
        self.p1_melee_row16.clicked.connect(lambda: self.updateCurrentInput('p1_m_16'))
        self.p1_melee_row17.clicked.connect(lambda: self.updateCurrentInput('p1_m_17'))
        self.p1_melee_row18.clicked.connect(lambda: self.updateCurrentInput('p1_m_18'))
        self.p1_melee_row19.clicked.connect(lambda: self.updateCurrentInput('p1_m_19'))
        self.p1_melee_row20.clicked.connect(lambda: self.updateCurrentInput('p1_m_20'))

        self.p1_ranged_row01.clicked.connect(lambda: self.updateCurrentInput('p1_r_01'))
        self.p1_ranged_row02.clicked.connect(lambda: self.updateCurrentInput('p1_r_02'))
        self.p1_ranged_row03.clicked.connect(lambda: self.updateCurrentInput('p1_r_03'))
        self.p1_ranged_row04.clicked.connect(lambda: self.updateCurrentInput('p1_r_04'))
        self.p1_ranged_row05.clicked.connect(lambda: self.updateCurrentInput('p1_r_05'))
        self.p1_ranged_row06.clicked.connect(lambda: self.updateCurrentInput('p1_r_06'))
        self.p1_ranged_row07.clicked.connect(lambda: self.updateCurrentInput('p1_r_07'))
        self.p1_ranged_row08.clicked.connect(lambda: self.updateCurrentInput('p1_r_08'))
        self.p1_ranged_row09.clicked.connect(lambda: self.updateCurrentInput('p1_r_09'))
        self.p1_ranged_row10.clicked.connect(lambda: self.updateCurrentInput('p1_r_10'))
        self.p1_ranged_row11.clicked.connect(lambda: self.updateCurrentInput('p1_r_11'))
        self.p1_ranged_row12.clicked.connect(lambda: self.updateCurrentInput('p1_r_12'))
        self.p1_ranged_row13.clicked.connect(lambda: self.updateCurrentInput('p1_r_13'))
        self.p1_ranged_row14.clicked.connect(lambda: self.updateCurrentInput('p1_r_14'))
        self.p1_ranged_row15.clicked.connect(lambda: self.updateCurrentInput('p1_r_15'))
        self.p1_ranged_row16.clicked.connect(lambda: self.updateCurrentInput('p1_r_16'))
        self.p1_ranged_row17.clicked.connect(lambda: self.updateCurrentInput('p1_r_17'))
        self.p1_ranged_row18.clicked.connect(lambda: self.updateCurrentInput('p1_r_18'))
        self.p1_ranged_row19.clicked.connect(lambda: self.updateCurrentInput('p1_r_19'))
        self.p1_ranged_row20.clicked.connect(lambda: self.updateCurrentInput('p1_r_20'))

        self.p1_siege_row01.clicked.connect(lambda: self.updateCurrentInput('p1_s_01'))
        self.p1_siege_row02.clicked.connect(lambda: self.updateCurrentInput('p1_s_02'))
        self.p1_siege_row03.clicked.connect(lambda: self.updateCurrentInput('p1_s_03'))
        self.p1_siege_row04.clicked.connect(lambda: self.updateCurrentInput('p1_s_04'))
        self.p1_siege_row05.clicked.connect(lambda: self.updateCurrentInput('p1_s_05'))
        self.p1_siege_row06.clicked.connect(lambda: self.updateCurrentInput('p1_s_06'))
        self.p1_siege_row07.clicked.connect(lambda: self.updateCurrentInput('p1_s_07'))
        self.p1_siege_row08.clicked.connect(lambda: self.updateCurrentInput('p1_s_08'))
        self.p1_siege_row09.clicked.connect(lambda: self.updateCurrentInput('p1_s_09'))
        self.p1_siege_row10.clicked.connect(lambda: self.updateCurrentInput('p1_s_10'))
        self.p1_siege_row11.clicked.connect(lambda: self.updateCurrentInput('p1_s_11'))
        self.p1_siege_row12.clicked.connect(lambda: self.updateCurrentInput('p1_s_12'))
        self.p1_siege_row13.clicked.connect(lambda: self.updateCurrentInput('p1_s_13'))
        self.p1_siege_row14.clicked.connect(lambda: self.updateCurrentInput('p1_s_14'))
        self.p1_siege_row15.clicked.connect(lambda: self.updateCurrentInput('p1_s_15'))
        self.p1_siege_row16.clicked.connect(lambda: self.updateCurrentInput('p1_s_16'))
        self.p1_siege_row17.clicked.connect(lambda: self.updateCurrentInput('p1_s_17'))
        self.p1_siege_row18.clicked.connect(lambda: self.updateCurrentInput('p1_s_18'))
        self.p1_siege_row19.clicked.connect(lambda: self.updateCurrentInput('p1_s_19'))
        self.p1_siege_row20.clicked.connect(lambda: self.updateCurrentInput('p1_s_20'))

        self.p2_melee_row01.clicked.connect(lambda: self.updateCurrentInput('p2_m_01'))
        self.p2_melee_row02.clicked.connect(lambda: self.updateCurrentInput('p2_m_02'))
        self.p2_melee_row03.clicked.connect(lambda: self.updateCurrentInput('p2_m_03'))
        self.p2_melee_row04.clicked.connect(lambda: self.updateCurrentInput('p2_m_04'))
        self.p2_melee_row05.clicked.connect(lambda: self.updateCurrentInput('p2_m_05'))
        self.p2_melee_row06.clicked.connect(lambda: self.updateCurrentInput('p2_m_06'))
        self.p2_melee_row07.clicked.connect(lambda: self.updateCurrentInput('p2_m_07'))
        self.p2_melee_row08.clicked.connect(lambda: self.updateCurrentInput('p2_m_08'))
        self.p2_melee_row09.clicked.connect(lambda: self.updateCurrentInput('p2_m_09'))
        self.p2_melee_row10.clicked.connect(lambda: self.updateCurrentInput('p2_m_10'))
        self.p2_melee_row11.clicked.connect(lambda: self.updateCurrentInput('p2_m_11'))
        self.p2_melee_row12.clicked.connect(lambda: self.updateCurrentInput('p2_m_12'))
        self.p2_melee_row13.clicked.connect(lambda: self.updateCurrentInput('p2_m_13'))
        self.p2_melee_row14.clicked.connect(lambda: self.updateCurrentInput('p2_m_14'))
        self.p2_melee_row15.clicked.connect(lambda: self.updateCurrentInput('p2_m_15'))
        self.p2_melee_row16.clicked.connect(lambda: self.updateCurrentInput('p2_m_16'))
        self.p2_melee_row17.clicked.connect(lambda: self.updateCurrentInput('p2_m_17'))
        self.p2_melee_row18.clicked.connect(lambda: self.updateCurrentInput('p2_m_18'))
        self.p2_melee_row19.clicked.connect(lambda: self.updateCurrentInput('p2_m_19'))
        self.p2_melee_row20.clicked.connect(lambda: self.updateCurrentInput('p2_m_20'))

        self.p2_ranged_row01.clicked.connect(lambda: self.updateCurrentInput('p2_r_01'))
        self.p2_ranged_row02.clicked.connect(lambda: self.updateCurrentInput('p2_r_02'))
        self.p2_ranged_row03.clicked.connect(lambda: self.updateCurrentInput('p2_r_03'))
        self.p2_ranged_row04.clicked.connect(lambda: self.updateCurrentInput('p2_r_04'))
        self.p2_ranged_row05.clicked.connect(lambda: self.updateCurrentInput('p2_r_05'))
        self.p2_ranged_row06.clicked.connect(lambda: self.updateCurrentInput('p2_r_06'))
        self.p2_ranged_row07.clicked.connect(lambda: self.updateCurrentInput('p2_r_07'))
        self.p2_ranged_row08.clicked.connect(lambda: self.updateCurrentInput('p2_r_08'))
        self.p2_ranged_row09.clicked.connect(lambda: self.updateCurrentInput('p2_r_09'))
        self.p2_ranged_row10.clicked.connect(lambda: self.updateCurrentInput('p2_r_10'))
        self.p2_ranged_row11.clicked.connect(lambda: self.updateCurrentInput('p2_r_11'))
        self.p2_ranged_row12.clicked.connect(lambda: self.updateCurrentInput('p2_r_12'))
        self.p2_ranged_row13.clicked.connect(lambda: self.updateCurrentInput('p2_r_13'))
        self.p2_ranged_row14.clicked.connect(lambda: self.updateCurrentInput('p2_r_14'))
        self.p2_ranged_row15.clicked.connect(lambda: self.updateCurrentInput('p2_r_15'))
        self.p2_ranged_row16.clicked.connect(lambda: self.updateCurrentInput('p2_r_16'))
        self.p2_ranged_row17.clicked.connect(lambda: self.updateCurrentInput('p2_r_17'))
        self.p2_ranged_row18.clicked.connect(lambda: self.updateCurrentInput('p2_r_18'))
        self.p2_ranged_row19.clicked.connect(lambda: self.updateCurrentInput('p2_r_19'))
        self.p2_ranged_row20.clicked.connect(lambda: self.updateCurrentInput('p2_r_20'))

        self.p2_siege_row01.clicked.connect(lambda: self.updateCurrentInput('p2_s_01'))
        self.p2_siege_row02.clicked.connect(lambda: self.updateCurrentInput('p2_s_02'))
        self.p2_siege_row03.clicked.connect(lambda: self.updateCurrentInput('p2_s_03'))
        self.p2_siege_row04.clicked.connect(lambda: self.updateCurrentInput('p2_s_04'))
        self.p2_siege_row05.clicked.connect(lambda: self.updateCurrentInput('p2_s_05'))
        self.p2_siege_row06.clicked.connect(lambda: self.updateCurrentInput('p2_s_06'))
        self.p2_siege_row07.clicked.connect(lambda: self.updateCurrentInput('p2_s_07'))
        self.p2_siege_row08.clicked.connect(lambda: self.updateCurrentInput('p2_s_08'))
        self.p2_siege_row09.clicked.connect(lambda: self.updateCurrentInput('p2_s_09'))
        self.p2_siege_row10.clicked.connect(lambda: self.updateCurrentInput('p2_s_10'))
        self.p2_siege_row11.clicked.connect(lambda: self.updateCurrentInput('p2_s_11'))
        self.p2_siege_row12.clicked.connect(lambda: self.updateCurrentInput('p2_s_12'))
        self.p2_siege_row13.clicked.connect(lambda: self.updateCurrentInput('p2_s_13'))
        self.p2_siege_row14.clicked.connect(lambda: self.updateCurrentInput('p2_s_14'))
        self.p2_siege_row15.clicked.connect(lambda: self.updateCurrentInput('p2_s_15'))
        self.p2_siege_row16.clicked.connect(lambda: self.updateCurrentInput('p2_s_16'))
        self.p2_siege_row17.clicked.connect(lambda: self.updateCurrentInput('p2_s_17'))
        self.p2_siege_row18.clicked.connect(lambda: self.updateCurrentInput('p2_s_18'))
        self.p2_siege_row19.clicked.connect(lambda: self.updateCurrentInput('p2_s_19'))
        self.p2_siege_row20.clicked.connect(lambda: self.updateCurrentInput('p2_s_20'))

        # graveyard cards
        self.grave_01.clicked.connect(lambda: self.updateCurrentInput('g_01'))
        self.grave_02.clicked.connect(lambda: self.updateCurrentInput('g_02'))
        self.grave_03.clicked.connect(lambda: self.updateCurrentInput('g_03'))
        self.grave_04.clicked.connect(lambda: self.updateCurrentInput('g_04'))
        self.grave_05.clicked.connect(lambda: self.updateCurrentInput('g_05'))
        self.grave_06.clicked.connect(lambda: self.updateCurrentInput('g_06'))
        self.grave_07.clicked.connect(lambda: self.updateCurrentInput('g_07'))
        self.grave_08.clicked.connect(lambda: self.updateCurrentInput('g_08'))
        self.grave_09.clicked.connect(lambda: self.updateCurrentInput('g_09'))
        self.grave_10.clicked.connect(lambda: self.updateCurrentInput('g_10'))
        self.grave_11.clicked.connect(lambda: self.updateCurrentInput('g_11'))
        self.grave_12.clicked.connect(lambda: self.updateCurrentInput('g_12'))
        self.grave_13.clicked.connect(lambda: self.updateCurrentInput('g_13'))
        self.grave_14.clicked.connect(lambda: self.updateCurrentInput('g_14'))
        self.grave_15.clicked.connect(lambda: self.updateCurrentInput('g_15'))
        self.grave_16.clicked.connect(lambda: self.updateCurrentInput('g_16'))
        self.grave_17.clicked.connect(lambda: self.updateCurrentInput('g_17'))
        self.grave_18.clicked.connect(lambda: self.updateCurrentInput('g_18'))
        self.grave_19.clicked.connect(lambda: self.updateCurrentInput('g_19'))
        self.grave_20.clicked.connect(lambda: self.updateCurrentInput('g_20'))

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

        # drawing rounds won
        self.connect(self.game, SIGNAL('getP1RoundsWon(int)'), self.getP1RoundsWon)
        self.connect(self.game, SIGNAL('getP2RoundsWon(int)'), self.getP2RoundsWon)

    def sendSelectedDeck(self):
        if self.deckListBox.currentItem() is None:
            pass
        else:
            self.updateCurrentInput(self.deckListBox.currentItem().text())

    def updateCurrentInput(self, input):
        self.game.currentInput = input

    def showDecks(self, deckList):
        for deck in deckList:
            self.deckListBox.addItem(deck)

    def switchDeckList(self, on_off):
        if on_off == 'off':
            self.deckListBox.hide()
            self.selectDeck.hide()

    def updateGameMessage(self, message):
        self.gameMessage.setText(message)

    def hideGraveyard(self):
        # disable
        self.grave_01.setEnabled(False)
        self.grave_02.setEnabled(False)
        self.grave_03.setEnabled(False)
        self.grave_04.setEnabled(False)
        self.grave_05.setEnabled(False)
        self.grave_06.setEnabled(False)
        self.grave_07.setEnabled(False)
        self.grave_08.setEnabled(False)
        self.grave_09.setEnabled(False)
        self.grave_10.setEnabled(False)
        self.grave_11.setEnabled(False)
        self.grave_12.setEnabled(False)
        self.grave_13.setEnabled(False)
        self.grave_14.setEnabled(False)
        self.grave_15.setEnabled(False)
        self.grave_16.setEnabled(False)
        self.grave_17.setEnabled(False)
        self.grave_18.setEnabled(False)
        self.grave_19.setEnabled(False)
        self.grave_20.setEnabled(False)

        # hide
        self.grave_01.hide()
        self.grave_02.hide()
        self.grave_03.hide()
        self.grave_04.hide()
        self.grave_05.hide()
        self.grave_06.hide()
        self.grave_07.hide()
        self.grave_08.hide()
        self.grave_09.hide()
        self.grave_10.hide()
        self.grave_11.hide()
        self.grave_12.hide()
        self.grave_13.hide()
        self.grave_14.hide()
        self.grave_15.hide()
        self.grave_16.hide()
        self.grave_17.hide()
        self.grave_18.hide()
        self.grave_19.hide()
        self.grave_20.hide()

    def switchGrave(self, sentgraveyard):
        graveSize = len(sentgraveyard)

        if graveSize > 0:
            self.grave_01.setEnabled(True)
            self.grave_01.setIcon(QtGui.QIcon('images/' + sentgraveyard[0] + '.jpg'))
            self.grave_01.show()
        else:
            self.grave_01.setEnabled(False)
            self.grave_01.hide()
        if graveSize > 1:
            self.grave_02.setEnabled(True)
            self.grave_02.setIcon(QtGui.QIcon('images/' + sentgraveyard[1] + '.jpg'))
            self.grave_02.show()
        else:
            self.grave_02.setEnabled(False)
            self.grave_02.hide()
        if graveSize > 2:
            self.grave_03.setEnabled(True)
            self.grave_03.setIcon(QtGui.QIcon('images/' + sentgraveyard[2] + '.jpg'))
            self.grave_03.show()
        else:
            self.grave_03.setEnabled(False)
            self.grave_03.hide()
        if graveSize > 3:
            self.grave_04.setEnabled(True)
            self.grave_04.setIcon(QtGui.QIcon('images/' + sentgraveyard[3] + '.jpg'))
            self.grave_04.show()
        else:
            self.grave_04.setEnabled(False)
            self.grave_04.hide()
        if graveSize > 4:
            self.grave_05.setEnabled(True)
            self.grave_05.setIcon(QtGui.QIcon('images/' + sentgraveyard[4] + '.jpg'))
            self.grave_05.show()
        else:
            self.grave_05.setEnabled(False)
            self.grave_05.hide()
        if graveSize > 5:
            self.grave_06.setEnabled(True)
            self.grave_06.setIcon(QtGui.QIcon('images/' + sentgraveyard[5] + '.jpg'))
            self.grave_06.show()
        else:
            self.grave_06.setEnabled(False)
            self.grave_06.hide()
        if graveSize > 6:
            self.grave_07.setEnabled(True)
            self.grave_07.setIcon(QtGui.QIcon('images/' + sentgraveyard[6] + '.jpg'))
            self.grave_07.show()
        else:
            self.grave_07.setEnabled(False)
            self.grave_07.hide()
        if graveSize > 7:
            self.grave_08.setEnabled(True)
            self.grave_08.setIcon(QtGui.QIcon('images/' + sentgraveyard[7] + '.jpg'))
            self.grave_08.show()
        else:
            self.grave_08.setEnabled(False)
            self.grave_08.hide()
        if graveSize > 8:
            self.grave_09.setEnabled(True)
            self.grave_09.setIcon(QtGui.QIcon('images/' + sentgraveyard[8] + '.jpg'))
            self.grave_09.show()
        else:
            self.grave_09.setEnabled(False)
            self.grave_09.hide()
        if graveSize > 9:
            self.grave_10.setEnabled(True)
            self.grave_10.setIcon(QtGui.QIcon('images/' + sentgraveyard[9] + '.jpg'))
            self.grave_10.show()
        else:
            self.grave_10.setEnabled(False)
            self.grave_10.hide()
        if graveSize > 10:
            self.grave_11.setEnabled(True)
            self.grave_11.setIcon(QtGui.QIcon('images/' + sentgraveyard[10] + '.jpg'))
            self.grave_11.show()
        else:
            self.grave_11.setEnabled(False)
            self.grave_11.hide()
        if graveSize > 11:
            self.grave_12.setEnabled(True)
            self.grave_12.setIcon(QtGui.QIcon('images/' + sentgraveyard[11] + '.jpg'))
            self.grave_12.show()
        else:
            self.grave_12.setEnabled(False)
            self.grave_12.hide()
        if graveSize > 12:
            self.grave_13.setEnabled(True)
            self.grave_13.setIcon(QtGui.QIcon('images/' + sentgraveyard[12] + '.jpg'))
            self.grave_13.show()
        else:
            self.grave_13.setEnabled(False)
            self.grave_13.hide()
        if graveSize > 13:
            self.grave_14.setEnabled(True)
            self.grave_14.setIcon(QtGui.QIcon('images/' + sentgraveyard[13] + '.jpg'))
            self.grave_14.show()
        else:
            self.grave_14.setEnabled(False)
            self.grave_14.hide()
        if graveSize > 14:
            self.grave_15.setEnabled(True)
            self.grave_15.setIcon(QtGui.QIcon('images/' + sentgraveyard[14] + '.jpg'))
            self.grave_15.show()
        else:
            self.grave_15.setEnabled(False)
            self.grave_15.hide()
        if graveSize > 15:
            self.grave_16.setEnabled(True)
            self.grave_16.setIcon(QtGui.QIcon('images/' + sentgraveyard[15] + '.jpg'))
            self.grave_16.show()
        else:
            self.grave_16.setEnabled(False)
            self.grave_16.hide()
        if graveSize > 16:
            self.grave_17.setEnabled(True)
            self.grave_17.setIcon(QtGui.QIcon('images/' + sentgraveyard[16] + '.jpg'))
            self.grave_17.show()
        else:
            self.grave_17.setEnabled(False)
            self.grave_17.hide()
        if graveSize > 17:
            self.grave_18.setEnabled(True)
            self.grave_18.setIcon(QtGui.QIcon('images/' + sentgraveyard[17] + '.jpg'))
            self.grave_18.show()
        else:
            self.grave_18.setEnabled(False)
            self.grave_18.hide()
        if graveSize > 18:
            self.grave_19.setEnabled(True)
            self.grave_19.setIcon(QtGui.QIcon('images/' + sentgraveyard[18] + '.jpg'))
            self.grave_19.show()
        else:
            self.grave_19.setEnabled(False)
            self.grave_19.hide()
        if graveSize > 19:
            self.grave_20.setEnabled(True)
            self.grave_20.setIcon(QtGui.QIcon('images/' + sentgraveyard[19] + '.jpg'))
            self.grave_20.show()
        else:
            self.grave_20.setEnabled(False)
            self.grave_20.hide()

    def switchNext(self, on_off):
        if on_off == 'on':
            self.nextButton.setEnabled(True)
        elif on_off == 'off':
            self.nextButton.setEnabled(False)

    def switchPass(self, on_off):
        if on_off == 'on':
            self.passButton.setEnabled(True)
        elif on_off == 'off':
            self.passButton.setEnabled(False)

    def switchMelee(self, on_off):
        if on_off == 'on':
            self.meleeButton.setEnabled(True)
        elif on_off == 'off':
            self.meleeButton.setEnabled(False)

    def switchRanged(self, on_off):
        if on_off == 'on':
            self.rangedButton.setEnabled(True)
        elif on_off == 'off':
            self.rangedButton.setEnabled(False)

    def switchSiege(self, on_off):
        if on_off == 'on':
            self.siegeButton.setEnabled(True)
        elif on_off == 'off':
            self.siegeButton.setEnabled(False)

    def getPlayerTurn(self, player_turn):
        self.player_turn = player_turn

    def drawCurrentP1RoundScore(self, p1_round_score):
        self.p1_score_text.setText(str(p1_round_score))

    def drawCurrentP2RoundScore(self, p2_round_score):
        self.p2_score_text.setText(str(p2_round_score))

    def getP1RoundsWon(self, p1_rounds_won):
        self.p1_rounds_won_text.setText(str(p1_rounds_won))

    def getP2RoundsWon(self, p2_rounds_won):
        self.p2_rounds_won_text.setText(str(p2_rounds_won))

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
            self.weather_1.show()
        else:
            self.weather_1.hide()
        if weatherSize > 1:
            self.weather_2.setPixmap(QtGui.QPixmap('images/' + weather[1] + '.jpg'))
            self.weather_2.show()
        else:
            self.weather_2.hide()

    def drawCurrentP1Hand(self, p1_hand):
        if self.player_turn == 1:

            handSize = len(p1_hand)

            if handSize > 0:
                self.hand_01.setEnabled(True)
                self.hand_01.setIcon(QtGui.QIcon('images/' + p1_hand[0] + '.jpg'))
                self.hand_01.show()
            else:
                self.hand_01.setEnabled(False)
                self.hand_01.hide()

            if handSize > 1:
                self.hand_02.setEnabled(True)
                self.hand_02.setIcon(QtGui.QIcon('images/' + p1_hand[1] + '.jpg'))
                self.hand_02.show()
            else:
                self.hand_02.setEnabled(False)
                self.hand_02.hide()

            if handSize > 2:
                self.hand_03.setEnabled(True)
                self.hand_03.setIcon(QtGui.QIcon('images/' + p1_hand[2] + '.jpg'))
                self.hand_03.show()
            else:
                self.hand_03.setEnabled(False)
                self.hand_03.hide()

            if handSize > 3:
                self.hand_04.setEnabled(True)
                self.hand_04.setIcon(QtGui.QIcon('images/' + p1_hand[3] + '.jpg'))
                self.hand_04.show()
            else:
                self.hand_04.setEnabled(False)
                self.hand_04.hide()

            if handSize > 4:
                self.hand_05.setEnabled(True)
                self.hand_05.setIcon(QtGui.QIcon('images/' + p1_hand[4] + '.jpg'))
                self.hand_05.show()
            else:
                self.hand_05.setEnabled(False)
                self.hand_05.hide()

            if handSize > 5:
                self.hand_06.setEnabled(True)
                self.hand_06.setIcon(QtGui.QIcon('images/' + p1_hand[5] + '.jpg'))
                self.hand_06.show()
            else:
                self.hand_06.setEnabled(False)
                self.hand_06.hide()

            if handSize > 6:
                self.hand_07.setEnabled(True)
                self.hand_07.setIcon(QtGui.QIcon('images/' + p1_hand[6] + '.jpg'))
                self.hand_07.show()
            else:
                self.hand_07.setEnabled(False)
                self.hand_07.hide()

            if handSize > 7:
                self.hand_08.setEnabled(True)
                self.hand_08.setIcon(QtGui.QIcon('images/' + p1_hand[7] + '.jpg'))
                self.hand_08.show()
            else:
                self.hand_08.setEnabled(False)
                self.hand_08.hide()

            if handSize > 8:
                self.hand_09.setEnabled(True)
                self.hand_09.setIcon(QtGui.QIcon('images/' + p1_hand[8] + '.jpg'))
                self.hand_09.show()
            else:
                self.hand_09.setEnabled(False)
                self.hand_09.hide()

            if handSize > 9:
                self.hand_10.setEnabled(True)
                self.hand_10.setIcon(QtGui.QIcon('images/' + p1_hand[9] + '.jpg'))
                self.hand_10.show()
            else:
                self.hand_10.setEnabled(False)
                self.hand_10.hide()

            if handSize > 10:
                self.hand_11.setEnabled(True)
                self.hand_11.setIcon(QtGui.QIcon('images/' + p1_hand[10] + '.jpg'))
                self.hand_11.show()
            else:
                self.hand_11.setEnabled(False)
                self.hand_11.hide()

            if handSize > 11:
                self.hand_12.setEnabled(True)
                self.hand_12.setIcon(QtGui.QIcon('images/' + p1_hand[11] + '.jpg'))
                self.hand_12.show()
            else:
                self.hand_12.setEnabled(False)
                self.hand_12.hide()

            if handSize > 12:
                self.hand_13.setEnabled(True)
                self.hand_13.setIcon(QtGui.QIcon('images/' + p1_hand[12] + '.jpg'))
                self.hand_13.show()
            else:
                self.hand_13.setEnabled(False)
                self.hand_13.hide()

            if handSize > 13:
                self.hand_14.setEnabled(True)
                self.hand_14.setIcon(QtGui.QIcon('images/' + p1_hand[13] + '.jpg'))
                self.hand_14.show()
            else:
                self.hand_14.setEnabled(False)
                self.hand_14.hide()

            if handSize > 14:
                self.hand_15.setEnabled(True)
                self.hand_15.setIcon(QtGui.QIcon('images/' + p1_hand[14] + '.jpg'))
                self.hand_15.show()
            else:
                self.hand_15.setEnabled(False)
                self.hand_15.hide()

            if handSize > 15:
                self.hand_16.setEnabled(True)
                self.hand_16.setIcon(QtGui.QIcon('images/' + p1_hand[15] + '.jpg'))
                self.hand_16.show()
            else:
                self.hand_16.setEnabled(False)
                self.hand_16.hide()

            if handSize > 16:
                self.hand_17.setEnabled(True)
                self.hand_17.setIcon(QtGui.QIcon('images/' + p1_hand[16] + '.jpg'))
                self.hand_17.show()
            else:
                self.hand_17.setEnabled(False)
                self.hand_17.hide()

            if handSize > 17:
                self.hand_18.setEnabled(True)
                self.hand_18.setIcon(QtGui.QIcon('images/' + p1_hand[17] + '.jpg'))
                self.hand_18.show()
            else:
                self.hand_18.setEnabled(False)
                self.hand_18.hide()

            if handSize > 18:
                self.hand_19.setEnabled(True)
                self.hand_19.setIcon(QtGui.QIcon('images/' + p1_hand[18] + '.jpg'))
                self.hand_19.show()
            else:
                self.hand_19.setEnabled(False)
                self.hand_19.hide()

            if handSize > 19:
                self.hand_20.setEnabled(True)
                self.hand_20.setIcon(QtGui.QIcon('images/' + p1_hand[19] + '.jpg'))
                self.hand_20.show()
            else:
                self.hand_20.setEnabled(False)
                self.hand_20.hide()

    def drawCurrentP2Hand(self, p2_hand):
        if self.player_turn == 2:

            handSize = len(p2_hand)

            if handSize > 0:
                self.hand_01.setEnabled(True)
                self.hand_01.setIcon(QtGui.QIcon('images/' + p2_hand[0] + '.jpg'))
                self.hand_01.show()
            else:
                self.hand_01.setEnabled(False)
                self.hand_01.hide()

            if handSize > 1:
                self.hand_02.setEnabled(True)
                self.hand_02.setIcon(QtGui.QIcon('images/' + p2_hand[1] + '.jpg'))
                self.hand_02.show()
            else:
                self.hand_02.setEnabled(False)
                self.hand_02.hide()

            if handSize > 2:
                self.hand_03.setEnabled(True)
                self.hand_03.setIcon(QtGui.QIcon('images/' + p2_hand[2] + '.jpg'))
                self.hand_03.show()
            else:
                self.hand_03.setEnabled(False)
                self.hand_03.hide()

            if handSize > 3:
                self.hand_04.setEnabled(True)
                self.hand_04.setIcon(QtGui.QIcon('images/' + p2_hand[3] + '.jpg'))
                self.hand_04.show()
            else:
                self.hand_04.setEnabled(False)
                self.hand_04.hide()

            if handSize > 4:
                self.hand_05.setEnabled(True)
                self.hand_05.setIcon(QtGui.QIcon('images/' + p2_hand[4] + '.jpg'))
                self.hand_05.show()
            else:
                self.hand_05.setEnabled(False)
                self.hand_05.hide()

            if handSize > 5:
                self.hand_06.setEnabled(True)
                self.hand_06.setIcon(QtGui.QIcon('images/' + p2_hand[5] + '.jpg'))
                self.hand_06.show()
            else:
                self.hand_06.setEnabled(False)
                self.hand_06.hide()

            if handSize > 6:
                self.hand_07.setEnabled(True)
                self.hand_07.setIcon(QtGui.QIcon('images/' + p2_hand[6] + '.jpg'))
                self.hand_07.show()
            else:
                self.hand_07.setEnabled(False)
                self.hand_07.hide()

            if handSize > 7:
                self.hand_08.setEnabled(True)
                self.hand_08.setIcon(QtGui.QIcon('images/' + p2_hand[7] + '.jpg'))
                self.hand_08.show()
            else:
                self.hand_08.setEnabled(False)
                self.hand_08.hide()

            if handSize > 8:
                self.hand_09.setEnabled(True)
                self.hand_09.setIcon(QtGui.QIcon('images/' + p2_hand[8] + '.jpg'))
                self.hand_09.show()
            else:
                self.hand_09.setEnabled(False)
                self.hand_09.hide()

            if handSize > 9:
                self.hand_10.setEnabled(True)
                self.hand_10.setIcon(QtGui.QIcon('images/' + p2_hand[9] + '.jpg'))
                self.hand_10.show()
            else:
                self.hand_10.setEnabled(False)
                self.hand_10.hide()

            if handSize > 10:
                self.hand_11.setEnabled(True)
                self.hand_11.setIcon(QtGui.QIcon('images/' + p2_hand[10] + '.jpg'))
                self.hand_11.show()
            else:
                self.hand_11.setEnabled(False)
                self.hand_11.hide()

            if handSize > 11:
                self.hand_12.setEnabled(True)
                self.hand_12.setIcon(QtGui.QIcon('images/' + p2_hand[11] + '.jpg'))
                self.hand_12.show()
            else:
                self.hand_12.setEnabled(False)
                self.hand_12.hide()

            if handSize > 12:
                self.hand_13.setEnabled(True)
                self.hand_13.setIcon(QtGui.QIcon('images/' + p2_hand[12] + '.jpg'))
                self.hand_13.show()
            else:
                self.hand_13.setEnabled(False)
                self.hand_13.hide()

            if handSize > 13:
                self.hand_14.setEnabled(True)
                self.hand_14.setIcon(QtGui.QIcon('images/' + p2_hand[13] + '.jpg'))
                self.hand_14.show()
            else:
                self.hand_14.setEnabled(False)
                self.hand_14.hide()

            if handSize > 14:
                self.hand_15.setEnabled(True)
                self.hand_15.setIcon(QtGui.QIcon('images/' + p2_hand[14] + '.jpg'))
                self.hand_15.show()
            else:
                self.hand_15.setEnabled(False)
                self.hand_15.hide()

            if handSize > 15:
                self.hand_16.setEnabled(True)
                self.hand_16.setIcon(QtGui.QIcon('images/' + p2_hand[15] + '.jpg'))
                self.hand_16.show()
            else:
                self.hand_16.setEnabled(False)
                self.hand_16.hide()

            if handSize > 16:
                self.hand_17.setEnabled(True)
                self.hand_17.setIcon(QtGui.QIcon('images/' + p2_hand[16] + '.jpg'))
                self.hand_17.show()
            else:
                self.hand_17.setEnabled(False)
                self.hand_17.hide()

            if handSize > 17:
                self.hand_18.setEnabled(True)
                self.hand_18.setIcon(QtGui.QIcon('images/' + p2_hand[17] + '.jpg'))
                self.hand_18.show()
            else:
                self.hand_18.setEnabled(False)
                self.hand_18.hide()

            if handSize > 18:
                self.hand_19.setEnabled(True)
                self.hand_19.setIcon(QtGui.QIcon('images/' + p2_hand[18] + '.jpg'))
                self.hand_19.show()
            else:
                self.hand_19.setEnabled(False)
                self.hand_19.hide()

            if handSize > 19:
                self.hand_20.setEnabled(True)
                self.hand_20.setIcon(QtGui.QIcon('images/' + p2_hand[19] + '.jpg'))
                self.hand_20.show()
            else:
                self.hand_20.setEnabled(False)
                self.hand_20.hide()

    def drawCurrentP1MeleeLine(self, p1_melee_line):
        p1_melee_line_size = len(p1_melee_line)

        if p1_melee_line_size > 0:
            self.p1_melee_row01.setEnabled(True)
            self.p1_melee_row01.setIcon(QtGui.QIcon('images/' + p1_melee_line[0] + '.jpg'))
            self.p1_melee_row01.show()
        else:
            self.p1_melee_row01.setEnabled(False)
            self.p1_melee_row01.hide()

        if p1_melee_line_size > 1:
            self.p1_melee_row02.setEnabled(True)
            self.p1_melee_row02.setIcon(QtGui.QIcon('images/' + p1_melee_line[1] + '.jpg'))
            self.p1_melee_row02.show()
        else:
            self.p1_melee_row02.setEnabled(False)
            self.p1_melee_row02.hide()

        if p1_melee_line_size > 2:
            self.p1_melee_row03.setEnabled(True)
            self.p1_melee_row03.setIcon(QtGui.QIcon('images/' + p1_melee_line[2] + '.jpg'))
            self.p1_melee_row03.show()
        else:
            self.p1_melee_row03.setEnabled(False)
            self.p1_melee_row03.hide()

        if p1_melee_line_size > 3:
            self.p1_melee_row04.setEnabled(True)
            self.p1_melee_row04.setIcon(QtGui.QIcon('images/' + p1_melee_line[3] + '.jpg'))
            self.p1_melee_row04.show()
        else:
            self.p1_melee_row04.setEnabled(False)
            self.p1_melee_row04.hide()

        if p1_melee_line_size > 4:
            self.p1_melee_row05.setEnabled(True)
            self.p1_melee_row05.setIcon(QtGui.QIcon('images/' + p1_melee_line[4] + '.jpg'))
            self.p1_melee_row05.show()
        else:
            self.p1_melee_row05.setEnabled(False)
            self.p1_melee_row05.hide()

        if p1_melee_line_size > 5:
            self.p1_melee_row06.setEnabled(True)
            self.p1_melee_row06.setIcon(QtGui.QIcon('images/' + p1_melee_line[5] + '.jpg'))
            self.p1_melee_row06.show()
        else:
            self.p1_melee_row06.setEnabled(False)
            self.p1_melee_row06.hide()

        if p1_melee_line_size > 6:
            self.p1_melee_row07.setEnabled(True)
            self.p1_melee_row07.setIcon(QtGui.QIcon('images/' + p1_melee_line[6] + '.jpg'))
            self.p1_melee_row07.show()
        else:
            self.p1_melee_row07.setEnabled(False)
            self.p1_melee_row07.hide()

        if p1_melee_line_size > 7:
            self.p1_melee_row08.setEnabled(True)
            self.p1_melee_row08.setIcon(QtGui.QIcon('images/' + p1_melee_line[7] + '.jpg'))
            self.p1_melee_row08.show()
        else:
            self.p1_melee_row08.setEnabled(False)
            self.p1_melee_row08.hide()

        if p1_melee_line_size > 8:
            self.p1_melee_row09.setEnabled(True)
            self.p1_melee_row09.setIcon(QtGui.QIcon('images/' + p1_melee_line[8] + '.jpg'))
            self.p1_melee_row09.show()
        else:
            self.p1_melee_row09.setEnabled(False)
            self.p1_melee_row09.hide()

        if p1_melee_line_size > 9:
            self.p1_melee_row10.setEnabled(True)
            self.p1_melee_row10.setIcon(QtGui.QIcon('images/' + p1_melee_line[9] + '.jpg'))
            self.p1_melee_row10.show()
        else:
            self.p1_melee_row10.setEnabled(False)
            self.p1_melee_row10.hide()

        if p1_melee_line_size > 10:
            self.p1_melee_row11.setEnabled(True)
            self.p1_melee_row11.setIcon(QtGui.QIcon('images/' + p1_melee_line[10] + '.jpg'))
            self.p1_melee_row11.show()
        else:
            self.p1_melee_row11.setEnabled(False)
            self.p1_melee_row11.hide()

        if p1_melee_line_size > 11:
            self.p1_melee_row12.setEnabled(True)
            self.p1_melee_row12.setIcon(QtGui.QIcon('images/' + p1_melee_line[11] + '.jpg'))
            self.p1_melee_row12.show()
        else:
            self.p1_melee_row12.setEnabled(False)
            self.p1_melee_row12.hide()

        if p1_melee_line_size > 12:
            self.p1_melee_row13.setEnabled(True)
            self.p1_melee_row13.setIcon(QtGui.QIcon('images/' + p1_melee_line[12] + '.jpg'))
            self.p1_melee_row13.show()
        else:
            self.p1_melee_row13.setEnabled(False)
            self.p1_melee_row13.hide()

        if p1_melee_line_size > 13:
            self.p1_melee_row14.setEnabled(True)
            self.p1_melee_row14.setIcon(QtGui.QIcon('images/' + p1_melee_line[13] + '.jpg'))
            self.p1_melee_row14.show()
        else:
            self.p1_melee_row14.setEnabled(False)
            self.p1_melee_row14.hide()

        if p1_melee_line_size > 14:
            self.p1_melee_row15.setEnabled(True)
            self.p1_melee_row15.setIcon(QtGui.QIcon('images/' + p1_melee_line[14] + '.jpg'))
            self.p1_melee_row15.show()
        else:
            self.p1_melee_row15.setEnabled(False)
            self.p1_melee_row15.hide()

        if p1_melee_line_size > 15:
            self.p1_melee_row16.setEnabled(True)
            self.p1_melee_row16.setIcon(QtGui.QIcon('images/' + p1_melee_line[15] + '.jpg'))
            self.p1_melee_row16.show()
        else:
            self.p1_melee_row16.setEnabled(False)
            self.p1_melee_row16.hide()

        if p1_melee_line_size > 16:
            self.p1_melee_row17.setEnabled(True)
            self.p1_melee_row17.setIcon(QtGui.QIcon('images/' + p1_melee_line[16] + '.jpg'))
            self.p1_melee_row17.show()
        else:
            self.p1_melee_row17.setEnabled(False)
            self.p1_melee_row17.hide()

        if p1_melee_line_size > 17:
            self.p1_melee_row18.setEnabled(True)
            self.p1_melee_row18.setIcon(QtGui.QIcon('images/' + p1_melee_line[17] + '.jpg'))
            self.p1_melee_row18.show()
        else:
            self.p1_melee_row18.setEnabled(False)
            self.p1_melee_row18.hide()

        if p1_melee_line_size > 18:
            self.p1_melee_row19.setEnabled(True)
            self.p1_melee_row19.setIcon(QtGui.QIcon('images/' + p1_melee_line[18] + '.jpg'))
            self.p1_melee_row19.show()
        else:
            self.p1_melee_row19.setEnabled(False)
            self.p1_melee_row19.hide()

        if p1_melee_line_size > 19:
            self.p1_melee_row20.setEnabled(True)
            self.p1_melee_row20.setIcon(QtGui.QIcon('images/' + p1_melee_line[19] + '.jpg'))
            self.p1_melee_row20.show()
        else:
            self.p1_melee_row20.setEnabled(False)
            self.p1_melee_row20.hide()

    def drawCurrentP1RangedLine(self, p1_ranged_line):
        p1_ranged_line_size = len(p1_ranged_line)

        if p1_ranged_line_size > 0:
            self.p1_ranged_row01.setEnabled(True)
            self.p1_ranged_row01.setIcon(QtGui.QIcon('images/' + p1_ranged_line[0] + '.jpg'))
            self.p1_ranged_row01.show()
        else:
            self.p1_ranged_row01.setEnabled(False)
            self.p1_ranged_row01.hide()

        if p1_ranged_line_size > 1:
            self.p1_ranged_row02.setEnabled(True)
            self.p1_ranged_row02.setIcon(QtGui.QIcon('images/' + p1_ranged_line[1] + '.jpg'))
            self.p1_ranged_row02.show()
        else:
            self.p1_ranged_row02.setEnabled(False)
            self.p1_ranged_row02.hide()

        if p1_ranged_line_size > 2:
            self.p1_ranged_row03.setEnabled(True)
            self.p1_ranged_row03.setIcon(QtGui.QIcon('images/' + p1_ranged_line[2] + '.jpg'))
            self.p1_ranged_row03.show()
        else:
            self.p1_ranged_row03.setEnabled(False)
            self.p1_ranged_row03.hide()

        if p1_ranged_line_size > 3:
            self.p1_ranged_row04.setEnabled(True)
            self.p1_ranged_row04.setIcon(QtGui.QIcon('images/' + p1_ranged_line[3] + '.jpg'))
            self.p1_ranged_row04.show()
        else:
            self.p1_ranged_row04.setEnabled(False)
            self.p1_ranged_row04.hide()

        if p1_ranged_line_size > 4:
            self.p1_ranged_row05.setEnabled(True)
            self.p1_ranged_row05.setIcon(QtGui.QIcon('images/' + p1_ranged_line[4] + '.jpg'))
            self.p1_ranged_row05.show()
        else:
            self.p1_ranged_row05.setEnabled(False)
            self.p1_ranged_row05.hide()

        if p1_ranged_line_size > 5:
            self.p1_ranged_row06.setEnabled(True)
            self.p1_ranged_row06.setIcon(QtGui.QIcon('images/' + p1_ranged_line[5] + '.jpg'))
            self.p1_ranged_row06.show()
        else:
            self.p1_ranged_row06.setEnabled(False)
            self.p1_ranged_row06.hide()

        if p1_ranged_line_size > 6:
            self.p1_ranged_row07.setEnabled(True)
            self.p1_ranged_row07.setIcon(QtGui.QIcon('images/' + p1_ranged_line[6] + '.jpg'))
            self.p1_ranged_row07.show()
        else:
            self.p1_ranged_row07.setEnabled(False)
            self.p1_ranged_row07.hide()

        if p1_ranged_line_size > 7:
            self.p1_ranged_row08.setEnabled(True)
            self.p1_ranged_row08.setIcon(QtGui.QIcon('images/' + p1_ranged_line[7] + '.jpg'))
            self.p1_ranged_row08.show()
        else:
            self.p1_ranged_row08.setEnabled(False)
            self.p1_ranged_row08.hide()

        if p1_ranged_line_size > 8:
            self.p1_ranged_row09.setEnabled(True)
            self.p1_ranged_row09.setIcon(QtGui.QIcon('images/' + p1_ranged_line[8] + '.jpg'))
            self.p1_ranged_row09.show()
        else:
            self.p1_ranged_row09.setEnabled(False)
            self.p1_ranged_row09.hide()

        if p1_ranged_line_size > 9:
            self.p1_ranged_row10.setEnabled(True)
            self.p1_ranged_row10.setIcon(QtGui.QIcon('images/' + p1_ranged_line[9] + '.jpg'))
            self.p1_ranged_row10.show()
        else:
            self.p1_ranged_row10.setEnabled(False)
            self.p1_ranged_row10.hide()

        if p1_ranged_line_size > 10:
            self.p1_ranged_row11.setEnabled(True)
            self.p1_ranged_row11.setIcon(QtGui.QIcon('images/' + p1_ranged_line[10] + '.jpg'))
            self.p1_ranged_row11.show()
        else:
            self.p1_ranged_row11.setEnabled(False)
            self.p1_ranged_row11.hide()

        if p1_ranged_line_size > 11:
            self.p1_ranged_row12.setEnabled(True)
            self.p1_ranged_row12.setIcon(QtGui.QIcon('images/' + p1_ranged_line[11] + '.jpg'))
            self.p1_ranged_row12.show()
        else:
            self.p1_ranged_row12.setEnabled(False)
            self.p1_ranged_row12.hide()

        if p1_ranged_line_size > 12:
            self.p1_ranged_row13.setEnabled(True)
            self.p1_ranged_row13.setIcon(QtGui.QIcon('images/' + p1_ranged_line[12] + '.jpg'))
            self.p1_ranged_row13.show()
        else:
            self.p1_ranged_row13.setEnabled(False)
            self.p1_ranged_row13.hide()

        if p1_ranged_line_size > 13:
            self.p1_ranged_row14.setEnabled(True)
            self.p1_ranged_row14.setIcon(QtGui.QIcon('images/' + p1_ranged_line[13] + '.jpg'))
            self.p1_ranged_row14.show()
        else:
            self.p1_ranged_row14.setEnabled(False)
            self.p1_ranged_row14.hide()

        if p1_ranged_line_size > 14:
            self.p1_ranged_row15.setEnabled(True)
            self.p1_ranged_row15.setIcon(QtGui.QIcon('images/' + p1_ranged_line[14] + '.jpg'))
            self.p1_ranged_row15.show()
        else:
            self.p1_ranged_row15.setEnabled(False)
            self.p1_ranged_row15.hide()

        if p1_ranged_line_size > 15:
            self.p1_ranged_row16.setEnabled(True)
            self.p1_ranged_row16.setIcon(QtGui.QIcon('images/' + p1_ranged_line[15] + '.jpg'))
            self.p1_ranged_row16.show()
        else:
            self.p1_ranged_row16.setEnabled(False)
            self.p1_ranged_row16.hide()

        if p1_ranged_line_size > 16:
            self.p1_ranged_row17.setEnabled(True)
            self.p1_ranged_row17.setIcon(QtGui.QIcon('images/' + p1_ranged_line[16] + '.jpg'))
            self.p1_ranged_row17.show()
        else:
            self.p1_ranged_row17.setEnabled(False)
            self.p1_ranged_row17.hide()

        if p1_ranged_line_size > 17:
            self.p1_ranged_row18.setEnabled(True)
            self.p1_ranged_row18.setIcon(QtGui.QIcon('images/' + p1_ranged_line[17] + '.jpg'))
            self.p1_ranged_row18.show()
        else:
            self.p1_ranged_row18.setEnabled(False)
            self.p1_ranged_row18.hide()

        if p1_ranged_line_size > 18:
            self.p1_ranged_row19.setEnabled(True)
            self.p1_ranged_row19.setIcon(QtGui.QIcon('images/' + p1_ranged_line[18] + '.jpg'))
            self.p1_ranged_row19.show()
        else:
            self.p1_ranged_row19.setEnabled(False)
            self.p1_ranged_row19.hide()

        if p1_ranged_line_size > 19:
            self.p1_ranged_row20.setEnabled(True)
            self.p1_ranged_row20.setIcon(QtGui.QIcon('images/' + p1_ranged_line[19] + '.jpg'))
            self.p1_ranged_row20.show()
        else:
            self.p1_ranged_row20.setEnabled(False)
            self.p1_ranged_row20.hide()

    def drawCurrentP1SiegeLine(self, p1_siege_line):
        p1_siege_line_size = len(p1_siege_line)

        if p1_siege_line_size > 0:
            self.p1_siege_row01.setEnabled(True)
            self.p1_siege_row01.setIcon(QtGui.QIcon('images/' + p1_siege_line[0] + '.jpg'))
            self.p1_siege_row01.show()
        else:
            self.p1_siege_row01.setEnabled(False)
            self.p1_siege_row01.hide()

        if p1_siege_line_size > 1:
            self.p1_siege_row02.setEnabled(True)
            self.p1_siege_row02.setIcon(QtGui.QIcon('images/' + p1_siege_line[1] + '.jpg'))
            self.p1_siege_row02.show()
        else:
            self.p1_siege_row02.setEnabled(False)
            self.p1_siege_row02.hide()

        if p1_siege_line_size > 2:
            self.p1_siege_row03.setEnabled(True)
            self.p1_siege_row03.setIcon(QtGui.QIcon('images/' + p1_siege_line[2] + '.jpg'))
            self.p1_siege_row03.show()
        else:
            self.p1_siege_row03.setEnabled(False)
            self.p1_siege_row03.hide()

        if p1_siege_line_size > 3:
            self.p1_siege_row04.setEnabled(True)
            self.p1_siege_row04.setIcon(QtGui.QIcon('images/' + p1_siege_line[3] + '.jpg'))
            self.p1_siege_row04.show()
        else:
            self.p1_siege_row04.setEnabled(False)
            self.p1_siege_row04.hide()

        if p1_siege_line_size > 4:
            self.p1_siege_row05.setEnabled(True)
            self.p1_siege_row05.setIcon(QtGui.QIcon('images/' + p1_siege_line[4] + '.jpg'))
            self.p1_siege_row05.show()
        else:
            self.p1_siege_row05.setEnabled(False)
            self.p1_siege_row05.hide()

        if p1_siege_line_size > 5:
            self.p1_siege_row06.setEnabled(True)
            self.p1_siege_row06.setIcon(QtGui.QIcon('images/' + p1_siege_line[5] + '.jpg'))
            self.p1_siege_row06.show()
        else:
            self.p1_siege_row06.setEnabled(False)
            self.p1_siege_row06.hide()

        if p1_siege_line_size > 6:
            self.p1_siege_row07.setEnabled(True)
            self.p1_siege_row07.setIcon(QtGui.QIcon('images/' + p1_siege_line[6] + '.jpg'))
            self.p1_siege_row07.show()
        else:
            self.p1_siege_row07.setEnabled(False)
            self.p1_siege_row07.hide()

        if p1_siege_line_size > 7:
            self.p1_siege_row08.setEnabled(True)
            self.p1_siege_row08.setIcon(QtGui.QIcon('images/' + p1_siege_line[7] + '.jpg'))
            self.p1_siege_row08.show()
        else:
            self.p1_siege_row08.setEnabled(False)
            self.p1_siege_row08.hide()

        if p1_siege_line_size > 8:
            self.p1_siege_row09.setEnabled(True)
            self.p1_siege_row09.setIcon(QtGui.QIcon('images/' + p1_siege_line[8] + '.jpg'))
            self.p1_siege_row09.show()
        else:
            self.p1_siege_row09.setEnabled(False)
            self.p1_siege_row09.hide()

        if p1_siege_line_size > 9:
            self.p1_siege_row10.setEnabled(True)
            self.p1_siege_row10.setIcon(QtGui.QIcon('images/' + p1_siege_line[9] + '.jpg'))
            self.p1_siege_row10.show()
        else:
            self.p1_siege_row10.setEnabled(False)
            self.p1_siege_row10.hide()

        if p1_siege_line_size > 10:
            self.p1_siege_row11.setEnabled(True)
            self.p1_siege_row11.setIcon(QtGui.QIcon('images/' + p1_siege_line[10] + '.jpg'))
            self.p1_siege_row11.show()
        else:
            self.p1_siege_row11.setEnabled(False)
            self.p1_siege_row11.hide()

        if p1_siege_line_size > 11:
            self.p1_siege_row12.setEnabled(True)
            self.p1_siege_row12.setIcon(QtGui.QIcon('images/' + p1_siege_line[11] + '.jpg'))
            self.p1_siege_row12.show()
        else:
            self.p1_siege_row12.setEnabled(False)
            self.p1_siege_row12.hide()

        if p1_siege_line_size > 12:
            self.p1_siege_row13.setEnabled(True)
            self.p1_siege_row13.setIcon(QtGui.QIcon('images/' + p1_siege_line[12] + '.jpg'))
            self.p1_siege_row13.show()
        else:
            self.p1_siege_row13.setEnabled(False)
            self.p1_siege_row13.hide()

        if p1_siege_line_size > 13:
            self.p1_siege_row14.setEnabled(True)
            self.p1_siege_row14.setIcon(QtGui.QIcon('images/' + p1_siege_line[13] + '.jpg'))
            self.p1_siege_row14.show()
        else:
            self.p1_siege_row14.setEnabled(False)
            self.p1_siege_row14.hide()

        if p1_siege_line_size > 14:
            self.p1_siege_row15.setEnabled(True)
            self.p1_siege_row15.setIcon(QtGui.QIcon('images/' + p1_siege_line[14] + '.jpg'))
            self.p1_siege_row15.show()
        else:
            self.p1_siege_row15.setEnabled(False)
            self.p1_siege_row15.hide()

        if p1_siege_line_size > 15:
            self.p1_siege_row16.setEnabled(True)
            self.p1_siege_row16.setIcon(QtGui.QIcon('images/' + p1_siege_line[15] + '.jpg'))
            self.p1_siege_row16.show()
        else:
            self.p1_siege_row16.setEnabled(False)
            self.p1_siege_row16.hide()

        if p1_siege_line_size > 16:
            self.p1_siege_row17.setEnabled(True)
            self.p1_siege_row17.setIcon(QtGui.QIcon('images/' + p1_siege_line[16] + '.jpg'))
            self.p1_siege_row17.show()
        else:
            self.p1_siege_row17.setEnabled(False)
            self.p1_siege_row17.hide()

        if p1_siege_line_size > 17:
            self.p1_siege_row18.setEnabled(True)
            self.p1_siege_row18.setIcon(QtGui.QIcon('images/' + p1_siege_line[17] + '.jpg'))
            self.p1_siege_row18.show()
        else:
            self.p1_siege_row18.setEnabled(False)
            self.p1_siege_row18.hide()

        if p1_siege_line_size > 18:
            self.p1_siege_row19.setEnabled(True)
            self.p1_siege_row19.setIcon(QtGui.QIcon('images/' + p1_siege_line[18] + '.jpg'))
            self.p1_siege_row19.show()
        else:
            self.p1_siege_row19.setEnabled(False)
            self.p1_siege_row19.hide()

        if p1_siege_line_size > 19:
            self.p1_siege_row20.setEnabled(True)
            self.p1_siege_row20.setIcon(QtGui.QIcon('images/' + p1_siege_line[19] + '.jpg'))
            self.p1_siege_row20.show()
        else:
            self.p1_siege_row20.setEnabled(False)
            self.p1_siege_row20.hide()

    def drawCurrentP2MeleeLine(self, p2_melee_line):
        p2_melee_line_size = len(p2_melee_line)

        if p2_melee_line_size > 0:
            self.p2_melee_row01.setEnabled(True)
            self.p2_melee_row01.setIcon(QtGui.QIcon('images/' + p2_melee_line[0] + '.jpg'))
            self.p2_melee_row01.show()
        else:
            self.p2_melee_row01.setEnabled(False)
            self.p2_melee_row01.hide()

        if p2_melee_line_size > 1:
            self.p2_melee_row02.setEnabled(True)
            self.p2_melee_row02.setIcon(QtGui.QIcon('images/' + p2_melee_line[1] + '.jpg'))
            self.p2_melee_row02.show()
        else:
            self.p2_melee_row02.setEnabled(False)
            self.p2_melee_row02.hide()

        if p2_melee_line_size > 2:
            self.p2_melee_row03.setEnabled(True)
            self.p2_melee_row03.setIcon(QtGui.QIcon('images/' + p2_melee_line[2] + '.jpg'))
            self.p2_melee_row03.show()
        else:
            self.p2_melee_row03.setEnabled(False)
            self.p2_melee_row03.hide()

        if p2_melee_line_size > 3:
            self.p2_melee_row04.setEnabled(True)
            self.p2_melee_row04.setIcon(QtGui.QIcon('images/' + p2_melee_line[3] + '.jpg'))
            self.p2_melee_row04.show()
        else:
            self.p2_melee_row04.setEnabled(False)
            self.p2_melee_row04.hide()

        if p2_melee_line_size > 4:
            self.p2_melee_row05.setEnabled(True)
            self.p2_melee_row05.setIcon(QtGui.QIcon('images/' + p2_melee_line[4] + '.jpg'))
            self.p2_melee_row05.show()
        else:
            self.p2_melee_row05.setEnabled(False)
            self.p2_melee_row05.hide()

        if p2_melee_line_size > 5:
            self.p2_melee_row06.setEnabled(True)
            self.p2_melee_row06.setIcon(QtGui.QIcon('images/' + p2_melee_line[5] + '.jpg'))
            self.p2_melee_row06.show()
        else:
            self.p2_melee_row06.setEnabled(False)
            self.p2_melee_row06.hide()

        if p2_melee_line_size > 6:
            self.p2_melee_row07.setEnabled(True)
            self.p2_melee_row07.setIcon(QtGui.QIcon('images/' + p2_melee_line[6] + '.jpg'))
            self.p2_melee_row07.show()
        else:
            self.p2_melee_row07.setEnabled(False)
            self.p2_melee_row07.hide()

        if p2_melee_line_size > 7:
            self.p2_melee_row08.setEnabled(True)
            self.p2_melee_row08.setIcon(QtGui.QIcon('images/' + p2_melee_line[7] + '.jpg'))
            self.p2_melee_row08.show()
        else:
            self.p2_melee_row08.setEnabled(False)
            self.p2_melee_row08.hide()

        if p2_melee_line_size > 8:
            self.p2_melee_row09.setEnabled(True)
            self.p2_melee_row09.setIcon(QtGui.QIcon('images/' + p2_melee_line[8] + '.jpg'))
            self.p2_melee_row09.show()
        else:
            self.p2_melee_row09.setEnabled(False)
            self.p2_melee_row09.hide()

        if p2_melee_line_size > 9:
            self.p2_melee_row10.setEnabled(True)
            self.p2_melee_row10.setIcon(QtGui.QIcon('images/' + p2_melee_line[9] + '.jpg'))
            self.p2_melee_row10.show()
        else:
            self.p2_melee_row10.setEnabled(False)
            self.p2_melee_row10.hide()

        if p2_melee_line_size > 10:
            self.p2_melee_row11.setEnabled(True)
            self.p2_melee_row11.setIcon(QtGui.QIcon('images/' + p2_melee_line[10] + '.jpg'))
            self.p2_melee_row11.show()
        else:
            self.p2_melee_row11.setEnabled(False)
            self.p2_melee_row11.hide()

        if p2_melee_line_size > 11:
            self.p2_melee_row12.setEnabled(True)
            self.p2_melee_row12.setIcon(QtGui.QIcon('images/' + p2_melee_line[11] + '.jpg'))
            self.p2_melee_row12.show()
        else:
            self.p2_melee_row12.setEnabled(False)
            self.p2_melee_row12.hide()

        if p2_melee_line_size > 12:
            self.p2_melee_row13.setEnabled(True)
            self.p2_melee_row13.setIcon(QtGui.QIcon('images/' + p2_melee_line[12] + '.jpg'))
            self.p2_melee_row13.show()
        else:
            self.p2_melee_row13.setEnabled(False)
            self.p2_melee_row13.hide()

        if p2_melee_line_size > 13:
            self.p2_melee_row14.setEnabled(True)
            self.p2_melee_row14.setIcon(QtGui.QIcon('images/' + p2_melee_line[13] + '.jpg'))
            self.p2_melee_row14.show()
        else:
            self.p2_melee_row14.setEnabled(False)
            self.p2_melee_row14.hide()

        if p2_melee_line_size > 14:
            self.p2_melee_row15.setEnabled(True)
            self.p2_melee_row15.setIcon(QtGui.QIcon('images/' + p2_melee_line[14] + '.jpg'))
            self.p2_melee_row15.show()
        else:
            self.p2_melee_row15.setEnabled(False)
            self.p2_melee_row15.hide()

        if p2_melee_line_size > 15:
            self.p2_melee_row16.setEnabled(True)
            self.p2_melee_row16.setIcon(QtGui.QIcon('images/' + p2_melee_line[15] + '.jpg'))
            self.p2_melee_row16.show()
        else:
            self.p2_melee_row16.setEnabled(False)
            self.p2_melee_row16.hide()

        if p2_melee_line_size > 16:
            self.p2_melee_row17.setEnabled(True)
            self.p2_melee_row17.setIcon(QtGui.QIcon('images/' + p2_melee_line[16] + '.jpg'))
            self.p2_melee_row17.show()
        else:
            self.p2_melee_row17.setEnabled(False)
            self.p2_melee_row17.hide()

        if p2_melee_line_size > 17:
            self.p2_melee_row18.setEnabled(True)
            self.p2_melee_row18.setIcon(QtGui.QIcon('images/' + p2_melee_line[17] + '.jpg'))
            self.p2_melee_row18.show()
        else:
            self.p2_melee_row18.setEnabled(False)
            self.p2_melee_row18.hide()

        if p2_melee_line_size > 18:
            self.p2_melee_row19.setEnabled(True)
            self.p2_melee_row19.setIcon(QtGui.QIcon('images/' + p2_melee_line[18] + '.jpg'))
            self.p2_melee_row19.show()
        else:
            self.p2_melee_row19.setEnabled(False)
            self.p2_melee_row19.hide()

        if p2_melee_line_size > 19:
            self.p2_melee_row20.setEnabled(True)
            self.p2_melee_row20.setIcon(QtGui.QIcon('images/' + p2_melee_line[19] + '.jpg'))
            self.p2_melee_row20.show()
        else:
            self.p2_melee_row20.setEnabled(False)
            self.p2_melee_row20.hide()

    def drawCurrentP2RangedLine(self, p2_ranged_line):
        p2_ranged_line_size = len(p2_ranged_line)

        if p2_ranged_line_size > 0:
            self.p2_ranged_row01.setEnabled(True)
            self.p2_ranged_row01.setIcon(QtGui.QIcon('images/' + p2_ranged_line[0] + '.jpg'))
            self.p2_ranged_row01.show()
        else:
            self.p2_ranged_row01.setEnabled(False)
            self.p2_ranged_row01.hide()

        if p2_ranged_line_size > 1:
            self.p2_ranged_row02.setEnabled(True)
            self.p2_ranged_row02.setIcon(QtGui.QIcon('images/' + p2_ranged_line[1] + '.jpg'))
            self.p2_ranged_row02.show()
        else:
            self.p2_ranged_row02.setEnabled(False)
            self.p2_ranged_row02.hide()

        if p2_ranged_line_size > 2:
            self.p2_ranged_row03.setEnabled(True)
            self.p2_ranged_row03.setIcon(QtGui.QIcon('images/' + p2_ranged_line[2] + '.jpg'))
            self.p2_ranged_row03.show()
        else:
            self.p2_ranged_row03.setEnabled(False)
            self.p2_ranged_row03.hide()

        if p2_ranged_line_size > 3:
            self.p2_ranged_row04.setEnabled(True)
            self.p2_ranged_row04.setIcon(QtGui.QIcon('images/' + p2_ranged_line[3] + '.jpg'))
            self.p2_ranged_row04.show()
        else:
            self.p2_ranged_row04.setEnabled(False)
            self.p2_ranged_row04.hide()

        if p2_ranged_line_size > 4:
            self.p2_ranged_row05.setEnabled(True)
            self.p2_ranged_row05.setIcon(QtGui.QIcon('images/' + p2_ranged_line[4] + '.jpg'))
            self.p2_ranged_row05.show()
        else:
            self.p2_ranged_row05.setEnabled(False)
            self.p2_ranged_row05.hide()

        if p2_ranged_line_size > 5:
            self.p2_ranged_row06.setEnabled(True)
            self.p2_ranged_row06.setIcon(QtGui.QIcon('images/' + p2_ranged_line[5] + '.jpg'))
            self.p2_ranged_row06.show()
        else:
            self.p2_ranged_row06.setEnabled(False)
            self.p2_ranged_row06.hide()

        if p2_ranged_line_size > 6:
            self.p2_ranged_row07.setEnabled(True)
            self.p2_ranged_row07.setIcon(QtGui.QIcon('images/' + p2_ranged_line[6] + '.jpg'))
            self.p2_ranged_row07.show()
        else:
            self.p2_ranged_row07.setEnabled(False)
            self.p2_ranged_row07.hide()

        if p2_ranged_line_size > 7:
            self.p2_ranged_row08.setEnabled(True)
            self.p2_ranged_row08.setIcon(QtGui.QIcon('images/' + p2_ranged_line[7] + '.jpg'))
            self.p2_ranged_row08.show()
        else:
            self.p2_ranged_row08.setEnabled(False)
            self.p2_ranged_row08.hide()

        if p2_ranged_line_size > 8:
            self.p2_ranged_row09.setEnabled(True)
            self.p2_ranged_row09.setIcon(QtGui.QIcon('images/' + p2_ranged_line[8] + '.jpg'))
            self.p2_ranged_row09.show()
        else:
            self.p2_ranged_row09.setEnabled(False)
            self.p2_ranged_row09.hide()

        if p2_ranged_line_size > 9:
            self.p2_ranged_row10.setEnabled(True)
            self.p2_ranged_row10.setIcon(QtGui.QIcon('images/' + p2_ranged_line[9] + '.jpg'))
            self.p2_ranged_row10.show()
        else:
            self.p2_ranged_row10.setEnabled(False)
            self.p2_ranged_row10.hide()

        if p2_ranged_line_size > 10:
            self.p2_ranged_row11.setEnabled(True)
            self.p2_ranged_row11.setIcon(QtGui.QIcon('images/' + p2_ranged_line[10] + '.jpg'))
            self.p2_ranged_row11.show()
        else:
            self.p2_ranged_row11.setEnabled(False)
            self.p2_ranged_row11.hide()

        if p2_ranged_line_size > 11:
            self.p2_ranged_row12.setEnabled(True)
            self.p2_ranged_row12.setIcon(QtGui.QIcon('images/' + p2_ranged_line[11] + '.jpg'))
            self.p2_ranged_row12.show()
        else:
            self.p2_ranged_row12.setEnabled(False)
            self.p2_ranged_row12.hide()

        if p2_ranged_line_size > 12:
            self.p2_ranged_row13.setEnabled(True)
            self.p2_ranged_row13.setIcon(QtGui.QIcon('images/' + p2_ranged_line[12] + '.jpg'))
            self.p2_ranged_row13.show()
        else:
            self.p2_ranged_row13.setEnabled(False)
            self.p2_ranged_row13.hide()

        if p2_ranged_line_size > 13:
            self.p2_ranged_row14.setEnabled(True)
            self.p2_ranged_row14.setIcon(QtGui.QIcon('images/' + p2_ranged_line[13] + '.jpg'))
            self.p2_ranged_row14.show()
        else:
            self.p2_ranged_row14.setEnabled(False)
            self.p2_ranged_row14.hide()

        if p2_ranged_line_size > 14:
            self.p2_ranged_row15.setEnabled(True)
            self.p2_ranged_row15.setIcon(QtGui.QIcon('images/' + p2_ranged_line[14] + '.jpg'))
            self.p2_ranged_row15.show()
        else:
            self.p2_ranged_row15.setEnabled(False)
            self.p2_ranged_row15.hide()

        if p2_ranged_line_size > 15:
            self.p2_ranged_row16.setEnabled(True)
            self.p2_ranged_row16.setIcon(QtGui.QIcon('images/' + p2_ranged_line[15] + '.jpg'))
            self.p2_ranged_row16.show()
        else:
            self.p2_ranged_row16.setEnabled(False)
            self.p2_ranged_row16.hide()

        if p2_ranged_line_size > 16:
            self.p2_ranged_row17.setEnabled(True)
            self.p2_ranged_row17.setIcon(QtGui.QIcon('images/' + p2_ranged_line[16] + '.jpg'))
            self.p2_ranged_row17.show()
        else:
            self.p2_ranged_row17.setEnabled(False)
            self.p2_ranged_row17.hide()

        if p2_ranged_line_size > 17:
            self.p2_ranged_row18.setEnabled(True)
            self.p2_ranged_row18.setIcon(QtGui.QIcon('images/' + p2_ranged_line[17] + '.jpg'))
            self.p2_ranged_row18.show()
        else:
            self.p2_ranged_row18.setEnabled(False)
            self.p2_ranged_row18.hide()

        if p2_ranged_line_size > 18:
            self.p2_ranged_row19.setEnabled(True)
            self.p2_ranged_row19.setIcon(QtGui.QIcon('images/' + p2_ranged_line[18] + '.jpg'))
            self.p2_ranged_row19.show()
        else:
            self.p2_ranged_row19.setEnabled(False)
            self.p2_ranged_row19.hide()

        if p2_ranged_line_size > 19:
            self.p2_ranged_row20.setEnabled(True)
            self.p2_ranged_row20.setIcon(QtGui.QIcon('images/' + p2_ranged_line[19] + '.jpg'))
            self.p2_ranged_row20.show()
        else:
            self.p2_ranged_row20.setEnabled(False)
            self.p2_ranged_row20.hide()

    def drawCurrentP2SiegeLine(self, p2_siege_line):
        p2_siege_line_size = len(p2_siege_line)

        if p2_siege_line_size > 0:
            self.p2_siege_row01.setEnabled(True)
            self.p2_siege_row01.setIcon(QtGui.QIcon('images/' + p2_siege_line[0] + '.jpg'))
            self.p2_siege_row01.show()
        else:
            self.p2_siege_row01.setEnabled(False)
            self.p2_siege_row01.hide()

        if p2_siege_line_size > 1:
            self.p2_siege_row02.setEnabled(True)
            self.p2_siege_row02.setIcon(QtGui.QIcon('images/' + p2_siege_line[1] + '.jpg'))
            self.p2_siege_row02.show()
        else:
            self.p2_siege_row02.setEnabled(False)
            self.p2_siege_row02.hide()

        if p2_siege_line_size > 2:
            self.p2_siege_row03.setEnabled(True)
            self.p2_siege_row03.setIcon(QtGui.QIcon('images/' + p2_siege_line[2] + '.jpg'))
            self.p2_siege_row03.show()
        else:
            self.p2_siege_row03.setEnabled(False)
            self.p2_siege_row03.hide()

        if p2_siege_line_size > 3:
            self.p2_siege_row04.setEnabled(True)
            self.p2_siege_row04.setIcon(QtGui.QIcon('images/' + p2_siege_line[3] + '.jpg'))
            self.p2_siege_row04.show()
        else:
            self.p2_siege_row04.setEnabled(False)
            self.p2_siege_row04.hide()

        if p2_siege_line_size > 4:
            self.p2_siege_row05.setEnabled(True)
            self.p2_siege_row05.setIcon(QtGui.QIcon('images/' + p2_siege_line[4] + '.jpg'))
            self.p2_siege_row05.show()
        else:
            self.p2_siege_row05.setEnabled(False)
            self.p2_siege_row05.hide()

        if p2_siege_line_size > 5:
            self.p2_siege_row06.setEnabled(True)
            self.p2_siege_row06.setIcon(QtGui.QIcon('images/' + p2_siege_line[5] + '.jpg'))
            self.p2_siege_row06.show()
        else:
            self.p2_siege_row06.setEnabled(False)
            self.p2_siege_row06.hide()

        if p2_siege_line_size > 6:
            self.p2_siege_row07.setEnabled(True)
            self.p2_siege_row07.setIcon(QtGui.QIcon('images/' + p2_siege_line[6] + '.jpg'))
            self.p2_siege_row07.show()
        else:
            self.p2_siege_row07.setEnabled(False)
            self.p2_siege_row07.hide()

        if p2_siege_line_size > 7:
            self.p2_siege_row08.setEnabled(True)
            self.p2_siege_row08.setIcon(QtGui.QIcon('images/' + p2_siege_line[7] + '.jpg'))
            self.p2_siege_row08.show()
        else:
            self.p2_siege_row08.setEnabled(False)
            self.p2_siege_row08.hide()

        if p2_siege_line_size > 8:
            self.p2_siege_row09.setEnabled(True)
            self.p2_siege_row09.setIcon(QtGui.QIcon('images/' + p2_siege_line[8] + '.jpg'))
            self.p2_siege_row09.show()
        else:
            self.p2_siege_row09.setEnabled(False)
            self.p2_siege_row09.hide()

        if p2_siege_line_size > 9:
            self.p2_siege_row10.setEnabled(True)
            self.p2_siege_row10.setIcon(QtGui.QIcon('images/' + p2_siege_line[9] + '.jpg'))
            self.p2_siege_row10.show()
        else:
            self.p2_siege_row10.setEnabled(False)
            self.p2_siege_row10.hide()

        if p2_siege_line_size > 10:
            self.p2_siege_row11.setEnabled(True)
            self.p2_siege_row11.setIcon(QtGui.QIcon('images/' + p2_siege_line[10] + '.jpg'))
            self.p2_siege_row11.show()
        else:
            self.p2_siege_row11.setEnabled(False)
            self.p2_siege_row11.hide()

        if p2_siege_line_size > 11:
            self.p2_siege_row12.setEnabled(True)
            self.p2_siege_row12.setIcon(QtGui.QIcon('images/' + p2_siege_line[11] + '.jpg'))
            self.p2_siege_row12.show()
        else:
            self.p2_siege_row12.setEnabled(False)
            self.p2_siege_row12.hide()

        if p2_siege_line_size > 12:
            self.p2_siege_row13.setEnabled(True)
            self.p2_siege_row13.setIcon(QtGui.QIcon('images/' + p2_siege_line[12] + '.jpg'))
            self.p2_siege_row13.show()
        else:
            self.p2_siege_row13.setEnabled(False)
            self.p2_siege_row13.hide()

        if p2_siege_line_size > 13:
            self.p2_siege_row14.setEnabled(True)
            self.p2_siege_row14.setIcon(QtGui.QIcon('images/' + p2_siege_line[13] + '.jpg'))
            self.p2_siege_row14.show()
        else:
            self.p2_siege_row14.setEnabled(False)
            self.p2_siege_row14.hide()

        if p2_siege_line_size > 14:
            self.p2_siege_row15.setEnabled(True)
            self.p2_siege_row15.setIcon(QtGui.QIcon('images/' + p2_siege_line[14] + '.jpg'))
            self.p2_siege_row15.show()
        else:
            self.p2_siege_row15.setEnabled(False)
            self.p2_siege_row15.hide()

        if p2_siege_line_size > 15:
            self.p2_siege_row16.setEnabled(True)
            self.p2_siege_row16.setIcon(QtGui.QIcon('images/' + p2_siege_line[15] + '.jpg'))
            self.p2_siege_row16.show()
        else:
            self.p2_siege_row16.setEnabled(False)
            self.p2_siege_row16.hide()

        if p2_siege_line_size > 16:
            self.p2_siege_row17.setEnabled(True)
            self.p2_siege_row17.setIcon(QtGui.QIcon('images/' + p2_siege_line[16] + '.jpg'))
            self.p2_siege_row17.show()
        else:
            self.p2_siege_row17.setEnabled(False)
            self.p2_siege_row17.hide()

        if p2_siege_line_size > 17:
            self.p2_siege_row18.setEnabled(True)
            self.p2_siege_row18.setIcon(QtGui.QIcon('images/' + p2_siege_line[17] + '.jpg'))
            self.p2_siege_row18.show()
        else:
            self.p2_siege_row18.setEnabled(False)
            self.p2_siege_row18.hide()

        if p2_siege_line_size > 18:
            self.p2_siege_row19.setEnabled(True)
            self.p2_siege_row19.setIcon(QtGui.QIcon('images/' + p2_siege_line[18] + '.jpg'))
            self.p2_siege_row19.show()
        else:
            self.p2_siege_row19.setEnabled(False)
            self.p2_siege_row19.hide()

        if p2_siege_line_size > 19:
            self.p2_siege_row20.setEnabled(True)
            self.p2_siege_row20.setIcon(QtGui.QIcon('images/' + p2_siege_line[19] + '.jpg'))
            self.p2_siege_row20.show()
        else:
            self.p2_siege_row20.setEnabled(False)
            self.p2_siege_row20.hide()

def main():
    app = QtGui.QApplication(sys.argv)
    form = mainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()                          # run the main function