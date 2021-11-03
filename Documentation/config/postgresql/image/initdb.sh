#!/bin/bash -e

echo "Creating dblink extension"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE SCHEMA dblink;
    CREATE EXTENSION dblink SCHEMA dblink;
EOSQL

echo "Creating jobmon extension"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE SCHEMA jobmon;
    CREATE EXTENSION pg_jobmon SCHEMA jobmon;
    INSERT INTO jobmon.dblink_mapping_jobmon (username, pwd) VALUES ('$POSTGRES_USER', '$POSTGRES_PASSWORD');
EOSQL

echo "Creating partman extension"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE SCHEMA partman;
    CREATE EXTENSION pg_partman SCHEMA partman;
EOSQL

echo "Adding jobmon permissions"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    GRANT USAGE ON SCHEMA jobmon TO $POSTGRES_USER;
    GRANT USAGE ON SCHEMA dblink TO $POSTGRES_USER;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA jobmon TO $POSTGRES_USER;
    GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA jobmon TO $POSTGRES_USER;
    GRANT ALL ON ALL SEQUENCES IN SCHEMA jobmon TO $POSTGRES_USER;
EOSQL

echo "ADDING pg_partman_bgw TO postgresql.conf"
echo "shared_preload_libraries = 'pg_partman_bgw'" >> $PGDATA/postgresql.conf
echo "pg_partman_bgw.interval = 3600" >> $PGDATA/postgresql.conf
echo "pg_partman_bgw.role = '$POSTGRES_USER'" >> $PGDATA/postgresql.conf
echo "pg_partman_bgw.dbname = '$POSTGRES_DB'" >> $PGDATA/postgresql.conf
