import requests, csv
from bs4 import BeautifulSoup, Comment
from FAQ_ws import GetSoup  

URL = 'http://www.csee.usf.edu/~kchriste/ugFaq.html'  #USF CSE FAQ Page


def GetList(URL):
    """Gets a Python List of all links in a URL and the text associated with that link """
    
    soup = GetSoup(URL)
    Links = []
    for link in soup.findAll('a',href = True):
        if link.string != None and link.get('href') != None:
                temp = []
                a = str(link.string)
                b = a.strip()
                c = b.replace('\n',' ')
                d = c.replace('\r', "")
                temp.append(d)
                e = link.get('href')
                if '#' in e:
                    f = URL + e
                    temp.append(f)
                else:
                    temp.append(e)
                Links.append(temp)
    return Links

def Traverse_FAQ_BTags(URL):

    """ Iterates over B tags on FAQ webpage and writes Answers to CSV File """

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



def tests():
    Links = GetList(URL)
    #[print(x) for x in Links]
    
    f = open('Links_and_text.txt','w')  # Write Links to File
    for items in Links:
        for things in items:
            f.writelines(things+" ")
        f.writelines('\n')
    f.close()

    



if __name__ == '__main__':
    tests()





