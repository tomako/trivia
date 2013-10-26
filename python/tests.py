import unittest
import trivia
import sys
import StringIO

GOOD_ANSWER = 6
WRONG_ROLL = 0
GOOD_ROLL = 1


class MyTestCase(unittest.TestCase):
    def get_expected_characterization_value(self, filename):
        f = open(filename, "r")
        expected = f.read()
        f.close()
        return expected

    def _test_first(self):
        self.characterization_test("test.txt", [0, 5, 2, 0, 2, 8, 0, 0, 2, 5, 1, 6, 0, 6, 2, 5, 0, 4, 0, 7, 4, 5, 3, 8, 0, 4, 2, 3, 2, 6, 4, 0, 0, 5])

    def _test_second(self):
        self.characterization_test("test2.txt", [1, 2, 3, 8, 2, 1, 3, 4, 1, 4, 0, 4, 4, 5, 4, 1, 1, 0, 1, 0, 1, 4, 2, 4, 4, 1, 4, 4, 0, 5, 0, 7, 3, 1])

    def characterization_test(self,  filename, rnd_seq):
        oldstdout = sys.stdout

        sys.stdout = StringIO.StringIO()
        rnd = trivia.Random(rnd_seq)

        trivia.run(rnd)

        actual = sys.stdout.getvalue()
        sys.stdout = oldstdout

        expected = self.get_expected_characterization_value(filename)

        self.assertEqual(expected, actual)

    def test_good_answer_yields_money(self):
        game = self.setup_game()
        self.iterate_game(GOOD_ANSWER, game, GOOD_ROLL)
        self.assertEqual(game.players[0].purse, 1)

    def setup_game(self, legacy = False):
        game = trivia.Game(legacy)
        game.add_player("Bela")
        return game

    def test_wrong_answer_go_penalty(self):
        game = self.setup_game()
        self.iterate_game(trivia.WRONG_ANSWER, game, GOOD_ROLL)
        self.assertTrue(game.players[0].in_penalty_box)

    def iterate_game(self, answer, game, roll):
        game.roll(roll)
        return game.do_answer(answer)

    def test_wrong_answer_remain_in_penalty_box(self):
        game = self.setup_game()
        self.iterate_game(trivia.WRONG_ANSWER, game, GOOD_ROLL)
        self.iterate_game(trivia.WRONG_ANSWER, game, GOOD_ROLL)
        self.assertTrue(game.players[0].in_penalty_box)

    def test_wrong_roll_remain_in_penalty_box(self):
        game = self.setup_game()
        self.iterate_game(trivia.WRONG_ANSWER, game, GOOD_ROLL)
        self.iterate_game(GOOD_ANSWER, game, WRONG_ROLL)
        self.assertTrue(game.players[0].in_penalty_box)

    def test_penalty_box_bug(self):
        game = self.setup_game()
        self.iterate_game(trivia.WRONG_ANSWER, game, GOOD_ROLL)
        self.iterate_game(GOOD_ANSWER, game, GOOD_ROLL)
        self.assertFalse(game.players[0].in_penalty_box)

    def test_penalty_box_legacy(self):
        game = self.setup_game(True)
        self.iterate_game(trivia.WRONG_ANSWER, game, GOOD_ROLL)
        self.iterate_game(GOOD_ANSWER, game, GOOD_ROLL)
        self.assertTrue(game.players[0].in_penalty_box)

    def test_win_condition(self):
        game = self.setup_game()
        for i in xrange(0,5):
            self.iterate_game(GOOD_ANSWER, game, GOOD_ROLL)
        self.assertTrue(self.iterate_game(GOOD_ANSWER, game, GOOD_ROLL))

if __name__ == '__main__':
    unittest.main()
