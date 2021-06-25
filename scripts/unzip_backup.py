import os
import boto
from boto.s3.key import Key
import boto.s3.connection
import shutil
import tarfile
from botocore.exceptions import ClientError


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")  # dir of the metrics files
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME= os.environ.get("BUCKET_NAME")



conn = boto.s3.connection.S3Connection(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, port=443,
                                       host="kzn-swift.massopen.cloud", is_secure=True, calling_format=boto.s3.connection.OrdinaryCallingFormat())
bucket = conn.get_bucket(BUCKET_NAME)


backup_src = os.environ.get("BACKUP_SRC")  # dir of the metrics files
unzip_dir =  os.environ.get("UNZIP_DIR") # dir of the metrics files


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
   


def gunzip(file_path, output_path):
    try:
        file = tarfile.open(file_path)
        file.extractall(output_path)
        file.close()
    except Exception as ex:
        print("Error is occured while extract the file {} and the error is {}".format(file_path,ex))


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
