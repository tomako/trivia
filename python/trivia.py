#!/usr/bin/env python
import sys, StringIO

WRONG_ANSWER = 7

oldstdout = sys.stdout

sys.stdout = StringIO.StringIO()


class Player:
    def __init__(self, name):
        self.name = name
        self.place = 0
        self.purse = 0
        self.in_penalty_box = False

    def won(self):
        return self.purse == 6

    def question_correctly_answered(self, legacy):
        print 'Answer was correct!!!!'
        self.purse += 1
        print self.name + \
              ' now has ' + \
              str(self.purse) + \
              ' Gold Coins.'
        winner = self.won()
        if not legacy:
            self.in_penalty_box = False
        return winner


class Game:
    question_types = ["Pop", "Science", "Sports", "Rock"]

    def create_all_questions(self):
        for question in self.question_types:
            self.questions[question] = []

        for i in range(50):
            for question in self.question_types:
                self.questions[question].append(self.create_question(question,i))

    def __init__(self, legacy):
        self.legacy = legacy
        self.players = []
        self.current_player_index = 0

        self.questions = {}
        
        self.is_getting_out_of_penalty_box = False

        self.create_all_questions()

    def create_question(self, qtype, index):
        return "%s Question %s" % (qtype,index)
    
    #def is_playable(self):
    #    return self.how_many_players >= 2
    
    def add_player(self, player_name):
        self.players.append(Player(player_name))
        
        print player_name + " was added"
        print "They are player number %s" % self.number_of_players
        
        return True

    @property
    def current_player(self):
        return self.players[self.current_player_index]
    
    @property
    def number_of_players(self):
        return len(self.players)

    def advance_player_to_next_place(self, roll):
        self.current_player.place = (self.current_player.place + roll) % 12
        print self.current_player.name + \
              '\'s new location is ' + \
              str(self.current_player.place)

    def can_get_out_of_penalty(self, roll):
        return roll % 2 != 0

    def roll(self, roll):
        print "%s is the current player" % self.current_player.name
        print "They have rolled a %s" % roll
        
        if self.current_player.in_penalty_box:
            if self.can_get_out_of_penalty(roll):
                self.is_getting_out_of_penalty_box = True
                print "%s is getting out of the penalty box" % self.current_player.name
            else:
                print "%s is not getting out of the penalty box" % self.current_player.name
                self.is_getting_out_of_penalty_box = False

        if not self.current_player.in_penalty_box or self.is_getting_out_of_penalty_box:
            self.advance_player_to_next_place(roll)
            print "The category is %s" % self._current_category
            self._ask_question()
    
    def _ask_question(self):
        print self.questions[self._current_category].pop(0)
    
    @property
    def _current_category(self):
        return self.question_types[self.current_player.place % len(self.question_types)]

    def jump_to_next_player(self):
        self.current_player_index += 1
        if self.current_player_index == self.number_of_players: self.current_player_index = 0

    def correct_answer(self):
        result = True
        if not self.current_player.in_penalty_box or self.is_getting_out_of_penalty_box:
            result = self.current_player.question_correctly_answered(self.legacy)
        return result
    
    def wrong_answer(self):
        print 'Question was incorrectly answered'
        print self.current_player.name + " was sent to the penalty box"
        self.current_player.in_penalty_box = True

        return True

    def do_answer(self, answer):
        if answer == WRONG_ANSWER:
            has_winner = self.wrong_answer()
        else:
            has_winner = self.correct_answer()
        self.jump_to_next_player()
        return has_winner


from random import randrange

class Random:
    i = 0

    def __init__(self, seq):
        self.seq = seq

    def range(self, max):
        value = self.seq[self.i]
        self.i = self.i + 1
        return value


class RandomSaver:
    seq = []
    def range(self, max):
        value = randrange(max)
        self.seq.append(value)
        return value


def run(rnd):
    has_winner = False

    game = Game(True)

    game.add_player('Chet')
    game.add_player('Pat')
    game.add_player('Sue')

    while True:
        game.roll(rnd.range(5) + 1)

        answer = rnd.range(9)
        has_winner = game.do_answer(answer)
        
        if has_winner: break

if __name__ == '__main__':
    rnd = RandomSaver()

    run(rnd)

    actual = sys.stdout.getvalue()
    sys.stdout = oldstdout
    f = open("test2.txt", "w")
    f.write(actual)
    f.close()

    print rnd.seq
