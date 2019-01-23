import requests
from bs4 import BeautifulSoup, Comment
import csv

URL = 'http://www.csee.usf.edu/~kchriste/ugFaq.html'  # USF CSE FAQ Page


def Traverse_FAQ_BTags(URL):

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    csv_file = open('FAQ.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Question', 'Answer', 'link'])

    for item in soup.find_all('b'):

        Question = item.string.strip()

        temp = item.find_next("li")
        temp2 = temp.find_next(string=True)
        temp3 = temp2.find_next('a', href=True)
        myLink = temp3.get('href').strip()
        temp5 = temp3.find_next(string=True)

        Answer1 = str(temp2).strip() + " " + str(temp5).strip()
        Answer2 = Answer1.replace('\n', " ")
        Answer = Answer2.replace('\r', "")

       # print(Answer)

        if '#' in myLink:
            Link = URL + myLink
        else:
            Link = myLink
       # print(Link)

        csv_writer.writerow([Question, Answer, Link])

    csv_file.close()


Traverse_FAQ_BTags(URL)
