#!/bin/bash          

# INSTALLATION SCRIPT
# This script prompts the user for configuration values,
# and sets the config.env file accordingly
# It also moves the correct cronjob file into the root

echo 'Welcome to Curator!'
echo 'Warning: this will overwrite existing configuration'

echo '== S3 Configuration =='
read -p '- Use S3 Storage? (y/n) ' use_s3_raw

if [ $use_s3_raw = "y" ] ;then
    use_s3=true
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

echo "USE_S3=${use_s3}
BACKUP_SRC=${backup_src}
UNZIP_DIR=${unzip_dir}
BACKUP_DST=${backup_dst}
DATABASE_NAME=${db_name}
DATABASE_USER=${db_user_name}
DATABASE_PASSWORD=${db_password}
HOST_NAME=${db_hostname}
PORT_NUMBER=${db_portnumber}" > ./Documentation/config/config.env

if [ $use_s3_raw = "y" ]
then
    echo "S3_ENDPOINT=${s3_endpoint}
BUCKET_NAME=${bucket_name}" >> ./Documentation/config/config.env
    cp ./Documentation/config/cron/cronjob-s3.yaml ./cronjob.yaml
else
    cp ./Documentation/config/cron/cronjob-nos3.yaml ./cronjob.yaml
fi

echo ''
echo 'Curator configuration complete!'
echo '-> Note: to update the configuration, edit Documentation/config/config.env'