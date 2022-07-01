from asyncio.windows_events import NULL
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/{fork}/{star}/{lang}/', methods=['POST'])
def req(fork, star, lang):
    a = request.form.get('language')
    b = request.form.get('fork')
    c = request.form.get('star')

    return jsonify({"language": a, "fork": b, "star": c})


if __name__ == "__main__":
    app.run()
