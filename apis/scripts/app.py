from flask import Flask, request, jsonify
from postgres_interface import postgres_execute
from report_interface import get_report
from kubernetes import client, config
from openshift.dynamic import DynamicClient
import dateutil.parser
app = Flask(__name__)


@app.route('/report')
def report():
    resp = get_report(request.args)  # TODO status code
    print(resp)
    sql = "select * from generate_report_api('{}', '{}') where namespace='{}'".format(resp['spec']['reportPeriod'].lower(),
                                                              resp['spec']['reportingEnd'],
                                                              resp['spec']['namespace'])
    table = postgres_execute(sql, result=True)
    print(table)
    return jsonify(table)


if __name__ == '__main__':
    app.run()
