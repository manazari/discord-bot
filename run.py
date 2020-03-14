from bot import Bot
import commands

if __name__ == '__main__':
    mattbott = Bot('mattbott', ';;mattbott', {
        'email': 'mattn882@gmail.com',
        'password': 'matthewn882',
    })
    mattbott.login('https://discordapp.com/channels/687191433668591619/688169304159551512')
    for command in commands.all: mattbott.add_command(command)
    mattbott.listen()