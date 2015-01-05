from flask import Flask, jsonify, request
from robot import Robot
import json
import loop_wt_wt


# configuraiton
DEBUG = True

robot = Robot()
app = Flask(__name__)
#SERVER_NAME = '127.0.0.1:9010'
app.config.from_object(__name__)

@app.route('/')
def index():
    return app.send_static_file('html/index.html')


@app.route("/robot/run_wt_wt", methods=['POST'])
def run_wt_wt():
    global robot
    try:
        loop_wt_wt.wt_wt_prep_plan(robot, 10)
    except Exception as e:
        response = jsonify({
            'status': 400,
            'message': e.message
        })
        return response
    return jsonify(robot.to_dict())

@app.route("/robot")
def read():
    """
    display the state of the robot
    """
    global robot
    return jsonify(robot.to_dict())

@app.route("/robot/task", methods=['POST'])
def task():
    """
    execute an robot task
    """
    global robot
    data = request.data
    task = json.loads(data)
    method = getattr(robot, task['name'])
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
    return jsonify(robot.to_dict())

@app.route("/robot/reset", methods=['POST'])
def reset():
    global robot
    robot = Robot()
    return jsonify(robot.to_dict())

if __name__ == "__main__":
    app.run(port=9027)
