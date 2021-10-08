# python -W ignore scripts/http_test.py
import yaml
import unittest
from report_interface import report
import requests
import openshift
import warnings
warnings.filterwarnings("ignore")

yaml_valid = '''
apiVersion: batch.curator.openshift.io/v1
kind: Report
namespace: report-system
metadata:
  name: report-test-valid
spec:
  # Add fields here
  reportPeriod: Week
  namespace: koku-metrics-operator
  reportingEnd: "2021-08-26T00:00:00Z"
  schedule: "*/1 * * * *"  # schedule a time to generate and email report
'''

yaml_invalid = '''
apiVersion: batch.curator.openshift.io/v1
kind: Report
namespace: report-system
metadata:
  name: report-test-invalid
spec:
  # Add fields here
  reportPeriod: Week
  namespace: koku-metrics-operator
  reportingEnd: "2022-08-26T00:00:00Z"
  schedule: "*/1 * * * *"  # schedule a time to generate and email report
'''

valid_q = {'reportName': 'report-test-valid', 'reportNamespace': 'report-system'}
invalid_q = {'reportName': 'report-test-invalid', 'reportNamespace': 'report-system'}
badname_q = {'reportName': 'report-non-exist', 'reportNamespace': 'report-system'}


class TestHttpEndpoint(unittest.TestCase):
    def setUp(self):

        self.session = requests.Session()
        try:
            report.create(body=yaml.load(yaml_invalid), namespace='report-system')
            report.create(body=yaml.load(yaml_valid), namespace='report-system')
        except openshift.dynamic.exceptions.ConflictError:
            pass
        super().setUp()

    def tearDown(self):
        self.session.close()
        try:
            report.delete(name='report-test-invalid', namespace='report-system')
            report.delete(name='report-test-valid', namespace='report-system')
        except Exception:
            pass

    def test_valid(self):
        r = self.session.get('http://localhost:5000/report?'+'&'.join(['{}={}'.format(k, v) for k, v in valid_q.items()]))
        self.assertEqual(200, r.status_code)

    def test_future_timestamp(self):
        r = self.session.get('http://localhost:5000/report?'+'&'.join(['{}={}'.format(k, v) for k, v in invalid_q.items()]))
        self.assertEqual(400, r.status_code)

    def test_missing_keypair(self):
        r = self.session.get('http://localhost:5000/report?'+'&'.join(['{}={}'.format(k, v) for k, v in list(valid_q.items())[1:]]))
        self.assertEqual(400, r.status_code)

    def test_bad_reportName(self):
        r = self.session.get('http://localhost:5000/report?'+'&'.join(['{}={}'.format(k, v) for k, v in badname_q.items()]))
        self.assertEqual(404, r.status_code)


if __name__ == '__main__':
    unittest.main()
