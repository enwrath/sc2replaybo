import logging
import sc2reader
from math import floor
from json import dumps
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return """
<form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="submit">
</form>
"""


@app.route('/upload', methods=['POST'])
def upload():
    """Process the uploaded file"""
    uploaded_file = request.files.get('file')

    if not uploaded_file:
        return 'No file uploaded.', 400

    replay = sc2reader.load_replay(uploaded_file, load_map=True)
    player1 = replay.players[0]
    player2 = replay.players[1]

    build1 = []
    build2 = []


    for event in replay.events:
        if event.name == "UnitInitEvent":
            if event.unit_controller == player1:
                build1.append(floor(event.second / 60))
                build1.append(event.second % 60)
                if event.unit.name == "SupplyDepotLowered":
                    build1.append("SupplyDepot")
                else: build1.append(event.unit.name)
            else:
                build2.append(floor(event.second / 60))
                build2.append(event.second % 60)
                if event.unit.name == "SupplyDepotLowered":
                    build2.append("SupplyDepot")
                else: build2.append(event.unit.name)
    text = "<html><body><p>" + dumps(build1) + "</p><hr><p>" + dumps(build2) + "</p></body></html>"
    return text

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_storage_app]
