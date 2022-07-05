
from flask import Flask
from flask import request
import json
import analyze

app = Flask(__name__)


def on_json_loading_failed_return_dict(e):
    return {}


@app.route("/repos", methods=['GET', 'POST'])
def test():
    content = request.json
    contents = json.loads(content)
    analyze.queuing(contents)
    return ""


if __name__ == "__main__":
    app.run(debug=True)
