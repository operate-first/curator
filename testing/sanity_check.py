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
database_host_name = ''
port = ''
bearer_token = "sha256~xx"


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

def isclose(a, b, rel_tol=.05):
    return abs(a-b) <= rel_tol * max(abs(a), abs(b))


start_of_today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
offset = datetime.utcnow() - start_of_today
s = offset.seconds
hours, remainder = divmod(s, 3600)
minutes, seconds = divmod(remainder, 60)
offset_str = "{}h{}m{}s{}ms".format(hours, minutes, seconds, offset.microseconds // 1000)
# $ oc project openshift-monitoring; oc get routes
curator_url = "http://prometheus-k8s-openshift-monitoring.apps.curator.massopen.cloud"
auth_header = {"Authorization": "Bearer " + bearer_token}
prom = PrometheusConnect(url=curator_url, headers=auth_header, disable_ssl=True)
dbresp = postgres_execute("SELECT * FROM reports_human WHERE interval_end = '{}' and frequency = 'day'"
                          .format(start_of_today), result=True)
print('Testing result for [1d] report ending GMT', start_of_today - timedelta(seconds=1))

for record in dbresp:
    if not record[3]:
        continue
    memory_correct = False
    metric_data = prom.custom_query_range(
        "sum(sum(container_memory_usage_bytes{container!='POD', container!='', pod!='', namespace='"
        + str(record[3]) + "'} / 1024 / 1024) by (node, namespace, pod)) by (namespace)",
        start_time=start_of_today - timedelta(days=1, hours=6),  # utc - 6 hrs
        end_time=start_of_today - timedelta(hours=6, seconds=1),  # end_time is inclusive, use 23:59:59
        step=str(3600)  # 3600 * 24 seconds per day
    )
    memory_result = sum(float(i[1]) for i in metric_data[0]['values']) / len(metric_data[0]['values'])
    # memory_result = float(metric_data[0]['values'][-1][1])
    if isclose(memory_result, record[7]):  # col 7. pod memory usage
        memory_correct = True
    else:
        # print(metric_data)
        print(colored('[ERROR] namespace {} memory expected {} but got {}'.format(record[3], memory_result
                                                                           , record[7]), 'red'))
    metric_data = prom.custom_query(
        "sum(sum(rate(container_cpu_usage_seconds_total{container!='POD',container!='',pod!='', namespace='"
        + str(record[3]) + "'}[1d] offset " + offset_str + ")) BY (pod, namespace, node)) BY (namespace) * 1000",
        # start_time=start_of_today - timedelta(days=1, hours=6),  # utc - 6 hrs
        # end_time=start_of_today - timedelta(hours=6, seconds=1),  # end_time is inclusive, use 23:59:59
        # step=str(3600)  # 3600 * 24 seconds per day
    )
    # cpu_result = sum(float(i[1]) for i in metric_data[0]['values']) / len(metric_data[0]['values'])
    cpu_result = float(metric_data[0]['value'][-1])
    if memory_correct and isclose(cpu_result, record[4]):  # col 4. pod cpu usage
        print(colored(f'[PASS] cpu/memory test pass {record[3]}', 'green'))
    elif memory_correct:
        # print(metric_data)
        print(colored('[ERROR] namespace {} cpu expected {} but got {}'.format(record[3], cpu_result
                                                                           , record[4]), 'red'))
