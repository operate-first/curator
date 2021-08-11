#!/bin/bash          

# INSTALLATION SCRIPT

echo 'Welcome to Curator!'
echo 'Warning: this will overwrite existing configuration'

echo '== AWS Configuration =='
read -p '- Use AWS Store? (y/n) ' use_aws_raw

if [ $use_aws_raw = "y" ] ;then
    use_aws=true
    read -p '- S3 Endpoint: ' s3_endpoint
    read -p '- S3 Bucket Name: ' bucket_name
fi

echo '== Koku Metrics Configuration =='
read -p '- Koku Metrics Backup Source Path: ' backup_src
read -p '- Koku Metrics Unzip Directory: ' unzip_dir
read -p '- Koku Metrics Backup Destination Path: ' backup_dest

echo '== Database Configuration =='
read -p '- Database Name: ' db_name
read -p '- Database User: ' db_user_name
read -p '- Database Password: ' db_password
read -p '- Database Host: ' db_hostname
read -p '- Database Port: ' db_portnumber

echo "USE_AWS=${use_aws}
BACKUP_SRC=${backup_src}
UNZIP_DIR=${unzip_dir}
BUCKET_NAME=${bucket_name}
BACKUP_DST=${backup_dst}
S3_ENDPOINT=${s3_endpoint}
DATABASE_NAME=${db_name}
DATABASE_USER=${db_user_name}
DATABASE_PASSWORD=${db_password}
HOST_NAME=${db_hostname}
PORT_NUMBER=${db_portnumber}
" > ./Documentation/config/config.env

if [ $use_aws_raw = "y" ]
then
  cp ./Documentation/config/cron/cronjob-aws.yaml ./cronjob.yaml
else
  cp ./Documentation/config/cron/cronjob-noaws.yaml ./cronjob.yaml
fi

echo ''
echo 'Curator configuration complete!'