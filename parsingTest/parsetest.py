# html_doc = """<html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>

# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>

# <p class="story">...</p>
# """

# from bs4 import BeautifulSoup
# soup = BeautifulSoup(html_doc, 'html.parser')

# for child in soup.contents[0].contents:
#     print(child.name, '\nNEXT CHILD')

from bs4 import BeautifulSoup
html = open('test.html', 'r').read()
parsed_html = BeautifulSoup(html, features='html.parser')
# print(parsed_html.body.find('div', attrs={'class':'container'}).text)
print(parsed_html.contents[0].contents)
for element in parsed_html.contents[0].contents:
    if element == '\n': continue
    try:
        print(element['class'])
        for class_name in element['class']:
            if class_name.startswith('cat'):
                print('BINGO')
    except KeyError: pass