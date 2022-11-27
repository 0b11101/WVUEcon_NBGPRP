from otree.api import *
import random

doc = """
Your app description
"""


# TODO My idea is to generate a string containing all of the randomly generated zeros and ones pass that to the
#  javascript

def generate_matrix_values() -> {str, int, int}:
    row, col, randomizer = 10, 15, random.randint(0, 100000)
    zeros, ones = 0, 0
    data_arr = ''

    for i in range(150):
        if random.randint(0, 100000) < randomizer:
            data_arr += '0'
            zeros += 1
        else:
            data_arr += '1'
            ones += 1

    return [data_arr, zeros, ones]


class C(BaseConstants):
    NAME_IN_URL = 'tedious_observation'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1000  # 100 bc I want the app to be timed

    REWARD = 0.25  # according to the research paper by Dr.Burke
    TIME = [10, 20, 20]


#    string_matrix = generate_matrix_values()[0]
#    zeros = generate_matrix_values()[1]
#    ones = generate_matrix_values()[2]


class Subsession(BaseSubsession):
    stage = models.IntegerField()


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        p.layout = generate_matrix_values()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    num_trials = models.IntegerField(initial=0)
    num_correct = models.IntegerField(initial=0)
    num_correct = models.IntegerField(initial=0)
    time_left = models.FloatField(doc="Stage 1: 10min, Stage 2 and 3: 20 min")
    guess = models.IntegerField(min=0, label="Input the amount of zeros here")


# PAGES


class Counting(Page):
    form_model = 'player'
    form_fields = ['guess']

    def before_next_page(player: Player, timeout_happened):
        if player.guess == C.zeros:
            player.payoff = C.REWARD


class ResultsWaitPage(WaitPage):
    generate_matrix_values()


class Results(Page):
    pass


page_sequence = [Counting, ResultsWaitPage, Results]
