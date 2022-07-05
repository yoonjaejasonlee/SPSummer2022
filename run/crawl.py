from typing import final
import pandas as pd
import urllib.request
import mariadb
import requests
import json
import sys
from pandas import *
from flask import Flask, jsonify, request, session, make_response, url_for, redirect
from pandas.tseries.offsets import MonthEnd

user = 'yewonhong'
token = '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'  # 3months exp

conn = None
cursor = None

try:
    conn = mariadb.connect(
        user='root',
        password='a1234567!',
        host='sparrow-ml.fasoo.com',  # '127.0.0.1',
        port=30198,
        db='Crawler'  # 'pythondb',
    )
    cursor = conn.cursor()

except mariadb.Error as e:

    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)

app = Flask(__name__)


@app.route('/<string:language>/<int:stars>/<int:forks>/<int:months>/', methods=['GET'])
def actor_to_crawler(language, stars, forks, months):
    if request.method == 'GET':

        if request.form.get('language') == 'language':
            session["language"]
        if request.form.get('stars') == 'stars':
            session["stars"]
        if request.form.get('forks') == 'forks':
            session["forks"]
        if request.form.get('months') == 'months':
            session["months"]

    today = pd.datetime.now().date()  # will be removed from pandas in a future ver
    for beg in pd.date_range(end=today, periods=months, freq='MS')[::-1]:
        dt = beg.strftime("%Y-%m-%d") + '..' + (beg + MonthEnd(1)).strftime("%Y-%m-%d")
        url = f'https://api.github.com/search/repositories?q=stars:>{stars}+forks:>{forks}+language:{language}+created:{dt}+&order=desc&per_page=100&'
        print(dt)
        crawling(url)

    return jsonify({"language": language, "forks": forks, "stars": stars, "months": months})


global total_list

total_list = []


def crawling(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    tot_repos = requests.get(url, auth=(user, token)).json()
    total = tot_repos["total_count"]
    print('Total count of repos:', total)
    global total_list

    i = 1
    while i <= (total / 100) + 1:

        final_url = url + 'page={}'.format(i)
        res = requests.get(final_url, auth=(user, token))
        repos = res.json()
        month_list = []
        if rescode == 200:
            repos.get('items', 'error')
            repos = res.json()
            month_list = ([i['html_url'] for i in repos['items']])
            final_list = []
            for j in repos['items']:
                try:
                    res_data = j['html_url']
                    cursor.execute(f"INSERT IGNORE INTO repos VALUES(\"{res_data}\")")
                    conn.commit()

                    for res_data in month_list:
                        if res_data in total_list:
                            continue
                        else:
                            print(res_data)
                            final_list.append(res_data)
                            total_list.append(res_data)

                except KeyError:
                    print("error")
            i = i + 1
            month_list.clear()
            url = "http://127.0.0.1:5000/repos"
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, json=json.dumps(final_list), headers=headers)


if __name__ == "__main__":
    app.run(host="127.0.0.1",
            port=4999,
            debug=True)
