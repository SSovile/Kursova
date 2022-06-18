import time
import serial
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

DB_URI = "mysql+pymysql://root:root@localhost/kursova"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = SQLAlchemy(app)
ma = Marshmallow(app)

arduino_serial = serial.Serial("COM2", 9600, timeout=1)
cors = CORS(app)

list_of_commands = []

password = ""


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    result = db.Column(db.String(255), nullable=False)

    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return "result " + self.result


class ResultSchema(ma.Schema):
    class Meta:
        fields = ('id', 'result')


result_schema = ResultSchema()
results_schema = ResultSchema(many=True)


@app.route("/result", methods=["GET"])
def get_me():
    results = Result.query.all()
    result = results_schema.dump(results)
    return jsonify(result)


@app.route("/result", methods=["POST"])
def post_request():
    data = request.get_json()
    global password
    print(data)
    list_of_commands.append(data)
    send_list_of_commands(list_of_commands)
    if data != "#" and data != "*":
        password += data
        print("password " + password)
    if data == "#":
        send_data(password)
        print(password)
        arduino_serial.read()
        password = ""
    print(f"Command: {data}, List: {list_of_commands}")

    return 'Success', 200


def send_data(example):
    data_set = {"result": example}
    json_dump = json.dumps(data_set)
    print(json_dump)
    data = ResultSchema().loads(json_dump)

    new_example = Result(**data)
    print(new_example)
    db.session.add(new_example)
    db.session.commit()


def send_list_of_commands(commands):
    for command in commands:
        send_command(command)
        time.sleep(1.3)
    list_of_commands.clear()


def send_command(command):
    arduino_serial.write(command.encode())


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
