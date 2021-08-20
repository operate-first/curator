import os
from typing import Tuple
import boto
from boto.s3.key import Key
import boto.s3.connection
import shutil
import tarfile
from botocore.exceptions import ClientError
import psycopg2
import csv

AWS_ACCESS_KEY_ID = os.environ.get(
    "AWS_ACCESS_KEY_ID")  # dir of the metrics files
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

conn = boto.s3.connection.S3Connection(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    port=443,
    host="kzn-swift.massopen.cloud",
    is_secure=True,
    calling_format=boto.s3.connection.OrdinaryCallingFormat(),
)
bucket = conn.get_bucket(BUCKET_NAME)

backup_src = os.environ.get("BACKUP_SRC")  # dir of the metrics files
unzip_dir = os.environ.get("UNZIP_DIR")  # dir of the metrics files
database_name = os.environ.get("DATABASE_NAME")
database_user = os.environ.get("DATABASE_USER")
database_password = os.environ.get("DATABASE_PASSWORD")
host_name = os.environ.get("HOST_NAME")
port = os.environ.get("PORT_NUMBER")
has_s3_access = os.environ.get("HAS_S3_ACCESS")

if not os.path.exists(unzip_dir):
    os.makedirs(unzip_dir)
# # Download the history file from s3 bucket


def get_history_file():
    try:
        key = bucket.get_key("history.txt")
        if key is None:
            print("The history file is not found in s3 bucket")
            if not os.path.exists(os.path.join(unzip_dir, "history.txt")):
                with open(os.path.join(unzip_dir, "history.txt"), mode="w") as hf:
                    hf.write("test")
            # upload the file into s3
            upkey = bucket.new_key("history.txt")
            upkey.set_contents_from_filename(
                os.path.join(unzip_dir, "history.txt"))
            # download the file from s3
            downkey = bucket.get_key("history.txt")
            downkey.get_contents_to_filename(
                os.path.join(unzip_dir, "history.txt"))
        else:
            key.get_contents_to_filename(
                os.path.join(unzip_dir, "history.txt"))
    except ClientError as ex:
        print(ex)


def update_history_data(sql_query):
    '''
        Update the history data
    '''
    is_updated = True
    try:
        conn = psycopg2.connect(
            database=database_name,
            user=database_user,
            password=database_password,
            host=host_name,
            port=port,
        )

        cursor = conn.cursor()

        cursor.execute(sql_query)

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as ex:
        is_updated = False
        print(ex)
    return is_updated


def get_history_data():
    history = ""
    try:
        conn = psycopg2.connect(
            database=database_name,
            user=database_user,
            password=database_password,
            host=host_name,
            port=port,
        )

        cursor = conn.cursor()

        cursor.execute("select file_names from history")
        history = cursor.fetchone()

        cursor.close()
        conn.close()
    except Exception as ex:
        print(ex)
    return history


def add_csv_data(sql_query):
    """
    Add the csv rows into database
    """
    count = 0
    try:
        conn = psycopg2.connect(
            database=database_name,
            user=database_user,
            password=database_password,
            host=host_name,
            port=port,
        )

        cursor = conn.cursor()

        cursor.execute(sql_query)

        conn.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")
        cursor.close()
        conn.close()
    except Exception as ex:
        print(ex)
    return count


def push_csv_to_db(extracted_csv_path):
    rowcount = 0
    try:
        for bsubdir, bdirs, csvfiles in os.walk(extracted_csv_path):
            for csvf in csvfiles:
                if csvf.endswith(".csv"):
                    csv_full_path = os.path.join(bsubdir, csvf)
                    table_name_local = os.path.splitext(csv_full_path)
                    table_name_local = table_name_local[0][-1]

                    table_name_sql = "logs_0"

                    with open(csv_full_path, "r") as f:
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
                                query = """INSERT INTO {}(report_period_start, report_period_end, interval_start, interval_end, namespace, namespace_labels) VALUES('{}','{}','{}','{}','{}','{}')""".format(
                                    table_name_sql,
                                    report_period_start,
                                    report_period_end,
                                    interval_start,
                                    interval_end,
                                    namespace,
                                    namespace_labels,
                                )

                            elif table_name_local == "1":
                                table_name_sql = "logs_1"
                                node = row[4]
                                node_labels = row[5]
                                query = """INSERT INTO {}(report_period_start, report_period_end, interval_start, interval_end, node, node_labels) VALUES('{}','{}','{}','{}','{}','{}')""".format(
                                    table_name_sql,
                                    report_period_start,
                                    report_period_end,
                                    interval_start,
                                    interval_end,
                                    node,
                                    node_labels,
                                )
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
                                query = """INSERT INTO {}(report_period_start, report_period_end, interval_start, interval_end, node, namespace, pod, pod_usage_cpu_core_seconds, pod_request_cpu_core_seconds, pod_limit_cpu_core_seconds,	pod_usage_memory_byte_seconds, pod_request_memory_byte_seconds, pod_limit_memory_byte_seconds, node_capacity_cpu_cores, node_capacity_cpu_core_seconds, node_capacity_memory_bytes, node_capacity_memory_byte_seconds, resource_id, pod_labels) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(
                                    table_name_sql,
                                    report_period_start,
                                    report_period_end,
                                    interval_start,
                                    interval_end,
                                    node,
                                    namespace,
                                    pod,
                                    pod_usage_cpu_core_seconds,
                                    pod_request_cpu_core_seconds,
                                    pod_limit_cpu_core_seconds,
                                    pod_usage_memory_byte_seconds,
                                    pod_request_memory_byte_seconds,
                                    pod_limit_memory_byte_seconds,
                                    node_capacity_cpu_cores,
                                    node_capacity_cpu_core_seconds,
                                    node_capacity_memory_bytes,
                                    node_capacity_memory_byte_seconds,
                                    resource_id,
                                    pod_labels,
                                )
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
                                query = """INSERT INTO {}(report_period_start, report_period_end, interval_start, interval_end, namespace, pod, persistentvolumeclaim, persistentvolume, storageclass, persistentvolumeclaim_capacity_bytes, persistentvolumeclaim_capacity_byte_seconds, volume_request_storage_byte_seconds, persistentvolumeclaim_usage_byte_seconds, persistentvolume_labels, persistentvolumeclaim_labels) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(
                                    table_name_sql,
                                    report_period_start,
                                    report_period_end,
                                    interval_start,
                                    interval_end,
                                    namespace,
                                    pod,
                                    persistentvolumeclaim,
                                    persistentvolume,
                                    storageclass,
                                    persistentvolumeclaim_capacity_bytes,
                                    persistentvolumeclaim_capacity_byte_seconds,
                                    volume_request_storage_byte_seconds,
                                    persistentvolumeclaim_usage_byte_seconds,
                                    persistentvolume_labels,
                                    persistentvolumeclaim_labels,
                                )

                            rowcount = add_csv_data(query)
    except Exception as ex:
        print("An error is occured {0}".format(ex))
    return rowcount


def gunzip(file_path, output_path, is_push_db=True):
    try:
        file = tarfile.open(file_path)
        file.extractall(output_path)
        file.close()
        if is_push_db:
            push_csv_to_db(output_path)
    except Exception as ex:
        print(
            "Error is occured while extract the file {} and the error is {}".format(
                file_path, ex
            )
        )


def move_unzipped_files_into_s3(unzip_folder_dir, file_folder):
    moved_files_count = 0
    try:
        for usubdir, udirs, ufiles in os.walk(unzip_folder_dir):
            for uf in ufiles:
                unzip_full_path = os.path.join(usubdir, uf)
                uk = bucket.new_key(os.path.join(file_folder, uf))
                uk.set_contents_from_filename(unzip_full_path)
                print(unzip_full_path)
                moved_files_count = +1
    except Exception as exp:
        print("An error is occured while move files into s3 {0}".format(exp))
    return moved_files_count


if __name__ == "__main__":
    newly_unzipped_files = ""
    unzipped_file_hist = ""

    if has_s3_access.upper() == "TRUE":
        get_history_file()
    else:
        unzipped_file_hist = get_history_data()
        if unzipped_file_hist: 
            unzipped_file_hist = unzipped_file_hist.split("\n")

    # Read the unzipped files history details
    try:
        with open(os.path.join(unzip_dir, "history.txt"), mode="r") as h_f:
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
                    if has_s3_access.upper() == "TRUE":
                        moved_files_count = move_unzipped_files_into_s3(
                            unzip_folder_dir, file_folder)
                    newly_unzipped_files = "{}{}\n".format(
                        newly_unzipped_files, bf)
                    shutil.rmtree(unzip_folder_dir)

    except Exception as ex:
        print(
            "An error is occured while unzip the files into unzip directory {}".format(
                ex)
        )
    if has_s3_access.upper() == "TRUE":
        try:
            with open(os.path.join(unzip_dir, "history.txt"), mode="a+") as h_f:
                h_f.write(newly_unzipped_files)

            hk = bucket.new_key("history.txt")
            # # upload the history files with newly unzipped folders
            hk.set_contents_from_filename(
                os.path.join(unzip_dir, "history.txt"))
            os.remove(os.path.join(unzip_dir, "history.txt"))
        except Exception as ex:
            print(
                "Error is occured while push the updated history files into s3 {}".format(ex))
    else:
        query = "INSERT INTO HISTORY VALUES ('{}')".format(newly_unzipped_files)
        update_history_data(query)
