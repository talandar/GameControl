from flask import Flask, jsonify, request
from flask_cors import CORS
import RecapManager


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!2')


@app.route('/recap', methods=['GET', 'POST'])
def format_recap():
    response_object = {'status': 'success'}
    if request.method == 'GET':
        response_object["msg"] = 'ModifiedRecap'
    else:
        formatted = RecapManager.format(request.json['rawText'])
        response_object["msg"] = formatted
    return jsonify(response_object)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
