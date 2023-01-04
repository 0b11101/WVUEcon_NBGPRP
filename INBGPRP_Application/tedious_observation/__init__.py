import time
import random
from typing import Dict, Any

from otree.api import *

doc = """
Your app description
"""


def comp_num_generator():
    return random.randint(1, 100)


class C(BaseConstants):
    NAME_IN_URL = 'tedious_observation'
    PLAYERS_PER_GROUP = None
    NUM_PERIODS_PER_GAME = 100  # 1000 bc I want the app to be time
    TIMEOUT_HAPPENS = [10, 20, 20]
    NUM_ROUNDS = 3 * NUM_PERIODS_PER_GAME
    PAYOUT = 0.25
    COMP_NUMBER = comp_num_generator()


class Subsession(BaseSubsession):
    stage = models.IntegerField(initial=0)
    round = models.IntegerField(initial=0)
    is_last_period = models.BooleanField()
    timeout_happened = models.BooleanField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Game info
    num_trials = models.IntegerField(initial=0)
    num_correct = models.IntegerField(initial=0)
    feedback = models.StringField(initial="You\'ll see feedback here")

    # Player input
    table_goal = models.IntegerField(blank=True, intitial=10, label="Table Goal (Optional)")
    comprehension_input = models.IntegerField()
    zeros_guess = models.IntegerField(min=0, label="Input the amount of zeros here")

    # Validation
    zeros_actual = models.IntegerField()
    ones = models.IntegerField()


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        ses_stage = 1
        ses_round = 1
        timeout = False
        # loop to go through subsessions
        for ss in subsession.in_rounds(1, C.NUM_ROUNDS):
            ss.stage = ses_stage
            ss.round = ses_round
            ss.timeout_happened = timeout
            ss.is_last_period = ses_round == C.NUM_PERIODS_PER_GAME
            if ss.is_last_period or ss.timeout_happened:
                ses_stage += 1
                ses_round = 1
                ss.timeout_happened = False
            else:
                ses_round += 1


def matrix_creation(player: Player) -> [str, int, int]:
    row, col, randomizer = 10, 15, random.randint(0, 100000)
    zeros, ones = 0, 0
    matrix = ''

    for i in range(150):
        if random.randint(0, 100000) < randomizer:
            matrix += '0'
            zeros += 1
        else:
            matrix += '1'
            ones += 1

    player.zeros_actual = zeros
    player.ones = ones
    print()
    print(zeros)
    return [matrix, zeros, ones]


def get_timeout_seconds(player):
    participant = player.participant
    return participant.expiry - time.time()


def display_timer(player):
    return get_timeout_seconds(player) > 0


def next_sg_session(player: Player, subsession: Subsession):
    subsession.stage += 1
    subsession.round = 1
    subsession.timeout_happened = True


# PAGES
class Info(Page):
    form_model = 'player'
    form_fields = ['table_goal', 'comprehension_input']

    @staticmethod
    def error_message(player: Player, values):
        if values['comprehension_input'] != C.COMP_NUMBER:
            return 'The comprehension number must match the value provided!'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if player.subsession.stage == 1:
            participant.expiry = time.time() + 60 * 10   # TODO change back to 60 * 10
        else:
            participant.expiry = time.time() + 60 * 20

        if timeout_happened:
            next_sg_session(player)

    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        return subsession.round == 1


class Counting(Page):
    form_model = 'player'
    form_fields = ['zeros_guess']

    display_timer = display_timer
    get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def is_displayed(player: Player):
        return get_timeout_seconds(player) > 3

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # TODO change display to participant.payoff and remove logic to look at previous player rounds.
        print(f'zeros_actual: {player.zeros_actual}, zero_g: {player.zeros_guess}')
        if player.subsession.round == 1:
            if player.zeros_guess == player.zeros_actual:
                player.payoff += C.PAYOUT
                player.feedback = f'Correct: {player.zeros_guess} = {player.zeros_actual} '
            else:
                player.feedback = f'Incorrect: {player.zeros_guess} ≠ {player.zeros_actual} '
        else:
            prev_player = player.in_round(player.round_number - 1)
            if player.zeros_guess == player.zeros_actual:
                print(prev_player.payoff)
                player.payoff += prev_player.payoff + C.PAYOUT
                player.feedback = f'Correct: {player.zeros_guess} = {player.zeros_actual} '
                print(player.field_maybe_none('feedback'))
            else:
                player.payoff += prev_player.payoff
                player.feedback = f'Incorrect: {player.zeros_guess} ≠ {player.zeros_actual} '

    @staticmethod
    def js_vars(player):
        m_values = matrix_creation(player)
        print(f'[1]: {m_values[1]}, [2]: {m_values[2]}')
        if player.round_number > 1:
            last_round = player.in_round(player.round_number - 1)
        else:
            last_round = player
        return dict(
            matrix=m_values[0],
            zeros=m_values[1],
            ones=m_values[2],
            feedback=last_round.feedback
        )


class ResultsWaitPage(WaitPage):  # TODO use participants.payoff to display money
    pass


class Results(Page):
    pass


#    @staticmethod
#    def is_displayed(player: Player):
#        return player.subsession.timeout_happened


page_sequence = [Info, Counting]
