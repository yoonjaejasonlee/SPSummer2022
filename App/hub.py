from flask import jsonify
import requests
from prettytable import PrettyTable


table = PrettyTable()
table.field_names = ["User Name", "Created Date","Language", "Stars", "Forks","URL"]


user = 'yoonjaejasonlee'
token = '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'

authorization = f'token {token}'
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization" : authorization,
    }
i = 1
while 1:
    langs= "python"
    stars = 3000
    forks = 200

    api_url = f"https://api.github.com/search/repositories?q=language:{langs}+stars:>={stars}+forks:>={forks}&page={i}&per_page={1}"

    #send get request
    response = requests.get(api_url,auth=(user,token))

    #get the json data
    data =  response.json()

    for repository in data:
        #name = repository["name"]
        #created_date = repository["created_at"]
        #language = repository["language"]
        #stars = repository["stargazers_count"]
        #forks = repository["forks"]
        #url = repository["html_url"]
        count = repository["total_count"]
        
        #table.add_row([name, created_date, language, stars,forks,url])
        

    
    #print(table)

   #rl = requests.get("https://api.github.com/rate_limit", auth=(user,token))

    #data2 = rl.json()

    print(count)


    i +=1

        


    