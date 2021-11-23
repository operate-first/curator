import psycopg2, time, os

database_name = os.environ.get("DATABASE_NAME")
database_user = os.environ.get("DATABASE_USER")
database_password = os.environ.get("DATABASE_PASSWORD")
database_host_name = os.environ.get("DATABASE_HOST_NAME")
port = os.environ.get("PORT_NUMBER")


def update_history_data(sql_query):
    '''
        Update the history data
    '''
    is_updated = True
    conn = None
    conn = psycopg2.connect(
        database=database_name,
        user=database_user,
        password=database_password,
        host=database_host_name,
        port=port,
    )
    cursor = conn.cursor()

    cursor.execute(sql_query)

    conn.commit()
    cursor.close()
    conn.close()
    is_updated = False
    return is_updated


def get_history_data():
    history = []
    conn = None
    conn = psycopg2.connect(database=database_name, user=database_user,
                            password=database_password, host=database_host_name, port=port) #postgres database connection string

    cursor = conn.cursor()

    cursor.execute("select file_names from history")
    # history = cursor.fetchone()
    rows = cursor.fetchall()
    for row in rows:
        history.append(row[0])
    cursor.close()
    conn.close()
    return history


def postgres_execute(sql_query, data=None, result=False, header=False):
    """

    :param sql_query: query to be run
    :param data: List of List; data[i] represents one record to be insert
        when None, sql_query is a complete sql query
        when Not None, sql_query is contains formatting string {}
    :return: Number of rows successfully inserted
    """

    conn = psycopg2.connect(database=database_name, user=database_user,
                            password=database_password, host=database_host_name, port=port) #postgres database connection string

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
        print(count, "Record inserted successfully into table")
        conn.close()
        return count
    else:
        result_list = []
        for i in range(count):
            record = cursor.fetchone()
            result_list.append(record)
        conn.close()
        return result_list


class BatchUpdatePostgres:
    """
    Batch Execution Buffer
    """
    def __init__(self, update_sql="", batch_size=1000, std_log=True, test_threshold=10, sleep_interval=10):
        self.sql = update_sql
        self.rows = []
        self.batch_size = batch_size
        self.std_log = std_log
        self.sleep_interval = sleep_interval
        self.test_threshold = test_threshold
        self.total_row = 0
        self.success = True

    def sql_isempty(self):
        return len(self.sql) == 0

    def set_sql(self, update_sql):
        self.sql = update_sql

    def add(self, single_row):
        self.rows.append(single_row)
        if len(self.rows) >= self.batch_size:
            self.update()

    def clean(self) -> int:  # don't forget to call clean to flush changes into db after gathering all data
        self.update()
        return self.total_row if self.success else -1

    def update(self, show_success=True):
        row_cnt = 0
        if not self.rows:
            return
        write_success = False
        test_cnt = 0
        while not write_success and test_cnt < self.test_threshold:
            try:
                row_cnt = postgres_execute(self.sql, self.rows)
                write_success = True
            except Exception as e:
                if self.std_log:
                    print('when %s' % self.sql, e)
                time.sleep(self.sleep_interval)
                test_cnt += 1
        if self.std_log and not write_success:
            print("write failed")
        elif show_success:
            print("successfully updated %d items" % len(self.rows))
        self.success &= write_success
        self.rows = []
        self.total_row += row_cnt
