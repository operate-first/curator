#!/bin/bash          

# INSTALLATION SCRIPT
# This script prompts the user for configuration values,
# and sets the config.env file accordingly
# It also moves the correct cronjob file into the root

echo 'Welcome to Curator!'
echo 'Warning: this will overwrite existing configuration at \nDocumentation/config/config.env and Documentation/credentials/credentials_example.env'

echo '== S3 Configuration =='
HAS_S3_ACCESS=false
while true; do
    read -p "Do you wish to use S3 Storage? [y/n] ?" yn
    case ${yn} in
        [Yy]* ) HAS_S3_ACCESS=true; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

if [[ "$HAS_S3_ACCESS" = true ]] ;then
    read -rp '- S3 Endpoint: ' s3_endpoint
    read -rp '- S3 Host Name: ' s3_host_name
    read -rp '- S3 Bucket Name: ' bucket_name
    read -rp '- S3 AWS ACCESS KEY ID: ' aws_access_key_id
    read -rp '- S3 AWS SECRET ACCESS KEY: ' aws_secret_access_key
fi

echo '== Koku Metrics Configuration =='
read -rp '- Koku Metrics Backup Source Path: ' backup_src
read -rp '- Koku Metrics Unzip Directory: ' unzip_dir
read -rp '- Koku Metrics Backup Destination Path: ' backup_dest

echo '== Database Configuration =='
read -rp '- Database Name: ' db_name
read -rp '- Database User: ' db_user_name
read -rp '- Database Password: ' db_password
read -rp '- Database Host: ' db_hostname
read -rp '- Database Port: ' db_portnumber

echo "HAS_S3_ACCESS=${HAS_S3_ACCESS}
BACKUP_SRC=${backup_src}
UNZIP_DIR=${unzip_dir}
BACKUP_DST=${backup_dest}
DATABASE_NAME=${db_name}
DATABASE_USER=${db_user_name}
DATABASE_PASSWORD=${db_password}
DATABASE_HOST_NAME=${db_hostname}
PORT_NUMBER=${db_portnumber}" > ./Documentation/config/config.env

if [[ "$HAS_S3_ACCESS" = true ]]
then
    echo "S3_ENDPOINT=${s3_endpoint}
BUCKET_NAME=${bucket_name}
S3_HOST_NAME=${s3_host_name}" >> ./Documentation/config/config.env;
    echo "AWS_ACCESS_KEY_ID=${aws_access_key_id}
AWS_SECRET_ACCESS_KEY=${aws_secret_access_key}" > ./Documentation/credentials/credentials_example.env;
fi

echo ''
echo 'Curator configuration complete!'
echo '-> Note: to update the configuration, edit Documentation/config/config.env and Documentation/credentials/credentials_example.env'