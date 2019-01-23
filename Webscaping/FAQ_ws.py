import requests, csv
from bs4 import BeautifulSoup, Comment

URL = 'http://www.csee.usf.edu/~kchriste/ugFaq.html'  #USF CSE FAQ Page


#-------------------------------------------

def GetSoup(URL):
    r = requests.get(URL)
    return BeautifulSoup(r.content, 'html.parser')

#-------------------------------------------

def URL2txt(URL, recursive = False):
    if recursive:
        pass
    
    soup = GetSoup(URL)
    return soup.get_text()

#-------------------------------------------

def GetLinks(URL, recursive = False):
    if recursive:
        pass
    
    links = ''
    soup = GetSoup(URL)
    for link in soup.find_all('a', href = True):
        links += str(link.get('href'))+'\n'
    return links

#-------------------------------------------

def Write2File(filename,data):
    f = open(filename,'w')
    f.write(data)
    f.close()

#-------------------------------------------


def GetList(URL):
    """Gets a Python List of all links in a URL and the text associated with that link """
    
    soup = GetSoup(URL)
    Links = []
    for link in soup.findAll('a',href = True):
        if link.string != None and link.get('href') != None:
                a = str(link.string)
                b = a.strip()
                c = b.replace('\n',' ')
                d = c.replace('\r', "")
                #temp.append(d)
                text = d
                e = link.get('href')
                if '#' in e:
                    Link = URL + e
                    #temp.append(f)

                else:
                    #temp.append(e)
                    Link = e
                Links.append((text,Link))
    return Links

#-----------------------------------------------------------------------------------

def Traverse_FAQ_BTags(URL):

    """ Iterates over B tags on FAQ webpage and writes Answers to CSV File """

    data = []

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
        data.append((Question,Answer,Link))

    csv_file.close()
    return data

#-----------------------------------------------------------------------------------


if __name__ == '__main__':
    FAQ_text = URL2txt(URL)
    Write2File('FAQ.txt', FAQ_text)

    links = GetLinks(URL)
    Write2File('links.txt', links)

    mylist = Traverse_FAQ_BTags(URL)

    Links = GetList(URL)
    [print(x[1]) for x in Links]

    for items in Links:
        URL = items[1]
        #print(URL)
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.getText)





