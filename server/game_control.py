"""Root manager for application.  Controls endpoints for the client"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import recap.recap_manager as RecapManager
import music.music_endpoints as MusicEndpoints


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.register_blueprint(MusicEndpoints.music_page)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    "sanity/connectivity check"
    return jsonify('pong!')


@app.route('/recap', methods=['POST'])
def format_recap():
    "format a recap.  Returns bbcode version of recap, with links added."
    response_object = {'status': 'success'}
    formatted = RecapManager.format_recap(request.json['rawText'])
    response_object["msg"] = formatted
    return jsonify(response_object)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
