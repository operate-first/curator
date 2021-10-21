from flask import Flask, request, jsonify, render_template, send_file, after_this_request
from postgres_interface import postgres_execute, postgres_connection
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
import os
import tarfile
import shutil
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
    # print(resp, file=sys.stdout)
    if 'reportingStart' in resp['spec'].keys():
        sql = "SELECT * FROM logs_2 WHERE interval_start >= '{}'::timestamp with time zone AND interval_end < '{}'::timestamp with time zone "\
            .format(resp['spec']['reportingStart'],resp['spec']['reportingEnd'])
    else:
        offset = 0
        if resp['spec']['reportPeriod'].lower() == 'day':
            offset = 1
        elif resp['spec']['reportPeriod'].lower() == 'week':
            offset = 7
        elif resp['spec']['reportPeriod'].lower() == 'month':
            offset = 30
        sql = "SELECT * FROM logs_2 WHERE interval_start >= '{0}'::timestamp with time zone - interval '{1} day' AND interval_end < '{0}'::timestamp with time zone".\
            format(resp['spec']['reportingEnd'], offset)
    if 'namespace' in resp['spec'].keys():
        sql += " AND namespace='{}'".format(resp['spec']['namespace'])
    # print(sql, file=sys.stdout)
    table = postgres_execute(sql, result=True, header=True)
    return jsonify(table)
    # df = pd.DataFrame(table[1:])
    # df.columns = table[0]
    # html_template = Template(TEMPLATE_CONTENT)
    # return html_template.render(**{"tables": [df.to_html(classes='data')], "titles": df.columns.values})


@app.route('/download')
def download():
    start = request.args['start']
    end = request.args['end']
    tmp_path = '/tmp/curator-report'
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    dir_name = '{}-{}-koku-metrics'.format(start, end)
    outfile = dir_name + '.tar.gz'

    if not os.path.exists(os.path.join(tmp_path, dir_name)):
        os.makedirs(os.path.join(tmp_path, dir_name))

    conn, cur = postgres_connection()
    for i in range(4):
        conn, cur = postgres_connection()
        outputsql = "COPY " \
                    "(SELECT * " \
                    "FROM logs_" + str(i) + \
                    " WHERE interval_start >= '{}'::timestamp with time zone " \
                    "AND interval_end < '{}'::timestamp with time zone) " \
                    "TO STDOUT WITH CSV DELIMITER ',' HEADER" \
            .format(str(start), str(end))
        with open(os.path.join(tmp_path, os.path.join(dir_name, dir_name + '.{}.csv'.format(i))), 'w+') as f:
            cur.copy_expert(outputsql, f)
    conn.close()
    with tarfile.open(os.path.join(tmp_path, outfile), "w:gz") as tar:
        tar.add(os.path.join(tmp_path, dir_name), arcname=os.path.basename(dir_name))

    @after_this_request
    def remove_file(response):
        try:
            shutil.rmtree(os.path.join(tmp_path, dir_name))
            os.remove(os.path.join(tmp_path, outfile))
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response
    return send_file(os.path.join(tmp_path, outfile), as_attachment=True, attachment_filename=outfile)


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
