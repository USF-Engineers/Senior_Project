""" for text in soup.body.find_all(string=True):
    if text.parent.name not in ['script', 'meta', 'link', 'style'] and not isinstance(text, Comment) and text != '\n':
        FAQ_text += text.strip()
 """
"""


 html_doc = 
<a href="http://www.usf.edu/engineering/cse">Computer Science and
Engineering</a>


soup = BeautifulSoup(html_doc, 'html.parser')
a = str(soup.get_text())
b = a.strip()
c = b.replace('\n',' ')


"""