import json
from new_scraper import FAQ_scrap

data = FAQ_scrap()
#print(data)

for key in data:
    print(key)
    print(data[key])


with open('Training_Data.json','w') as outfile:
    json.dump(data,outfile,indent=2)