import pandas as pd
import urllib.request
import mariadb
import requests
import time
import sys
from pandas import *
from flask import Flask, jsonify, request
from pandas.tseries.offsets import MonthEnd


user = 'yewonhong'
token = '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'  # 3months exp

conn = None
cursor = None

try:
    conn = mariadb.connect(
        user='root',
        password='a1234567!',
        host='sparrow-ml.fasoo.com',
        port=30198,
        db='Crawler',
    )
    cursor = conn.cursor()

except mariadb.Error as e:

    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)

app = Flask(__name__)
lists = []


# with app.app_context():
#     cursor = mariadb.connection.cursor()

@app.route('/request', methods=['POST'])
def actor_to_crawler():
    a = request.form.get('language')
    b = request.form.get('forks')
    c = request.form.get('stars')

    return jsonify({"language": a, "forks": b, "stars": c})


@app.route("/repos/<string:s>", methods=['GET'])
def crawler_to_analyzer(s):
    lists.clear()
    url = get_url(lang)
    final_url = url + 'page={s}'
    res = requests.get(final_url, auth=(user, token))
    repos = res.json()

    for s in repos["items"]:
        url = s["html_url"]
        lists.append(url)

    print(lists)
    return jsonify(lists)


def request_crawl(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    # ________________________delete later__________________________
    tot_repos = requests.get(url, auth=(user, token)).json()
    total = tot_repos["total_count"]
    print('Total count of repos:', total)
    start = time.time()
    # global final_url
    # ________________________delete later__________________________

    i = 1
    while i <= 10:

        final_url = url + 'page={}'.format(i)
        res = requests.get(final_url, auth=(user, token))
        repos = res.json()

        if (rescode == 200):
            repos.get('items', 'error')
            for j in repos['items']:
                try:
                    res_data = j['html_url']
                    lists.append(res_data)
                    cursor.execute(f"INSERT IGNORE INTO repos VALUES(\"{res_data}\")")
                    conn.commit()
                    # Request API (Crawler <-> Analyzer)
                    i += 1

                except KeyError:
                    print("error")
                    i
            print(lists)

            # ________________________delete later__________________________
            end = time.time()
            print('response time: ', end - start, '\n')
            # ________________________delete later__________________________

        else:
            print("Error code: " + rescode)


def get_url(lang):
    def set_stars(stars_d=50):

        stars = int(input("Set the minimum number of stars (default & minimum is 50): "))

        if stars >= 50:
            print('The {} is set as stars.'.format(stars))
            return stars
        else:
            print('The default value 50 is set.')
            return stars_d

    def set_forks(forks_d=5):

        forks = int(input("Set the minimum number of forks (default & minimum is 5): "))

        if forks >= 5:
            print('The {} is set as forks.'.format(forks))
            return forks
        else:
            print('The default value 5 is set.')
            return forks_d

    stars = set_stars()
    forks = set_forks()

    if (lang == "py"):

        today = pd.datetime.now().date()  # will be removed from pandas in a future ver
        for beg in pd.date_range(end=today, periods=100, freq='MS')[::-1]:
            dt = beg.strftime("%Y-%m-%d") + '..' + (beg + MonthEnd(1)).strftime("%Y-%m-%d")
            url = f'https://api.github.com/search/repositories?q=stars:>{stars}+forks:>{forks}+language:python+created:{dt}+&order=desc&per_page=100&'
            print(dt)  # delete later
            request_crawl(url)


    elif (lang == "js"):

        today = pd.datetime.now().date()  # will be removed from pandas in a future ver
        for beg in pd.date_range(end=today, periods=100, freq='MS')[::-1]:
            dt = beg.strftime("%Y-%m-%d") + '..' + (beg + MonthEnd(1)).strftime("%Y-%m-%d")
            url = 'https://api.github.com/search/repositories?q=stars:>{}+forks:>{}+language:javascript+created:{}+&order=desc&per_page=100&'.format(
                stars, forks, dt)
            print(dt)  # delete later
            request_crawl(url)


lang = input("Choose the programming language (python/nodejs): ")
# lang = request.get(f"https://api.github.com/search/repositories/{}/{}/languages").json().keys()
if lang == "py":
    print(get_url(lang))

elif lang == "js":
    print(get_url(lang))

else:
    print("Retype the programming language.")

actor_to_crawler()