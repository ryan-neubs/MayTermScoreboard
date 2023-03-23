# app.py

from flask import Flask, render_template
import json
from pprint import pprint as pretty
from dotenv import load_dotenv
import os

app = Flask(__name__)
@app.route('/points')
def hello():
    data = get_points()
    return render_template('points.html', points=data)

def get_points():
    with open('points.json') as data_file:
        data = json.load(data_file)
    return data

def update_points(year, amount):
    data = get_points()
    data["Points"][year] += amount
    with open('points.json', 'w') as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True)

def reset_points():
    data = get_points()
    for p in data["Points"]:
        data["Points"][p] = 0
    with open('points.json', 'w') as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True)

def verifypw(input):
    return input == os.getenv('PASSKEY')

app.run(host='localhost', port=5000)