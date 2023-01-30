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
    ROUNDS_IN_STAGE = 100  # 1000 bc I want the app to be time
    TIMEOUT_HAPPENS = [10, 20, 20]
    NUM_ROUNDS = 3 * ROUNDS_IN_STAGE
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
    correct = models.BooleanField()
    feedback = models.StringField(initial="You\'ll see feedback here")

    # Player input
    comprehension_input = models.IntegerField(blank=False)
    zeros_guess = models.IntegerField(min=0, label="Input the amount of zeros here")

    # Participant info
    correct_s1 = models.IntegerField(initial=0)
    correct_s2 = models.IntegerField(initial=0)
    correct_s3 = models.IntegerField(initial=0)

    # Validation
    zeros_actual = models.IntegerField()
    ones = models.IntegerField()

    # Stage info
    stage = models.IntegerField(initial=1)
    first_round = models.BooleanField()
    table_goal = models.IntegerField(intitial=10, label="Table Goal (Optional)", blank=True)

    # congratulations Page
    congratulated = models.BooleanField(initial=False)
    choices = models.StringField( label="Please choice an option",
        choices=['Continue on same stage', 'Move to next stage']
    )


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
            ss.is_last_period = ses_round == C.ROUNDS_IN_STAGE
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
    return [matrix, zeros, ones]


def get_timeout_seconds(player):
    participant = player.participant
    return participant.expiry - time.time()


def display_timer(player):
    return get_timeout_seconds(player) > 0


def advance_stage(subsession: Subsession):
    subsession.stage += 1
    subsession.round = 1
    subsession.timeout_happened = True


def stage_number(subsesion: Subsession) -> int:
    return subsesion.stage


def correct_in_stage(player: Player) -> int:  # TODO
    if player.round_number <= 1 and \
            player.field_maybe_none('correct') is not None:
        return int(player.correct)

    participant = player.participant
    participant.correct_s1, participant.correct_s2, participant.correct_s3 = 0, 0, 0
    cur_stage = stage_number(player.subsession)
    start, end = 0, 0
    par_correct = None

    if cur_stage == 1:
        par_correct = participant.correct_s1
        start, end = 1, C.ROUNDS_IN_STAGE
    elif cur_stage == 2:
        par_correct = participant.correct_s2
        start, end = C.ROUNDS_IN_STAGE + 1, C.ROUNDS_IN_STAGE * 2
    elif cur_stage == 3:
        par_correct = participant.correct_s3
        start, end = C.ROUNDS_IN_STAGE * 2 + 1, C.ROUNDS_IN_STAGE * 3
    else:
        print("ERROR: default switch case")
        return 1234567890
    """
    match cur_stage:
        case 1:
            par_correct = participant.correct_s1
            start, end = 1, C.ROUNDS_IN_STAGE
        case 2:
            par_correct = participant.correct_s2
            start, end = C.ROUNDS_IN_STAGE + 1, C.ROUNDS_IN_STAGE * 2
        case 3:
            par_correct = participant.correct_s3
            start, end = C.ROUNDS_IN_STAGE * 2 + 1, C.ROUNDS_IN_STAGE * 3
        case _:
            print("ERROR: default switch case")
            return 1234567890
    """

    for s_round in player.in_rounds(start, end):
        if s_round.field_maybe_none('zeros_actual') is None:
            return par_correct
        if s_round.field_maybe_none('correct') is not None and s_round.correct:
            par_correct += int(s_round.correct)

    return par_correct


# Checks to see if there have been three consecutive wrongs
def penalty_check(player) -> int:
    if player.round_number <= 1 and \
            player.field_maybe_none('correct') is not None:
        return int(player.correct)

    cur_stage = stage_number(player.subsession)
    wrong_count = 0
    start, end = 0, 0

    match cur_stage:
        case 1:
            start, end = 1, C.ROUNDS_IN_STAGE
        case 2:
            start, end = C.ROUNDS_IN_STAGE + 1, C.ROUNDS_IN_STAGE * 2
        case 3:
            start, end = C.ROUNDS_IN_STAGE * 2 + 1, C.ROUNDS_IN_STAGE * 3
        case _:
            print("ERROR IN W: default switch case")
            return 987654321

    for s_round in player.in_rounds(start, end):
        if s_round.field_maybe_none('zeros_actual') is None:
            return wrong_count
        if s_round.field_maybe_none('correct') is not None and not s_round.correct:
            wrong_count += 1
        else:
            wrong_count = 0

    return wrong_count


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

        participant.congratulated = False
        participant.table_goal = player.field_maybe_none('table_goal')

        if player.subsession.stage == 1:
            participant.correct_s1 = player.correct_s1
            participant.expiry = time.time() + 30  # TODO change back to 60 * 10
            if participant.table_goal is None:
                participant.table_goal = 10
        elif player.subsession.stage == 2:
            participant.correct_s2 = player.correct_s2
            participant.expiry = time.time() + 60 * 20
            if participant.table_goal is None:
                participant.table_goal = 20;
        else:
            participant.correct_s3 = player.correct_s3
            participant.expiry = time.time() + 60 * 20
            if participant.table_goal is None:
                participant.table_goal = 20;

        if timeout_happened:
            advance_stage(player)

    @staticmethod
    def is_displayed(player: Player):  # TODO use this for congratulations page
        subsession = player.subsession
        return subsession.round == 1


class Counting(Page):
    form_model = 'player'
    form_fields = ['zeros_guess', 'table_goal']

    get_timeout_seconds = get_timeout_seconds
    correct, wrong = 0, 0

    @staticmethod
    def is_displayed(player: Player):
        return get_timeout_seconds(player) > 3

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # TODO change display to participant.payoff and remove logic to look at previous player rounds.
        if player.zeros_guess == player.zeros_actual:
            player.correct = True
            player.payoff += C.PAYOUT
            player.feedback = f'Correct: {player.zeros_guess} = {player.zeros_actual}'
        else:
            player.correct = False
            penalty = penalty_check(player)
            if penalty > 2:
                player.payoff -= C.PAYOUT
                player.feedback = f'<b>Incorrect: {player.zeros_guess} ≠ {player.zeros_actual}<br><br>' \
                                  f'<span>&Ll;</span>&nbsp' \
                                  f'Alert: 0.25 penalty!' \
                                  f'&nbsp<span>&Gg;</span></b>'
            elif penalty > 1:
                player.feedback = f'Incorrect: {player.zeros_guess} ≠ {player.zeros_actual}<br><br>' \
                                  f'<span>&#9888;</span>&nbsp' \
                                  f'<b>Warning: <span>&#9888;</span><br>' \
                                  f'$0.25 penalty with <br>3 consecutive wrong answers!</b>'
            else:
                player.feedback = f'Incorrect: {player.zeros_guess} ≠ {player.zeros_actual} '

    @staticmethod
    def js_vars(player):
        correct_s = correct_in_stage(player)
        m_values = matrix_creation(player)
        if player.round_number > 1:
            last_round = player.in_round(player.round_number - 1)
        else:
            last_round = player
        return dict(
            matrix=m_values[0],
            zeros=m_values[1],
            ones=m_values[2],
            feedback=last_round.feedback,
            correct=correct_s,
        )


class Congratulations(Page):
    form_model = 'player'
    form_fields = ['choices']


    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        player_progress = correct_in_stage(player)
        return not participant.congratulated and (player_progress >= participant.table_goal)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.congratulated = True


class ResultsWaitPage(WaitPage):  # TODO use participants.payoff to display money
    pass


class Results(Page):
    pass


page_sequence = [Info, Counting, Congratulations]