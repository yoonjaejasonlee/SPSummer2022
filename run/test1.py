import pandas as pd
import requests
from flask import Flask, jsonify, request, session, render_template
from pandas.tseries.offsets import MonthEnd

user = 'yewonhong'
token = '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'  # 3months exp

app = Flask(__name__)
lists = []
fin_list = []


@app.route("/<string:language>/<int:stars>/<int:forks>/<int:months>/", methods=['GET'])
def actor_to_crawler(language, stars, forks, months):
    today = pd.datetime.now().date()  # will be removed from pandas in a future ver
    for beg in pd.date_range(end=today, periods=months, freq='MS')[::-1]:
        dt = beg.strftime("%Y-%m-%d") + '..' + (beg + MonthEnd(1)).strftime("%Y-%m-%d")
        url = f"https://api.github.com/search/repositories?q=stars:>{stars}+forks:>{forks}+language:{language}+created:{dt}+&order=desc&per_page=100&"
        crawl(url)

    return jsonify({"language": language, "forks": forks, "stars": stars, "months": months})


def crawl(url):
    lists.clear()
    response = requests.get(url, auth=(user, token))
    response_data = response.json()
    for s in response_data["items"]:
        html_url = s["html_url"]
        if html_url in fin_list:
            continue
        else:
            fin_list.append(html_url)
            lists.append(html_url)


@app.route("/repos", methods=['GET'])
def crawler_to_analyzer():
    return jsonify(lists)


if __name__ == "__main__":
    app.run(debug=True)
