import flask
import logging
import csv
from flask import request, json, jsonify
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

from waimea.config import API_HOST, API_PORT

app = flask.Flask('waimea-bigwave-detector')

def gen_filename(base_name, suffix, extension):
    return '{}_{}.{}'.format(base_name,datetime.utcnow().strftime(suffix),extension)

@app.route('/log', methods=['POST'])
def log():
    # TODO:
    #   1) Receive log messages using flask.request.data
    #   2) Buffer log messages to generate one log file per minute
    #   3) Write logs to /waimea/logs/
    
    log_message = request.data
    data = json.loads(log_message)
    now = datetime.now().strftime("%H:%M:%S")

    app.logger.info("%s, %s", now, data)

    base_name="./logs/wave_heights"
    suffix="%H-%M"
    extension="csv"

    file_name=gen_filename(base_name=base_name, suffix=suffix, extension=extension)
    handler = TimedRotatingFileHandler(file_name, when="M", interval=1)

    if (app.logger.hasHandlers()):
        app.logger.handlers.clear()

    app.logger.addHandler(handler)

    return jsonify(data)

@app.route('/alert', methods=['POST'])
def alert():
    # TODO:
    #   1) Receive alert messages
    #   2) Write alerts to /waimea/alerts/

    alert_message = request.data
    alert_data = json.loads(alert_message)

    # TODO: define separate loggers/subloggers to avoid mixing messages
    # Alternative is to write alerts to one csv file instead of using logger to avoid mixing log messages
    # with open('./alerts/alerts_file.csv', mode="w") as alerts_file:
    #     alert_writer = csv.writer(alerts_file, delimiter=",", quotechar='"')
    #     alert_writer.writerow(["alert", "avg wave height is", alert_data])

    app.logger.info("alert, average wave height is %s", alert_data)

    base_name="./alerts/alert"
    suffix="%H-%M-%S"
    extension="csv"

    file_name=gen_filename(base_name=base_name, suffix=suffix, extension=extension)
    alert_handler = logging.FileHandler(file_name)
    
    app.logger.addHandler(alert_handler)

    return jsonify(alert_data)

def main():
    app.run(host=API_HOST, port=API_PORT, debug=True)
