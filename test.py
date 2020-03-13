from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

creds = {
    'email': 'mattn882@gmail.com',
    'password': 'matthewn882',
}

# driver = webdriver.Chrome(executable_path = 'C:\Windows\chromedriver.exe')
driver = webdriver.Chrome(executable_path = '.\chromedriver.exe')

def get_messages():
    driver.implicitly_wait(15)
    message_container = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div')
    return message_container.find_elements_by_xpath('./div')

class Bot:
    def __init__(self, cue, profile_creds):
        self.cue = cue
        self.profile_creds = profile_creds
        self.commands = []
        self.messages = []
        self.logged_in = False

    def login(self, channel_url):
        driver.get(channel_url)
        driver.implicitly_wait(10)
        enter_email = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div/form/div/div/div[1]/div[3]/div[1]/div/input')
        enter_password = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div/form/div/div/div[1]/div[3]/div[2]/div/input')
        enter_email.send_keys(self.profile_creds['email'])
        enter_password.send_keys(self.profile_creds['password'])
        driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div/form/div/div/div[1]/div[3]/button[2]/div').click()
        self.messages = self.get_new_messages()
        self.logged_in = True

    def get_new_messages(self):
        driver.implicitly_wait(15)
        message_container = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div')
        return message_container.find_elements_by_xpath('./div')
    
    def send_message(self, message):
        if not self.logged_in: return
        print(f'''SENDING '{message}' ''')
        for i, line in enumerate(message.splitlines(), 1):
            box = driver.find_element_by_xpath(f'''/html/body/div/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/div[1]/form/div/div/div/div[3]/div/div[{i}]''')
            if i == 1:
                box.send_keys('> `')
            box.send_keys(f'''{line}''')
            box.send_keys(Keys.SHIFT, Keys.ENTER)
        box.send_keys('`' + Keys.ENTER)
    
    def interpret(self, line):
        if not line.startswith(self.cue+' '):
            return
        line = line.split(self.cue+' ', 1)[1]
        for command in self.commands:
            if line.startswith(command.cue+' '):
                print(f'''Found '{command.name}' command''')
                message = command.interpret(line.split(command.cue+' ', 1)[1])
                if message: self.send_message(message)
            break

    def add_command(self, command):
        self.commands.append(command)


class Command:
    def __init__(self, name, descr, cue, interpret_fn):
        self.name = name
        self.descr = descr
        self.cue = cue
        self.interpret_fn = interpret_fn

    def interpret(self, command):
        if command.startswith('!help'):
            return self.info_message()
        return self.interpret_fn(command)

    def info_message(self):
        return f'''#Command: {self.name}\n#Description: {self.descr}'''

mattbott = Bot(';;bott', creds)
mattbott.login('https://discordapp.com/channels/687191433668591619/687191434318839836')
def repeat_fn(command):
    return f'''repeating "{command}"!'''
repeater = Command(
    'Repeat',
    'have a message said back to you',
    'repeat',
    repeat_fn
)
mattbott.add_command(repeater)

messages = get_messages()
driver.implicitly_wait(0.1)
for message in messages:
    try:
        line = message.find_element_by_xpath('./div[1]/div[1]').get_attribute('innerHTML')
        mattbott.interpret(line)
    except NoSuchElementException:
        continue
driver.implicitly_wait(10)