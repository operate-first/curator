from flask import Flask, request, jsonify
from postgres_interface import postgres_execute
from kubernetes import client, config
from openshift.dynamic import DynamicClient

app = Flask(__name__)


@app.route('/report')
def report():
    config.load_incluster_config()
    k8s_client = client.ApiClient()
    dyn_client = DynamicClient(k8s_client)
    report = dyn_client.resources.get(api_version='batch.curator.openshift.io/v1', kind='Report')
    resp = report.get(name=request.args['reportName'], namespace=request.args['reportNamespace'])
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
