from datetime import datetime
import psycopg2
from datetime import timedelta
from prometheus_api_client import PrometheusConnect
import warnings
from termcolor import colored
warnings.filterwarnings("ignore")

database_name = ''
database_user = ''
database_password = ''
database_host_name = 'localhost'
port = ''
bearer_token = "sha256~xx"
target_prometheus = "http://prometheus-k8s-openshift-monitoring.apps.smaug.na.operate-first.cloud"

REL_TOLERANCE = .05  # relative tolerance


def postgres_execute(sql_query, data=None, result=False, header=False):
    """

    :param sql_query: query to be run
    :param data: List of List; data[i] represents one record to be insert
        when None, sql_query is a complete sql query
        when Not None, sql_query is contains formatting string {}
    :return: Number of rows successfully inserted
    """

    conn = psycopg2.connect(database=database_name, user=database_user,
                            password=database_password, host=database_host_name, port=port)

    cursor = conn.cursor()
    if data:
        records_list = ','.join(['%s'] * len(data))
        sql_query = sql_query.format(records_list)
        cursor.execute(sql_query, data)
    else:
        cursor.execute(sql_query)
    conn.commit()
    count = cursor.rowcount
    if not result:
        # print(count, "Record inserted successfully into table")
        conn.close()
        return count
    else:
        result_list = []
        if header:
            result_list.append([desc[0] for desc in cursor.description])
        for i in range(count):
            record = cursor.fetchone()
            result_list.append(record)
        conn.close()
        return result_list


def isclose(a, b, rel_tol=REL_TOLERANCE):
    return abs(a-b) <= rel_tol * max(abs(a), abs(b))


start_of_today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
offset = datetime.utcnow() - start_of_today
s = offset.seconds
hours, remainder = divmod(s, 3600)
minutes, seconds = divmod(remainder, 60)
offset_str = "{}h{}m{}s{}ms".format(hours, minutes, seconds, offset.microseconds // 1000)

auth_header = {"Authorization": "Bearer " + bearer_token}
prom = PrometheusConnect(url=target_prometheus, headers=auth_header, disable_ssl=True)
response = postgres_execute("SELECT * FROM reports_human WHERE interval_end = '{}' and frequency = 'day'"
                            .format(start_of_today), result=True)
print('Testing result for [1d] report ending GMT', start_of_today - timedelta(seconds=1))
sample = [['Namespace', 'isAccurate',
           'Prometheus CPU Report', 'Curator CPU Report',
           'Prometheus Memory Report', 'Curator Memory Report']]
for row in response:
    if not row[3]:
        continue
    memory_correct = False
    metric_data = prom.custom_query_range(
        "sum(sum(container_memory_usage_bytes{container!='POD', container!='', pod!='', namespace='"
        + str(row[3]) + "'} / 1024 / 1024) by (node, namespace, pod)) by (namespace)",
        start_time=start_of_today - timedelta(days=1, hours=6),  # utc - 6 hrs
        end_time=start_of_today - timedelta(hours=6, seconds=1),  # end_time is inclusive, use 23:59:59
        step=str('1m')  # consistent with koku-metrics-operator step
    )
    try:
        memory_result = sum(float(i[1]) for i in metric_data[0]['values']) / len(metric_data[0]['values'])
    except IndexError as e:
        print('[INFO] no matching namespace: {} in prometheus'.format(row[3]))
        continue
    if isclose(memory_result, row[7]):  # col 7. pod memory usage
        memory_correct = True
    else:
        print(colored('[ERROR] namespace {} memory expected {} but got {}'.format(row[3], memory_result
                                                                                  , row[7]), 'red'))
    metric_data = prom.custom_query(
        "sum(sum(rate(container_cpu_usage_seconds_total{container!='POD',container!='',pod!='', namespace='"
        + str(row[3]) + "'}[1d] offset " + offset_str + ")) BY (pod, namespace, node)) BY (namespace) * 1000",
    )
    try:
        cpu_result = float(metric_data[0]['value'][-1])
    except IndexError as e:
        print('[INFO] no matching namespace: {} in prometheus'.format(row[3]))
        continue
    if memory_correct and isclose(cpu_result, row[4]):  # col 4. pod cpu usage
        print(colored(f'[PASS] cpu/memory test pass {row[3]}', 'green'))
    elif memory_correct:
        print(colored('[ERROR] namespace {} cpu expected {} but got {}'.format(row[3], cpu_result
                                                                           , row[4]), 'red'))
    sample.append([row[3], '✅' if memory_correct and isclose(cpu_result, row[4]) else '❌', cpu_result, row[4],
                   memory_result, row[7]])

# save result as markdown
sample.sort(key=lambda x: (x[1] == 'isAccurate', x[1]), reverse=True)
markdown = str("| ")
for e in sample[0]:
    to_add = " " + str(e) + str(" |")
    markdown += to_add
markdown += "\n"

markdown += '|'
for i in range(len(sample[0])):
    markdown += str("-------------- | ")
markdown += "\n"
for entry in sample[1:]:
    markdown += str("| ")
    for e in entry:
        to_add = str(e) + str(" | ")
        markdown += to_add
    markdown += "\n"
with open('sanity_check_result.md', 'w+') as fd:
    fd.write(markdown)

