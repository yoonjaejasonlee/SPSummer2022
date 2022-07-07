import pandas as pd
import urllib.request
import requests
import json
from flask import Flask, jsonify
from pandas.tseries.offsets import MonthEnd

user = 'yoonjaejasonlee'
token = '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'

app = Flask(__name__)


@app.route('/<string:language>/<int:stars>/<int:forks>/<int:months>/', methods=['GET'])
def actor_to_crawler(language, stars, forks, months):
    today = pd.datetime.now().date()  # will be removed from pandas in a future ver
    for beg in pd.date_range(end=today, periods=months, freq='MS')[::-1]:
        dt = beg.strftime("%Y-%m-%d") + '..' + (beg + MonthEnd(1)).strftime("%Y-%m-%d")
        url = f'https://api.github.com/search/repositories?q=stars:>{stars}+forks:>{forks}+language:{language}+created:{dt}+&order=desc&per_page=100&'
        print(dt)
        crawling(url)

    return jsonify({"language": language, "forks": forks, "stars": stars, "months": months})


total_list = []


def crawling(url):
    requested = urllib.request.Request(url)
    response = urllib.request.urlopen(requested)
    rescode = response.getcode()
    tot_repos = requests.get(url, auth=(user, token)).json()
    total = tot_repos["total_count"]
    print('Total count of repos:', total)
    global total_list
    final_list = []
    i = 1
    while i <= (total / 100) + 1:

        final_url = url + 'page={}'.format(i)
        res = requests.get(final_url, auth=(user, token))
        repos = res.json()
        if rescode == 200:
            repos.get('items', 'error')
            repos = res.json()
            month_list = ([i['html_url'] for i in repos['items']])
            #final_list = []
            for _ in repos['items']:
                try:
                    for res_data in month_list:
                        if res_data in total_list:
                            continue
                        else:
                            final_list.append(res_data)
                            total_list.append(res_data)

                except KeyError:
                    print("error")
            i = i + 1
            month_list.clear()
    urls = "http://sparrow-ml.fasoo.com:24444/repos"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    requests.post(urls, json=json.dumps(final_list), headers=headers)
    final_list.clear()


if __name__ == "__main__":
    app.run(host="sparrow-ml.fasoo.com",
            port=24999,
            debug=True)
