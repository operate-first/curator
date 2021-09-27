from kubernetes import client, config
from openshift.dynamic import DynamicClient

config.load_incluster_config()
k8s_client = client.ApiClient()
dyn_client = DynamicClient(k8s_client)
report = dyn_client.resources.get(api_version='batch.curator.openshift.io/v1', kind='Report')


def get_report(request_args):
    resp = report.get(name=request_args['reportName'], namespace=request_args['reportNamespace'])
    return resp