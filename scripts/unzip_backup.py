import os
from boto.s3.key import Key
import boto.s3.connection
import shutil
import tarfile
from botocore.exceptions import ClientError
from datetime import datetime, timezone
import csv, json
from postgres_interface import get_history_data, BatchUpdatePostgres,postgres_execute


AWS_ACCESS_KEY_ID = os.environ.get(
    "AWS_ACCESS_KEY_ID")  # dir of the metrics files
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
S3_HOST_NAME= os.environ.get("S3_HOST_NAME")
has_s3_access = os.environ.get("HAS_S3_ACCESS").lower() in ('true', 't', 'y', 'yes')

if has_s3_access:
    conn = boto.s3.connection.S3Connection(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, port=443,
                                           host=S3_HOST_NAME, is_secure=True, calling_format=boto.s3.connection.OrdinaryCallingFormat())
    bucket = conn.get_bucket(BUCKET_NAME)

backup_src = os.environ.get("BACKUP_SRC")  # dir of the metrics files
unzip_dir = os.environ.get("UNZIP_DIR")  # dir of the metrics files


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


def push_csv_to_db(extracted_csv_path):
    rowcount = 0
    manifest = json.dumps(dict())
    for bsubdir, _, csvfiles in os.walk(extracted_csv_path):
        for csvf in csvfiles:
            if csvf.endswith(".csv"):
                csv_full_path = os.path.join(bsubdir, csvf)
                table_name_local = os.path.splitext(csv_full_path)
                table_name_local = table_name_local[0][-1]

                batch_executor = BatchUpdatePostgres()

                with open(csv_full_path, "r") as f:
                    # Notice that we don't need the `csv` module.
                    next(f)  # Skip the header row.
                    reader = csv.reader(f)

                    for row in reader:
                        report_period_start = row[0].replace(" UTC", "")
                        report_period_end = row[1].replace(" UTC", "")
                        interval_start = row[2].replace(" UTC", "")
                        interval_end = row[3].replace(" UTC", "")

                        if table_name_local == "0":
                            table_name_sql = "logs_0"
                            namespace = row[4]
                            namespace_labels = row[5]
                            if batch_executor.sql_isempty():
                                batch_executor.set_sql(
                                    """INSERT INTO """ + table_name_sql + """(report_period_start, report_period_end, interval_start, interval_end, namespace, namespace_labels) VALUES {}""")
                            batch_executor.add((
                                                report_period_start, report_period_end, interval_start, interval_end,
                                                namespace, namespace_labels))

                        elif table_name_local == "1":
                            table_name_sql = "logs_1"
                            node = row[4]
                            node_labels = row[5]
                            if batch_executor.sql_isempty():
                                batch_executor.set_sql(
                                    """INSERT INTO """ + table_name_sql + """(report_period_start, report_period_end, interval_start, interval_end, node, node_labels) VALUES {}""")
                            batch_executor.add((
                                                report_period_start, report_period_end, interval_start, interval_end,
                                                node, node_labels))
                        elif table_name_local == "2":
                            table_name_sql = "logs_2"
                            node = row[4]
                            namespace = row[5]
                            pod = row[6]
                            pod_usage_cpu_core_seconds = row[7] if row[7].strip() !="" else None
                            pod_request_cpu_core_seconds = row[8] if row[8].strip() !="" else None
                            pod_limit_cpu_core_seconds = row[9] if row[9].strip() !="" else None
                            pod_usage_memory_byte_seconds = row[10] if row[10].strip() !="" else None
                            pod_request_memory_byte_seconds = row[11] if row[11].strip() !="" else None
                            pod_limit_memory_byte_seconds = row[12] if row[12].strip() !="" else None
                            node_capacity_cpu_cores = row[13] if row[13].strip() !="" else None
                            node_capacity_cpu_core_seconds = row[14] if row[14].strip() !="" else None
                            node_capacity_memory_bytes = row[15] if row[15].strip() !="" else None
                            node_capacity_memory_byte_seconds = row[16] if row[16].strip() !="" else None
                            resource_id = row[17]
                            pod_labels = row[18]
                            if batch_executor.sql_isempty():
                                batch_executor.set_sql(
                                    """INSERT INTO """ + table_name_sql + """(report_period_start, report_period_end, interval_start, interval_end, node, namespace, pod, pod_usage_cpu_core_seconds, pod_request_cpu_core_seconds, pod_limit_cpu_core_seconds,	pod_usage_memory_byte_seconds, pod_request_memory_byte_seconds, pod_limit_memory_byte_seconds, node_capacity_cpu_cores, node_capacity_cpu_core_seconds, node_capacity_memory_bytes, node_capacity_memory_byte_seconds, resource_id, pod_labels) VALUES {}""")
                            batch_executor.add((
                                                report_period_start, report_period_end, interval_start, interval_end,
                                                node, namespace, pod, pod_usage_cpu_core_seconds,
                                                pod_request_cpu_core_seconds, pod_limit_cpu_core_seconds,
                                                pod_usage_memory_byte_seconds, pod_request_memory_byte_seconds,
                                                pod_limit_memory_byte_seconds, node_capacity_cpu_cores,
                                                node_capacity_cpu_core_seconds, node_capacity_memory_bytes,
                                                node_capacity_memory_byte_seconds, resource_id, pod_labels))
                        elif table_name_local == "3":
                            table_name_sql = "logs_3"
                            namespace = row[4]
                            pod = row[5]
                            persistentvolumeclaim = row[6]
                            persistentvolume = row[7]
                            storageclass = row[8]
                            persistentvolumeclaim_capacity_bytes = row[9] if row[9].strip() !="" else None
                            persistentvolumeclaim_capacity_byte_seconds = row[10] if row[10].strip() !="" else None
                            volume_request_storage_byte_seconds = row[11] if row[11].strip() !="" else None
                            persistentvolumeclaim_usage_byte_seconds = row[12] if row[12].strip() !="" else None
                            persistentvolume_labels = row[13]
                            persistentvolumeclaim_labels = row[14]
                            if batch_executor.sql_isempty():
                                batch_executor.set_sql(
                                    """INSERT INTO """ + table_name_sql + """(report_period_start, report_period_end, interval_start, interval_end, namespace, pod, persistentvolumeclaim, persistentvolume, storageclass, persistentvolumeclaim_capacity_bytes, persistentvolumeclaim_capacity_byte_seconds, volume_request_storage_byte_seconds, persistentvolumeclaim_usage_byte_seconds, persistentvolume_labels, persistentvolumeclaim_labels) VALUES {}""")
                            batch_executor.add((
                                                report_period_start, report_period_end, interval_start, interval_end,
                                                namespace, pod, persistentvolumeclaim, persistentvolume,
                                                storageclass, persistentvolumeclaim_capacity_bytes,
                                                persistentvolumeclaim_capacity_byte_seconds,
                                                volume_request_storage_byte_seconds,
                                                persistentvolumeclaim_usage_byte_seconds, persistentvolume_labels,
                                                persistentvolumeclaim_labels))

                    batch_rowcount = batch_executor.clean()
                    if batch_rowcount >= 0 and rowcount >= 0:
                        rowcount += batch_rowcount
                    else:
                        rowcount = -1
            elif csvf.endswith(".json"):
                csv_full_path = os.path.join(bsubdir, csvf)
                with open(csv_full_path, 'r') as fd:
                    try:
                        manifest = json.dumps(json.load(fd))  # dump into string
                    except Exception as e:
                        print('Fail to read manifest.json for ', bsubdir)
                        print(e)
    return rowcount, manifest


def gunzip(file_path, output_path, is_push_db=True):
    file = tarfile.open(file_path)
    file.extractall(output_path)
    file.close()
    # if is_push_db:
    #     push_csv_to_db(output_path)


def move_unzipped_files_into_s3(unzip_folder_dir, file_folder):
    moved_files_count = 0
    try:
        for usubdir, _, ufiles in os.walk(unzip_folder_dir):
            for uf in ufiles:
                unzip_full_path = os.path.join(usubdir, uf)
                uk = bucket.new_key(os.path.join(file_folder, uf))
                uk.set_contents_from_filename(unzip_full_path)
                print(unzip_full_path)
                moved_files_count += 1
    except Exception as exp:
        print("An error is occured while move files into s3 {0}".format(exp))
    return moved_files_count


if __name__ == "__main__":    
    s3_unzipped_file_hist = ""
    s3_newly_unzipped_file_hist = ""
    db_newly_unzipped_file_hist = []
    if has_s3_access:
        get_history_file()
        # Read the unzipped files history details
        try:
            with open(os.path.join(unzip_dir, "history.txt"), mode="r") as h_f:
                s3_unzipped_file_hist = h_f.readlines()
                # s3_zipped_file_hist = s3_zipped_file_hist.split("\n") 
        except Exception as ex:
            print("An error is occured while read the history file {}".format(ex))
    
    db_unzipped_file_hist = set(get_history_data())  # list lookup? use set
    # if db_zipped_file_hist:
    #     db_zipped_file_hist = db_zipped_file_hist.split("~")    

    try:
        for bsubdir, _, bfiles in os.walk(backup_src):
            for bf in bfiles:
                if bf.endswith(".gz"):
                    backup_full_path = os.path.join(bsubdir, bf)
                    file_folder = bf.split(".")[0]
                    unzip_folder_dir = os.path.join(unzip_dir, file_folder)
                    if not os.path.exists(unzip_folder_dir):
                        os.makedirs(unzip_folder_dir)
                    gunzip(backup_full_path, unzip_folder_dir)
                    if has_s3_access and not bf in s3_unzipped_file_hist:
                        moved_files_count = move_unzipped_files_into_s3(
                            unzip_folder_dir, file_folder)

                        s3_newly_unzipped_file_hist = "{}\n{}".format(s3_newly_unzipped_file_hist, bf)
                    if not bf in db_unzipped_file_hist:
                        push_rowcnt, manifest = push_csv_to_db(unzip_folder_dir)
                        # update history every time. this prevents data and metadata inconsistency
                        postgres_execute("INSERT INTO history(file_names, manifest, success, crtime) VALUES {}",
                                         [(bf, manifest, push_rowcnt > 0, datetime.now(timezone.utc))])

                    shutil.rmtree(unzip_folder_dir)

    except Exception as ex:
        print("An error is occured while unzip the files into unzip directory {}".format(ex))
    if has_s3_access:
        try:
            with open(os.path.join(unzip_dir, "history.txt"), mode="a+") as h_f:
                h_f.write(s3_newly_unzipped_file_hist)

            hk = bucket.new_key("history.txt")
            # # upload the history files with newly unzipped folders
            hk.set_contents_from_filename(
                os.path.join(unzip_dir, "history.txt"))
            os.remove(os.path.join(unzip_dir, "history.txt"))
        except Exception as ex:
            print(
                "Error is occured while push the updated history files into s3 {}".format(ex))
