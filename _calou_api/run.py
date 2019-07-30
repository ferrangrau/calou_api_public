import flask
import os
import ftplib

import matplotlib.pyplot as plt

from flask import request
from flask import jsonify
from datetime import datetime


app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Observatory Ca l'ou API</h1><p>API per controlar el observatori de Ca l'Ou.</p>"


@app.route('/api/v1/battery/add', methods=['GET'])
def api_id():
    result = {'result': ''}
    if 'v' in request.args:
        result['result'] = 'ok'
        voltage = float(request.args['v'])

        date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        filename = "data_{}.txt".format(datetime.now().strftime("%m"))
        # if last modification date of the file was one year before, empty file
        if os.path.isfile(filename):
            stat = os.stat(filename)

            if datetime.fromtimestamp(stat.st_mtime).strftime("%m") < datetime.now().strftime("%m"):
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

        # Add to leaky code within python_script_being_profiled.py
        from pympler import muppy, summary
        all_objects = muppy.get_objects()
        sum1 = summary.summarize(all_objects)  # Prints out a summary of the large objects
        summary.print_(sum1)  # Get references to certain types of objects such as dataframe

        import sys
        # print(globals())

        loca = locals()
        for var in loca:
            mida = sys.getsizeof(loca[var])/1024/1024
            if mida > 0.5:
                print(var, type(loca[var]), " - ", " - ", mida, "Mb")

    else:
        result['result'] = 'ko'

    return jsonify(result)


app.run(host='0.0.0.0')
