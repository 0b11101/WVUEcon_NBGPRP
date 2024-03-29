import os
from os import environ

SESSION_CONFIGS = [
    dict(
        name='Tedious_Observation',
        display_name='Counting Game',
        app_sequence=['tedious_observation'],
        num_demo_participants=1,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.25, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['expiry',
                      'table_goal',
                      'correct_s1',
                      'correct_s2',
                      'correct_s3',
                      'congratulated'
                      ]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

AUTH_LEVEL = os.environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6448173622590'
