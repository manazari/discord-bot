from bot import Command
import random

def repeat_fn(command):
    if command == '': return ''
    return f'''repeating "{command}"!'''
Repeat = Command(
    'Repeat',
    'have a message said back to you',
    'repeat',
    repeat_fn
)

def roll_fn(command):
    try: sides = int(command)
    except ValueError: return f'''This commands need an integer, a '{command}' sided dice doesn't exist'''
    landing_face = random.randint(1,sides+1)
    return f'''Rolling your {sides}-sided die...\nIt landed on **__{landing_face}__**'''
    # dash_emoji = ':dash:'
    # game_die_emoji = ':game_die:'
    # return f'''Rolling your {sides}-sided die {dash_emoji+game_die_emoji*2}\nIt landed on **__{landing_face}__**'''
Roll = Command(
    'Roll Dice',
    'roll a dice of any size',
    'roll',
    roll_fn
)

all = [
    Repeat,
    Roll,
]