from flask import Flask, request, jsonify
from postgres_interface import postgres_execute
from report_interface import get_report
from kubernetes import client, config
from openshift.dynamic import DynamicClient

app = Flask(__name__)


@app.route('/report')
def report():
    resp = get_report(request.args)  # TODO status code
    print(resp)
    sql = "select * from reports where namespace={} and frequency= '{}'".format(resp['spec']['namespace'],
                                                                                resp['spec']['reportPeriod'].lower())
    # for k, v in request.args.items():
    #     sql += " AND {} = '{}' ".format(k, v)
    # print(sql)
    table = postgres_execute(sql, result=True)
    print(table)
    return jsonify(table)


if __name__ == '__main__':
    app.run()
