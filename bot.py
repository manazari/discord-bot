from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome(executable_path = '.\chromedriver.exe')
    
def children_by_class_keyword(soup, class_keyword_path):
    if class_keyword_path == '': return []
    class_keywords = [{
        'keyword': class_keyword.split('[', 1)[0],
        'index': int(class_keyword.split('[', 1)[1][0:-1]),
    } for class_keyword in class_keyword_path.split('/')[0:-1]]
    class_keywords.append({
        'keyword': class_keyword_path.split('/')[-1:][0],
        'index': '*',
    })
    def inner_loop(soup):
        next_class, next_class_index = class_keywords[0]['keyword'], class_keywords[0]['index']
        children = []
        for element in soup.contents:
            if element == '\n': continue
            try:
                for class_name in element['class']:
                    if class_name.startswith(next_class): children.append(element)
            except KeyError: pass
        if next_class_index == '*': return children
        del class_keywords[0]
        return inner_loop(children[next_class_index])
    return inner_loop(soup)

class Bot:
    def __init__(self, name, cue, profile_creds):
        self.name = name
        self.cue = cue
        self.profile_creds = profile_creds
        self.commands = []
        self.messages = []
        self.logged_in = False

        def about_fn(command):
            about_message = f'''*__<< Help with {self.name.upper()} >>__*\n\n'''
            about_message += '\n\n'.join([command.info_message() for command in self.commands])
            self.send_message(about_message)
        
        self.add_command(Command(
            'About',
            'learn about what I can do for you!',
            'about',
            about_fn
        ))

    def login(self, channel_url):
        print(f'''Attempting to log into '{channel_url}' with credentials '{self.profile_creds}'...''')
        driver.get(channel_url)
        driver.implicitly_wait(10)
        enter_email = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div/form/div/div/div[1]/div[3]/div[1]/div/input')
        enter_password = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div/form/div/div/div[1]/div[3]/div[2]/div/input')
        enter_email.send_keys(self.profile_creds['email'])
        enter_password.send_keys(self.profile_creds['password'])
        driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div/form/div/div/div[1]/div[3]/button[2]/div').click()
        self.logged_in = True
        print('''LOGGED IN!''')
        self.get_new_messages()

    def get_new_messages(self):
        if not self.logged_in: return []
        driver.implicitly_wait(15)
        message_container = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div')
        parsed_html = BeautifulSoup(message_container.get_attribute('innerHTML'), features='html.parser')
        current_messages = children_by_class_keyword(parsed_html, 'message')
        new_messages = []
        def message_content(message_soup):
            return children_by_class_keyword(message_soup, 'contents[0]/messageContent')[0].text
        if not (len(current_messages) == 50 and len(self.messages) == 50):
            new_messages = current_messages[min(len(current_messages), len(self.messages)):]
        else:
            for i, message in enumerate(self.messages):
                if message_content(message) == message_content(current_messages[0]) and i != 0:
                    number_of_new_messages = i
                    new_messages = current_messages[-number_of_new_messages:]
                    break
        self.messages = current_messages
        return [message_content(message) for message in new_messages]
    
    def send_message(self, message):
        if not self.logged_in: return
        for i, line in enumerate(message.splitlines(), 1):
            box = driver.find_element_by_xpath(f'''/html/body/div/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/div[1]/form/div/div/div/div[3]/div/div[{i}]''')
            if i == 1:
                box.send_keys('> ')
            box.send_keys(f'''{line}''')
            box.send_keys(Keys.SHIFT, Keys.ENTER)
        box.send_keys(Keys.ENTER)
    
    def interpret(self, line):
        if not line.startswith(self.cue+' '):
            return
        line = line.split(self.cue+' ', 1)[1]
        for command in self.commands:
            if line.startswith(command.cue):
                print(f'''Summon is summoning the '{command.name}' command...''')
                command_line = line.split(command.cue, 1)[1].lstrip()
                message = command.interpret(command_line)
                if message: self.send_message(message)
                break
        else:
            self.send_message(f'''**Umm...** '__{line.split(' ')[0]}__' is not a command.\nTry '__about__' for help on what I can do!''')

    def listen(self):
        if not self.logged_in: return
        driver.implicitly_wait(0.1)
        while True:
            messages = self.get_new_messages()
            for message in messages:
                print('>', message)
                self.interpret(message)
            time.sleep(1)

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
        return f'''**__HELP FOR '{self.name.upper()}'__**
**# Cue**: `{self.cue}`
**# Desc**: `{self.descr}`'''