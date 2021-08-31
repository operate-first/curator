#!/bin/sh
mkdir -p testing/config
cp Documentation/config/config.env testing/config/config.env
mkdir -p testing/credentials
cp Documentation/credentials/credentials.env testing/credentials/credentials.env
kustomize build testing | oc apply -f- > /dev/null 2>&1

echo '=== S3 connection testing ==='
while [[ ! $(oc logs s3-connectivity-test -c mc 2> /dev/null) ]]; do echo "ContainerCreating ..."; sleep 2; done; oc logs s3-connectivity-test -c mc
echo '=== Postgres connection testing ==='
while [[ ! $(oc logs s3-connectivity-test -c postgres 2> /dev/null) ]]; do echo "ContainerCreating ..."; sleep 2; done; oc logs s3-connectivity-test -c postgres

kustomize build testing | oc delete -f- > /dev/null 2>&1