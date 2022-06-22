from flask import Flask, jsonify
import requests

app = Flask(__name__)
user = 'yoonjaejasonlee'
token = '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'


@app.route('/repos')
def hi():
    lists = []
    for i in range(3):
        api_url = f"https://api.github.com/search/repositories?q=language:python+stars:%3E=150+forks:%3E=20&page={i}&per_page=5"
        response = requests.get(api_url, auth=(user,token))
        response_data = response.json()

        for s in response_data["items"]:
            url = s["url"]
            lists.append(url)
    return jsonify(lists)


if __name__ == "__main__":
    app.run()
