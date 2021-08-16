import json
import base64

from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify


DIAGNOSTICS = Blueprint('DIAGNOSTICS', __name__)


def read_diagnostics_file():
    diagnostics = {}
    try:
        with open('diagnostic_data.json', 'r') as f:
            diagnostics = json.load(f)
    except FileNotFoundError:
        msg = 'Diagnostics have not yet run, please try again in a few minutes'
        diagnostics = {'error': msg}
    return diagnostics


@DIAGNOSTICS.route('/')
def get_diagnostics():
    diagnostics = read_diagnostics_file()

    if request.args.get('json'):
        return jsonify(diagnostics)

    return render_template('diagnostics_page.html', diagnostics=diagnostics)


@DIAGNOSTICS.route('/initFile.txt')
def get_initialisation_file():
    diagnostics = read_diagnostics_file()

    if diagnostics.get('error'):
        return 'Internal Server Error', 500

    response = {
        "VA": diagnostics['VA'],
        "FR": diagnostics['FR'],
        "E0": diagnostics['E0'],
        "RPI": diagnostics['RPI'],
        "OK": diagnostics['OK'],
        "PK": diagnostics['PK'],
        "PF": diagnostics["PF"],
        "ID": diagnostics["ID"]
    }

    response_b64 = base64.b64encode(str(json.dumps(response)).encode('ascii'))
    return response_b64