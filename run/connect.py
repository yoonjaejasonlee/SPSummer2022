from flask import Flask, jsonify
from flask import request
import requests
from multiprocessing import Process, Value

app = Flask(__name__)
user = 'yoonjaejasonlee'
token = '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'

lists = []


@app.route("/repos/<string:s>", methods=['GET'])
def test(s):
    lists.clear()
    api_url = f"https://api.github.com/search/repositories?q=language:python+stars:%3E=200+forks:%3E=100&page={s}&per_page=100"
    response = requests.get(api_url, auth=(user, token))
    response_data = response.json()
    for s in response_data["items"]:
        url = s["html_url"]
        lists.append(url)

    return jsonify(lists)


if __name__ == "__main__":
    app.run(host="sparrow-ml.fasoo.com",
            port=24443,
            debug=True)



