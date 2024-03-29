import flask
import os
import ftplib
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')

from flask import request
from flask import jsonify
from datetime import datetime

import multiprocessing as mp


app = flask.Flask(__name__)


def worker(voltage):
    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    filename = "data.txt"
    # if last modification date of the file was one year before, empty file
    if os.stat(filename).st_size > 1048576:
        open(filename, 'w').close()

    num = float(voltage)
    if num < 11.6:
        charge = "0%"
    elif num < 12.0:
        charge = "30%"
    elif num < 12.2:
        charge = "50%"
    elif num < 12.5:
        charge = "75%"
    else:
        charge = "100%"

    with open(filename, "a") as myfile:
        myfile.write("{}, {}\n".format(date, voltage))

    # Data for plotting
    t = []
    s = []
    with open(filename) as fp:
        for cnt, line in enumerate(fp):
            data = line.split(",")
            t.append(cnt)
            s.append(float(data[1].strip()))

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel="{} - {} - {}V".format(date, charge, voltage), ylabel='voltage (V)')
    ax.grid()

    fig.savefig("battery.png")

    # upload to FTP
    session = ftplib.FTP(os.environ['URL'], os.environ['USERNAME'], os.environ['PASSWORD'])
    file = open('battery.png', 'rb')
    session.storbinary('STOR battery.png', file)
    file.close()
    session.quit()


@app.route('/', methods=['GET'])
def home():
    return "<h1>Observatory Ca l'ou API</h1><p>API per controlar el observatori de Ca l'Ou.</p>"


@app.route('/api/v1/battery/add', methods=['GET'])
def api_id():
    result = {'result': ''}
    if 'v' in request.args:
        result['result'] = 'ok'
        voltage = float(request.args['v'])

        proc = mp.Process(target=worker, args=(voltage,))
        proc.daemon = True
        proc.start()
        proc.join()

    else:
        result['result'] = 'ko'

    return jsonify(result)


app.run(host='0.0.0.0')
