# ####################################
#
# File: TestScoreCard.py
# Auth: Gerik Peterson
# Desc: Unit Test File for the ScoreCard Class
#
# ####################################

import unittest
from src.ScoreCard import ScoreCard

# Utility Functions
def get_empty_score_card():
    return [
        {'bowls': [], 'total': 0}, 
        {'bowls': [], 'total': 0}, 
        {'bowls': [], 'total': 0}, 
        {'bowls': [], 'total': 0}, 
        {'bowls': [], 'total': 0}, 
        {'bowls': [], 'total': 0}, 
        {'bowls': [], 'total': 0},
        {'bowls': [], 'total': 0},
        {'bowls': [], 'total': 0},
        {'bowls': [], 'total': 0}]

def get_full_score_card():
    return [
        {'bowls': [0,0], 'total': 0},
        {'bowls': [0,0], 'total': 0},
        {'bowls': [0,0], 'total': 0},
        {'bowls': [0,0], 'total': 0},
        {'bowls': [0,0], 'total': 0},
        {'bowls': [0,0], 'total': 0},
        {'bowls': [0,0], 'total': 0},
        {'bowls': [0,0], 'total': 0},
        {'bowls': [0,0], 'total': 0},
        {'bowls': [0,0,0], 'total': 0}]

class TestScoreCard(unittest.TestCase):

    def setUp(self):
        self.sc = ScoreCard()
        frames = [{"bowls":[],"total":0} for i in range(10)]
        self.exp_state = {"status" : "open", "scores" : frames, "game_total" : 0}

    def test_register_first_bowl(self):
        self.exp_state["scores"] = get_empty_score_card()
        self.exp_state["scores"][0]["bowls"].append(5)
        self.exp_state["scores"][0]["total"] = 5
        self.exp_state["game_total"] = 5
        self.assertEqual(self.sc.bowl(5),self.exp_state)

    def test_too_many_bowls(self):
        self.sc.frame_idx = 10
        self.exp_state["scores"] = get_empty_score_card()
        self.exp_state["status"] = "fin"
        self.assertEqual(self.sc.bowl(1),self.exp_state)

    def test_negative_pins(self):
        self.assertEquals(self.sc.bowl(-1),self.exp_state)    

    def test_more_than_ten_pins(self):
        self.sc.bowl(5)
        self.exp_state["scores"] = get_empty_score_card()
        self.exp_state["scores"][0]["bowls"].append(5)
        self.exp_state["scores"][0]["total"] = 5
        self.exp_state["game_total"] = 5
        self.assertEqual(self.sc.bowl(9), self.exp_state)

    def test_four_simple_bowls(self):
        self.sc.bowl(3)
        self.sc.bowl(3)
        self.sc.bowl(3)
        self.sc.bowl(3)
        self.exp_state["scores"] = get_empty_score_card()
        self.exp_state["scores"][0]["bowls"].append(3)
        self.exp_state["scores"][0]["total"] = 3
        self.exp_state["scores"][0]["bowls"].append(3)
        self.exp_state["scores"][0]["total"] = 6
        self.exp_state["scores"][1]["bowls"].append(3)
        self.exp_state["scores"][1]["total"] = 3
        self.exp_state["scores"][1]["bowls"].append(3)
        self.exp_state["scores"][1]["total"] = 6
        self.exp_state["game_total"] = 12
        self.assertEqual(self.sc.get_game_state(),self.exp_state)

    def test_full_game_all_strikes(self):
        for i in range(12):
            self.sc.bowl(10)
        self.exp_state["scores"] = [
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10,10,10], 'total': 30}]
        self.exp_state["game_total"] = 300
        self.exp_state["status"] = "fin"
        self.assertEqual(self.sc.get_game_state(),self.exp_state)

    def test_strike_spare_strike_spare_spare_norm(self):
        self.sc.bowl(10)
        self.sc.bowl(5)
        self.sc.bowl(5)
        self.sc.bowl(10)
        self.sc.bowl(7)
        self.sc.bowl(3)
        self.sc.bowl(4)
        self.sc.bowl(6)
        self.sc.bowl(0)
        self.exp_state["scores"] = [
            {'bowls': [10], 'total': 20},
            {'bowls': [5,5], 'total': 20},
            {'bowls': [10], 'total': 20},
            {'bowls': [7,3], 'total': 14},
            {'bowls': [4,6], 'total': 10},
            {'bowls': [0], 'total': 0},
            {'bowls': [], 'total': 0},
            {'bowls': [], 'total': 0},
            {'bowls': [], 'total': 0},
            {'bowls': [], 'total': 0}]
        self.exp_state["game_total"] = 84
        self.exp_state["status"] = "open"
        self.assertEqual(self.sc.get_game_state(),self.exp_state)

    def test_final_frame_miss_second_bowl(self):
        self.maxDiff = None
        for i in range(9):
           self.sc.bowl(10)
        self.sc.bowl(1)
        self.sc.bowl(0)
        self.exp_state["scores"] = [
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 30},
            {'bowls': [10], 'total': 21},
            {'bowls': [10], 'total': 11},
            {'bowls': [1,0], 'total': 1}]
        self.exp_state["game_total"] = 243
        self.exp_state["status"] = "fin"
        self.assertEqual(self.sc.get_game_state(),self.exp_state)



