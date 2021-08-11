#!/bin/sh

DIE() {
	echo "ERROR: $*" >&2
	exit 1
}

 # this script usually won't be run at all if AWS backup is disabled; 
 # this check ensures it stops if it is run manually
[ "$USE_AWS" ] || DIE "AWS Backup Disabled"
[ "$S3_ENDPOINT" ] || DIE "missing S3_ENDPOINT"
[ "$AWS_SECRET_ACCESS_KEY" ] || DIE "missing AWS_SECRET_ACCESS_KEY"
[ "$AWS_ACCESS_KEY_ID" ] || DIE "missing AWS_ACCESS_KEY_ID"
[ "$BACKUP_SRC" ] || DIE "missing BACKUP_SRC"
[ "$BACKUP_DST" ] || DIE "missing BACKUP_DST"

mc -C /tmp/mc $MC_GLOBAL_FLAGS alias set \
	backup "$S3_ENDPOINT" "$AWS_ACCESS_KEY_ID" "$AWS_SECRET_ACCESS_KEY"
mc -C /tmp/mc $MC_GLOBAL_FLAGS mirror $MC_MIRROR_FLAGS "$BACKUP_SRC" "backup/$BACKUP_DST"
