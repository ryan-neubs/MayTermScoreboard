# app.py

from flask import Flask, render_template, request, redirect, flash
import json
from pprint import pprint as pretty
from dotenv import load_dotenv
import os
from time import sleep

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/', methods=['GET', 'POST'])
def home():

    data = get_points()
    freshmen = data["Points"]["Freshmen"]
    sophomore = data["Points"]["Sophomore"]
    junior = data["Points"]["Junior"]
    senior = data["Points"]["Senior"]

    return render_template('points.html',
                           freshmen=freshmen, 
                           sophomore=sophomore,
                           junior=junior,
                           senior=senior)

@app.route('/pointedit', methods=['GET', 'POST'])
def pointedit():
    if request.method == 'POST':
        form = request.form
        if verifypw(form["passkey"]):
            update_points(form["class"], form["points"])
    return render_template('editor.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
         form = request.form
         if verifypw(form["passkey"]):
             reset_points()
    return redirect('/')

def reset_points():
    data = get_points()
    for p in data["Points"]:
        data["Points"][p] = 0
    with open('points.json', 'w') as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True)

def update_points(year, amount):
    amount = int(amount)
    data = get_points()
    data["Points"][year] += amount
    with open('points.json', 'w') as data_file:
        json.dump(data, data_file, indent=4, sort_keys=True)

def get_points():
    with open('points.json') as data_file:
        data = json.load(data_file)
    return data


# For whoever read this: The passkey will be stored in a .env file. It is in the gitignore template so
# it isn't out on the repository for anyone to see. You can make the passkey whatever you want in the .env
def verifypw(input):
    return input == os.getenv('PASSKEY')

app.run(host='localhost', port=5000)