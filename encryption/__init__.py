import string
import time
import random

from otree.api import *


doc = """
Encryption Task
"""


class C(BaseConstants):
    NAME_IN_URL = 'encryption'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    PAYMENT_PER_CORRECT = 0.10
    TIME_FOR_TASK = 100000
    RANDOM_SEED = 12345678


class Subsession(BaseSubsession):
    random_seed = models.IntegerField()
    payment_per_correct = models.CurrencyField()
    lookup_table = models.StringField()
    word = models.StringField()

    def setup_round(self):
        if self.round_number == 1:
            self.random_seed = C.RANDOM_SEED
            random.seed(self.random_seed)
        self.payment_per_correct = Currency(C.PAYMENT_PER_CORRECT)
        self.word = "".join(random.choices(string.ascii_uppercase,k=5))
        self.lookup_table = "".join(random.sample(string.ascii_uppercase,26))

        for player in self.get_players():
            player.setup_round()

    @property
    def lookup_dict(self):
        lookup = {}
        for letter in string.ascii_uppercase:
            lookup[letter] = self.lookup_table.index(letter)+1
        return lookup

    @property
    def correct_response(self):
        return [self.lookup_dict[letter] for letter in self.word]
        return [
            self.lookup_dict[self.word[0]],
            self.lookup_dict[self.word[1]],
            self.lookup_dict[self.word[2]],
            self.lookup_dict[self.word[3]],
            self.lookup_dict[self.word[4]],
        ]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    time_for_task = models.IntegerField()
    response_1 = models.IntegerField()
    response_2 = models.IntegerField()
    response_3 = models.IntegerField()
    response_4 = models.IntegerField()
    response_5 = models.IntegerField()
    is_correct = models.BooleanField()
    started_task_at = models.FloatField()
    # time_elapsed = models.FloatField()
    # time_remaining = models.FloatField()

    def setup_round(self):
        self.time_for_task = C.TIME_FOR_TASK

    def start_task(self):
        self.started_task_at = time.time()

    def get_time_remaining(self):
        # self.time_elapsed = time.time() - self.in_round(1).started_task_at
        # self.time_remaining = self.time_for_task - self.time_elapsed
        return self.time_for_task - (time.time() - self.in_round(1).started_task_at)

    @property
    def response_fields(self):
        return [
            "response_1",
            "response_2",
            "response_3",
            "response_4",
            "response_5",
        ]

    @property
    def response(self):
        return [
            self.response_1,
            self.response_2,
            self.response_3,
            self.response_4,
            self.response_5,
        ]

    def check_response(self):
        self.is_correct = (
            self.response == self.subsession.correct_response
        )
        if self.is_correct:
            self.payoff = self.subsession.payment_per_correct


def creating_session(subsession):
    subsession.setup_round()


# PAGES
class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player,timeout_happened):
        player.start_task()


class Decision(Page):
    form_model = "player"

    @staticmethod
    def get_form_fields(player):
        return player.response_fields

    @staticmethod
    def before_next_page(player,timeout_happened):
        player.check_response()

    @staticmethod
    def get_timeout_seconds(player):
        return player.get_time_remaining()


class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    Intro,
    Decision,
    Results,
]
