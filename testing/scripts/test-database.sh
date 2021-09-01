#!/bin/sh

DIE() {
	echo "ERROR: $*" >&2
	exit 1
}

[ "$DATABASE_NAME" ] || DIE "missing DATABASE_NAME"
[ "$DATABASE_USER" ] || DIE "missing DATABASE_USER"
[ "$DATABASE_PASSWORD" ] || DIE "missing DATABASE_PASSWORD"
[ "$DATABASE_HOST_NAME" ] || DIE "missing DATABASE_HOST_NAME"
[ "$PORT_NUMBER" ] || DIE "missing PORT_NUMBER"

psql -d "postgresql://$DATABASE_USER:$DATABASE_PASSWORD@$DATABASE_HOST_NAME:$PORT_NUMBER/$DATABASE_NAME" -Atc "SELECT 'database connected ' || now()::text;"