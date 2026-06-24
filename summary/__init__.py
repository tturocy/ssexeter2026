from otree.api import *


doc = """
App to display summary of earnings in experiment
"""


class C(BaseConstants):
    NAME_IN_URL = 'summary'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    def collect_results(self):
        for player in self.get_players():
            player.earnings_contest = player.participant.vars.get("earnings_contest", Currency(67))
            player.earnings_encryption = player.participant.vars.get("earnings_encryption", Currency(67))


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    earnings_contest = models.CurrencyField()
    earnings_encryption = models.CurrencyField()



# PAGES
class CollectResults(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.collect_results()


class Results(Page):
    pass


page_sequence = [
    CollectResults,
    Results,
]
