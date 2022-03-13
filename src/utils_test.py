import unittest
import utils

class TestIsValid(unittest.TestCase):
    def test_not_square_vector(self):
        v = ['0', '0', '0']
        self.assertRaises(Exception, utils.is_valid, v)
        v = ['0', '0', '0', '0', '0', '0', '0']
        self.assertRaises(Exception, utils.is_valid, v)

    def test_invalid_values(self):
        v = [2, '0', '0', '0', '0', '0', '0', '0', '0']
        self.assertRaises(Exception, utils.is_valid, v)
        v = ['0', '0', '0', '-1']
        self.assertRaises(Exception, utils.is_valid, v)

    def test_is_valid(self):
        v = ['0', '1', '1', '0']
        self.assertTrue(utils.is_valid(v))
        v = ['0', '0', '0', '1']
        self.assertFalse(utils.is_valid(v))

class TestWinnerList(unittest.TestCase):
    def test_two_by_two(self):
        winner_list = [[0, 2], [1, 3], [0, 1], [2, 3], [0, 3], [1, 2]]
        self.assertEqual(winner_list, utils.winner_list(2))
        winner_list = [[0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [2, 4, 6]]
        self.assertEqual(winner_list, utils.winner_list(3))

class TestIsWinner(unittest.TestCase):
    def test_not_winner(self):
        v = ['0', '0', '0', '0']
        self.assertFalse(utils.is_winner(v))
        v = ['1', '0', '0', '0']
        self.assertFalse(utils.is_winner(v))
        v = ['1', '0', '0', '0', '1', '0', '0', '1', '0']
        self.assertFalse(utils.is_winner(v))
        v = ['1', '1', '0', '0', '0', '0', '0', '1', '0']
        self.assertFalse(utils.is_winner(v))
        v = ['1', '1', '0', '1', '1', '0', '0', '0', '0']
        self.assertFalse(utils.is_winner(v))

    def test_horizontal_winner(self):
        v = ['1', '1', '0', '0']
        self.assertTrue(utils.is_winner(v))
        v = ['0', '0', '1', '1']
        self.assertTrue(utils.is_winner(v))
        v = ['1', '1', '1', '0', '0', '0', '0', '0', '0']
        self.assertTrue(utils.is_winner(v))
        v = ['0', '0', '0', '0', '0', '0', '1', '1', '1']
        self.assertTrue(utils.is_winner(v))

    def test_vertical_winner(self):
        v = ['1', '0', '1', '0']
        self.assertTrue(utils.is_winner(v))
        v = ['0', '1', '0', '1']
        self.assertTrue(utils.is_winner(v))
        v = ['1', '0', '0', '1', '0', '0', '1', '0', '0']
        self.assertTrue(utils.is_winner(v))
        v = ['0', '1', '0', '0', '1', '0', '0', '1', '0']
        self.assertTrue(utils.is_winner(v))

    def test_diagonal_winner(self):
        v = ['1', '0', '1', '0']
        self.assertTrue(utils.is_winner(v))
        v = ['0', '1', '0', '1']
        self.assertTrue(utils.is_winner(v))
        v = ['1', '0', '0', '0', '1', '0', '0', '1']
        self.assertTrue(utils.is_winner(v))
        v = ['1', '0', '0', '0', '1', '0', '0', '1']
        self.assertTrue(utils.is_winner(v))

if __name__ == '__main__':
    unittest.main()
