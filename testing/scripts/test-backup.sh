#!/bin/sh

DIE() {
	echo "ERROR: $*" >&2
	exit 1
}

[ "$S3_ENDPOINT" ] || DIE "missing S3_ENDPOINT"
[ "$AWS_SECRET_ACCESS_KEY" ] || DIE "missing AWS_SECRET_ACCESS_KEY"
[ "$AWS_ACCESS_KEY_ID" ] || DIE "missing AWS_ACCESS_KEY_ID"
[ "$BACKUP_SRC" ] || DIE "missing BACKUP_SRC"
[ "$BACKUP_DST" ] || DIE "missing BACKUP_DST"
[ "$BUCKET_NAME" ] || DIE "missing BUCKET_NAME"

mc -C /tmp/mc $MC_GLOBAL_FLAGS alias set \
	backup "$S3_ENDPOINT" "$AWS_ACCESS_KEY_ID" "$AWS_SECRET_ACCESS_KEY"

mc -C /tmp/mc $MC_GLOBAL_FLAGS find "backup/$BACKUP_DST"
mc -C /tmp/mc $MC_GLOBAL_FLAGS find "backup/$BUCKET_NAME"
#[ -d "$BACKUP_SRC" ] || DIE "Directory $BACKUP_SRC does not exists."

mkdir upload
mkdir download
dd if=/dev/urandom of=./upload/rand bs=1024 count=1 > /dev/null 2>&1
mc -C /tmp/mc $MC_GLOBAL_FLAGS mirror $MC_MIRROR_FLAGS ./upload "backup/$BACKUP_DST"
mc -C /tmp/mc $MC_GLOBAL_FLAGS cp $MC_MIRROR_FLAGS "backup/$BACKUP_DST/rand" ./download/rand
[ -f "./download/rand" ] || DIE "fail to upload/download to s3"
#mc -C /tmp/mc $MC_GLOBAL_FLAGS rm $MC_MIRROR_FLAGS "backup/$BACKUP_DST/rand"

