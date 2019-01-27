import requests, csv
from bs4 import BeautifulSoup, Comment


def FAQ_scrap():
    URL = 'http://www.csee.usf.edu/~kchriste/ugFaq.html'

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    data = {}

    for i in range(3,6,1):
        for items in soup.find_all('h3')[i]:
            title = items.string.strip()
            for tags in items.find_all_next('b'):
                Question = tags

                #print("Question: ----------------------")
                #print(Question.string.strip())

                li_tag = Question.find_next('li')
                links = li_tag.select('a')
                strings = li_tag.find_all(string=True)

                
                Answer = " ".join(strings).replace('\n'," ").replace('\r',"").replace("  ", " ")
                #print("SINGLE ANSWER: -----------")
                #print(Answer)

                data[Question.string.strip().replace('\n'," ").replace('\r',"")] = Answer

                #print(data[Question.string.strip()])
                
                Answer_List = []
                for i in range(0,len(strings)-2,2):
                    if len(strings) == 1:
                        Answer_List.append((strings[i], "No Links"))
                        break
                    else:
                        answer = strings[i] + strings[i+1]
                        Answer_List.append((answer.replace('\n'," ").replace('\r',""),links[int(i/2)].get('href')))
                    
                #print("ANSWER LIST: --------------------------------")
                #[print(x) for x in Answer_List]
                #print('\n')

    return data


#data = FAQ_scrap()

#print(data)

  