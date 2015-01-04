from flask import Flask, jsonify, request
from anabot import Anabot
import json
import loop_wt_wt


# configuraiton
DEBUG = True

anabot = Anabot()
app = Flask(__name__)
#SERVER_NAME = '127.0.0.1:9010'
app.config.from_object(__name__)

@app.route('/')
def index():
    return app.send_static_file('html/index.html')


@app.route("/anabot/run_wt_wt", methods=['POST'])
def run_wt_wt():
    global anabot
    try:
        loop_wt_wt.wt_wt_prep_plan(anabot, 10)
    except Exception as e:
        response = jsonify({
            'status': 400,
            'message': e.message
        })
        return response
    return jsonify(anabot.to_dict())

@app.route("/anabot")
def read():
    """
    display the state of the anabot
    """
    global anabot
    return jsonify(anabot.to_dict())

@app.route("/anabot/task", methods=['POST'])
def task():
    """
    execute an anabot task
    """
    global anabot
    data = request.data
    task = json.loads(data)
    method = getattr(anabot, task['name'])
    inputs = task['inputs'] if task['inputs'] else dict()
    try:
        task['outputs'] = method(**inputs)
    except Exception as e:
        response = jsonify({
            'status': 400,
            'message': e.message
        })
        response.status_code = 400
        return response
    return jsonify(anabot.to_dict())

@app.route("/anabot/reset", methods=['POST'])
def reset():
    global anabot
    anabot = Anabot()
    return jsonify(anabot.to_dict())

if __name__ == "__main__":
    app.run(port=9027)
