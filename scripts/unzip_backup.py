import os
import boto
from boto.s3.key import Key
import boto.s3.connection
import shutil
import tarfile
from botocore.exceptions import ClientError
import psycopg2
import csv
import time

#get all the environment variables
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")  
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME= os.environ.get("BUCKET_NAME")



conn = boto.s3.connection.S3Connection(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, port=443,
                                       host="kzn-swift.massopen.cloud", is_secure=True, calling_format=boto.s3.connection.OrdinaryCallingFormat())
bucket = conn.get_bucket(BUCKET_NAME)


backup_src = os.environ.get("BACKUP_SRC")  
unzip_dir =  os.environ.get("UNZIP_DIR")

#get all database variables
database_name = os.environ.get("DATABASE_NAME")
database_user=os.environ.get("DATABASE_USER")
database_password=os.environ.get("DATABASE_PASSWORD")
host_name=os.environ.get("HOST_NAME")
port=os.environ.get("PORT_NUMBER")


if not os.path.exists(unzip_dir):
    os.makedirs(unzip_dir)
# # Download the history file from s3 bucket

try:
    key = bucket.get_key('history.txt')
    if key is None:
        print("The history file is not found in s3 bucket")
        if not os.path.exists(os.path.join(unzip_dir,"history.txt")):
            with open(os.path.join(unzip_dir,"history.txt"),mode='w') as hf:
                hf.write("test")
        # upload the file into s3
        upkey = bucket.new_key('history.txt')
        upkey.set_contents_from_filename(os.path.join(unzip_dir,'history.txt'))
        # download the file from s3
        downkey = bucket.get_key('history.txt')
        downkey.get_contents_to_filename(os.path.join(unzip_dir,'history.txt'))
    else:
        key.get_contents_to_filename(os.path.join(unzip_dir,'history.txt'))
except ClientError as ex:
    # file not found 
    #  Create the history file
    print(ex)


#Push all data to database
def postgres_execute(sql_query, data=None) -> int:
    """
        Add the csv rows into database
    """
    try:
        conn = psycopg2.connect(database=database_name, user=database_user,
                                password=database_password, host=host_name, port=port) #postgres database connection string

        cursor = conn.cursor()
        if data:
            records_list = ','.join(['%s'] * len(data))
            sql_query = sql_query.format(records_list)
            cursor.execute(sql_query, data)
        else:
            cursor.execute(sql_query)
        conn.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")
        return count
    except Exception as ex:
        print(ex)
        return 0


class BatchUpdatePostgres:
    def __init__(self, update_sql="", batch_size=1000, std_log=True, sleep_interval=10):
        self.sql = update_sql
        self.rows = []
        self.batch_size = batch_size
        self.std_log = std_log
        self.sleep_interval = sleep_interval

    def sql_isempty(self):
        return len(self.sql) == 0

    def set_sql(self, update_sql):
        self.sql = update_sql

    def add(self, single_row):
        self.rows.append(single_row)
        if len(self.rows) >= self.batch_size:
            self.update()

    def clean(self):  # don't forget to call clean to flush changes into db after gathering all data
        self.update()

    def update(self, show_success=True) -> int:
        row_cnt = 0
        if not self.rows:
            return row_cnt
        write_success = False
        while not write_success:
            try:
                row_cnt = postgres_execute(self.sql, self.rows)
                write_success = True
            except Exception as e:
                if self.std_log:
                    print('when %s' % self.sql, e)
                time.sleep(self.sleep_interval)
        if self.std_log and not write_success:
            print("write failed")
        elif show_success:
            print("successfully updated %d items" % len(self.rows))
        self.rows = []
        return row_cnt


#Iterating to all csv files in unzipped folder and pusing them to it's respective database table.
def push_csv_to_db(extracted_csv_path):
    for bsubdir, bdirs, csvfiles in os.walk(extracted_csv_path):
        for csvf in csvfiles:
            if csvf.endswith(".csv"):
                csv_full_path = os.path.join(bsubdir, csvf)
                table_name_local = os.path.splitext(csv_full_path)
                table_name_local = table_name_local[0][-1]

                batch_executor = BatchUpdatePostgres()
                with open(csv_full_path, 'r') as f:
                    # Notice that we don't need the `csv` module.
                    next(f)  # Skip the header row.
                    reader = csv.reader(f)
                    for row in reader:
                        report_period_start = row[0].replace(" +0000 UTC", "")
                        report_period_end = row[1].replace(" +0000 UTC", "")
                        interval_start = row[2].replace(" +0000 UTC", "")
                        interval_end = row[3].replace(" +0000 UTC", "")

                        if table_name_local == "0":
                            table_name_sql = "logs_0"
                            namespace = row[4]
                            namespace_labels = row[5]
                            if batch_executor.sql_isempty():
                                batch_executor.set_sql("""INSERT INTO """ + table_name_sql + """(report_period_start, report_period_end, interval_start, interval_end, namespace, namespace_labels) VALUES {}""")
                            batch_executor.add((report_period_start, report_period_end, interval_start, interval_end, namespace, namespace_labels))

                        elif table_name_local == "1":
                            table_name_sql = "logs_1"
                            node = row[4]
                            node_labels = row[5]
                            if batch_executor.sql_isempty():
                                batch_executor.set_sql("""INSERT INTO """ + table_name_sql + """(report_period_start, report_period_end, interval_start, interval_end, node, node_labels) VALUES {}""")
                            batch_executor.add((report_period_start, report_period_end, interval_start, interval_end, node, node_labels))
                        elif table_name_local == "2":
                            table_name_sql = "logs_2"
                            node = row[4]
                            namespace = row[5]
                            pod = row[6]
                            pod_usage_cpu_core_seconds = row[7]
                            pod_request_cpu_core_seconds = row[8]
                            pod_limit_cpu_core_seconds = row[9]
                            pod_usage_memory_byte_seconds = row[10]
                            pod_request_memory_byte_seconds = row[11]
                            pod_limit_memory_byte_seconds = row[12]
                            node_capacity_cpu_cores = row[13]
                            node_capacity_cpu_core_seconds = row[14]
                            node_capacity_memory_bytes = row[15]
                            node_capacity_memory_byte_seconds = row[16]
                            resource_id = row[17]
                            pod_labels = row[18]
                            if batch_executor.sql_isempty():
                                batch_executor.set_sql("""INSERT INTO """ + table_name_sql + """(report_period_start, report_period_end, interval_start, interval_end, node, namespace, pod, pod_usage_cpu_core_seconds, pod_request_cpu_core_seconds, pod_limit_cpu_core_seconds,	pod_usage_memory_byte_seconds, pod_request_memory_byte_seconds, pod_limit_memory_byte_seconds, node_capacity_cpu_cores, node_capacity_cpu_core_seconds, node_capacity_memory_bytes, node_capacity_memory_byte_seconds, resource_id, pod_labels) VALUES {}""")
                            batch_executor.add((report_period_start, report_period_end, interval_start, interval_end, node, namespace, pod, pod_usage_cpu_core_seconds, pod_request_cpu_core_seconds, pod_limit_cpu_core_seconds,	pod_usage_memory_byte_seconds, pod_request_memory_byte_seconds, pod_limit_memory_byte_seconds, node_capacity_cpu_cores, node_capacity_cpu_core_seconds, node_capacity_memory_bytes, node_capacity_memory_byte_seconds, resource_id, pod_labels))
                        elif table_name_local == "3":
                            table_name_sql = "logs_3"
                            namespace = row[4]
                            pod = row[5]
                            persistentvolumeclaim = row[6]
                            persistentvolume = row[7]
                            storageclass = row[8]
                            persistentvolumeclaim_capacity_bytes = row[9]
                            persistentvolumeclaim_capacity_byte_seconds = row[10]
                            volume_request_storage_byte_seconds = row[11]
                            persistentvolumeclaim_usage_byte_seconds = row[12]
                            persistentvolume_labels = row[13]
                            persistentvolumeclaim_labels = row[14]
                            if batch_executor.sql_isempty():
                                batch_executor.set_sql("""INSERT INTO """ + table_name_sql + """(report_period_start, report_period_end, interval_start, interval_end, namespace, pod, persistentvolumeclaim, persistentvolume, storageclass, persistentvolumeclaim_capacity_bytes, persistentvolumeclaim_capacity_byte_seconds, volume_request_storage_byte_seconds, persistentvolumeclaim_usage_byte_seconds, persistentvolume_labels, persistentvolumeclaim_labels) VALUES {}""")
                            batch_executor.add((report_period_start, report_period_end, interval_start, interval_end, namespace, pod, persistentvolumeclaim, persistentvolume, storageclass, persistentvolumeclaim_capacity_bytes, persistentvolumeclaim_capacity_byte_seconds, volume_request_storage_byte_seconds, persistentvolumeclaim_usage_byte_seconds, persistentvolume_labels, persistentvolumeclaim_labels))

                    batch_executor.update()


def gunzip(file_path, output_path):
    try:
        file = tarfile.open(file_path)
        file.extractall(output_path)
        file.close()
        push_csv_to_db(output_path)
    except Exception as ex:
        print("Error is occured while extract the file {} and the error is {}".format(
            file_path, ex))


# Read the unzipped files history details
newly_unzipped_files = ""
unzipped_file_hist = ""
try:
    with open(os.path.join(unzip_dir, 'history.txt'), mode='r') as h_f:
        unzipped_file_hist = h_f.read()
except Exception as ex:
    print("An error is occured while read the history file {}".format(ex))

try:
    for bsubdir, bdirs, bfiles in os.walk(backup_src):
        for bf in bfiles:
            if bf.endswith(".gz") and not bf in unzipped_file_hist:
                backup_full_path = os.path.join(bsubdir, bf)
                file_folder = bf.split(".")[0]
                unzip_folder_dir = os.path.join(unzip_dir, file_folder)
                if not os.path.exists(unzip_folder_dir):
                    os.makedirs(unzip_folder_dir)
                gunzip(backup_full_path, unzip_folder_dir)
                for usubdir, udirs, ufiles in os.walk(unzip_folder_dir):
                    for uf in ufiles:
                        unzip_full_path = os.path.join(usubdir, uf)
                        uk = bucket.new_key(os.path.join(file_folder,uf))
                        uk.set_contents_from_filename(unzip_full_path)
                        print(unzip_full_path)
                newly_unzipped_files = "{}{}\n".format(newly_unzipped_files, bf)
                
                shutil.rmtree(unzip_folder_dir)
except Exception as ex:
    print("An error is occured while unzip the files into unzip directory {}".format(ex))

try:
    with open(os.path.join(unzip_dir, 'history.txt'), mode='a+') as h_f:
        h_f.write(newly_unzipped_files)

    hk = bucket.new_key('history.txt')
    # # upload the history files with newly unzipped folders
    hk.set_contents_from_filename(os.path.join(unzip_dir, 'history.txt'))
    os.remove(os.path.join(unzip_dir,'history.txt'))
except Exception as ex:
    print("Error is occured while push the updated history files into s3 {}".format(ex))
