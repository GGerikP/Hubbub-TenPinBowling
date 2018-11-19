#!/usr/bin/python3

# #############################################
#
# File: ScoreCard.py
# Auth: Gerik Peterson
# Desc: Ten Pin Bowling Score Keeper
#
# #############################################

# Imports
import os
import warnings

class ScoreCard():

    def __init__(self):
        self.frame_count = 10
        self.frames = [{"bowls":[],"total":0} for i in range(self.frame_count)]
        self.max_bonus_frames = 2
        self.frame_idx = 0
        self.ball = 0
        self.game_total = 0
        self.status = "open"

    def get_game_state(self):
        '''
        get_game_state: public method to get a consumer the state of the game
        '''
        return {"status" : self.status, "scores" : self.frames, "game_total" : self.game_total}


    def bowl(self,ko_pins):
        '''
        bowl: public method to move the game forward
        Input: knocked over pin count
        Ouput: A dict containing the state of the game
        '''

        # Don't let us over bowl
        if self.frame_idx >= self.frame_count:
            self.status = "fin"
            return self.get_game_state()

        # Store the current ball score if it's valid
        try:
            ko_pins = int(ko_pins)
        except ValueError:
            warnings.warn("Bad Pin Value.  Rejecting.")
            return self.get_game_state()

        if self.__validate_bowl(ko_pins):
            self.frames[self.frame_idx]["bowls"].append(ko_pins)
            self.frames[self.frame_idx]["total"] += ko_pins
            self.game_total += ko_pins
        else:
            return self.get_game_state()

        # Add the bonuses
        self.__add_bonuses(ko_pins)

        # Prepare for the next bowl
        self.__prepare_next_bowl(ko_pins)

        if self.frame_idx >= self.frame_count:
            self.status = "fin"

        return self.get_game_state()


    def __validate_bowl(self,ko_pins):
        # Scenarios to check:
        # - number
        # - positive
        # - for all frames except the last first and second bowl are not more than 10 pins
        if not str(ko_pins).isdigit() or ko_pins < 0:
            return False
        elif self.frame_idx != self.frame_count - 1 and self.ball > 0 and (ko_pins + self.frames[self.frame_idx]["bowls"][0] > 10):
            warnings.warn("Impossible pin count.  Rejecting.")
            return False
        else:
            return True


    def __prepare_next_bowl(self, ko_pins):
        '''
        __prepare_next_frame: private method to prepare the next bowl
        '''
        # All the frames before the last...
        if self.frame_idx < self.frame_count - 1:
            # ...we're just resetting the ball count
            if self.ball == 1 or ko_pins == 10:
                self.ball = 0
                self.frame_idx += 1
            else:
                self.ball += 1
        elif self.frame_idx == self.frame_count - 1:
            # The last frame we need to figure out if we 
            # give them a third ball or not
            if self.ball >= 2:
                self.frame_idx += 1
            elif self.ball >= 1:
                # If this is our second ball, either
                if ko_pins == 10: # we just hit a strike
                    self.ball += 1
                # Or we got a spare
                elif ko_pins > 0 and self.frames[self.frame_idx]["bowls"][0] + ko_pins % 10 == 0:
                    self.ball += 1
                # If we don't get either we move on
                else:
                    self.frame_idx += 1
            else:
                self.ball += 1


    def __add_bonuses(self, ko_pins):

        # For all frames except the last 2 balls of the last frame
        if self.frame_idx < self.frame_count - 1 or (self.frame_idx == self.frame_count - 1 and self.ball == 0):
            self.__add_single_level_strike_bonus(ko_pins)
            self.__add_second_level_strike_bonus(ko_pins)
            self.__add_spare_bonus(ko_pins)
        else:
            self.__add_last_frame_bonus(ko_pins)


    def __add_single_level_strike_bonus(self,ko_pins):
        if self.frame_idx < 1:
            return

        if self.frames[self.frame_idx - 1]["bowls"][0] == 10:
            self.frames[self.frame_idx - 1]["total"] += ko_pins
            self.game_total += ko_pins


    def __add_second_level_strike_bonus(self,ko_pins):
        if self.frame_idx < 2:
            return

        if self.frames[self.frame_idx - 1]["bowls"][0] == 10 and self.frames[self.frame_idx - 2]["bowls"][0] == 10:
            self.frames[self.frame_idx - 2]["total"] += ko_pins;
            self.game_total += ko_pins


    def __add_spare_bonus(self,ko_pins):
        if self.frame_idx < 1 or self.ball > 0:
            return

        if self.frames[self.frame_idx - 1]["bowls"][0] != 10 and sum(self.frames[self.frame_idx - 1]["bowls"]) == 10:
            self.frames[self.frame_idx - 1]["total"] += ko_pins;
            self.game_total += ko_pins

    def __add_last_frame_bonus(self,ko_pins):
        if self.frame_idx != self.frame_count - 1:
            return

        if self.ball < 2 and self.frames[self.frame_idx - 1]["bowls"][0] == 10:
            self.frames[self.frame_idx - 1]["total"] += ko_pins
            self.game_total += ko_pins


