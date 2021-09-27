from flask import Flask, request, jsonify, render_template
from postgres_interface import postgres_execute
from report_interface import get_report
from kubernetes import client, config
from jinja2 import Template
from openshift.dynamic import DynamicClient
import dateutil.parser
import json
import werkzeug
from werkzeug import exceptions
import psycopg2
from psycopg2 import errors
import openshift
import pandas as pd
app = Flask(__name__)
# TEMPLATE_CONTENT = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Title</title>
# </head>
# <body>
#
# {% for table in tables %}
#             {{titles[loop.index]}}
#             {{ table|safe }}
# {% endfor %}
# </body>
# </html>
# """


@app.route('/report')
def report():
    resp = get_report(request.args)  # TODO status code
    print(resp)
    sql = "select * from generate_report_api('{}', '{}') where namespace='{}'".format(resp['spec']['reportPeriod'].lower(),
                                                              resp['spec']['reportingEnd'],
                                                              resp['spec']['namespace'])
    table = postgres_execute(sql, result=True, header=True)
    return jsonify(table)
    # df = pd.DataFrame(table[1:])
    # df.columns = table[0]
    # html_template = Template(TEMPLATE_CONTENT)
    # return html_template.render(**{"tables": [df.to_html(classes='data')], "titles": df.columns.values})



@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'bad request! ' + str(e), 400


@app.errorhandler(werkzeug.exceptions.BadRequestKeyError)
def handle_bad_request(e):
    return 'bad request! ' + str(e), 400


@app.errorhandler(psycopg2.errors.RaiseException)
def handle_bad_request(e):
    return 'bad request ' + str(e), 400

@app.errorhandler(openshift.dynamic.exceptions.NotFoundError)
def handle_bad_request(e):
    return 'bad request ' + str(e), 404


if __name__ == '__main__':
    app.run()
