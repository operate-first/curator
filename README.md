# **Curator**

## About
An infrastructure consumption showback project for OCP. The curator project retrieves infrastructure utilization as raw data using [koku-metrics-operator](https://github.com/project-koku/koku-metrics-operator).

You need administrator access to an OpenShift v.4.5+ cluster. 

The project is being incubated in the [Operate First](https://www.operate-first.cloud/) environment. To submit an issue or a feature request, please raise an issue at https://github.com/operate-first/curator/issues. 


### Backup a directory to an S3 bucket
This collection of manifests will deploy a Cron job that periodically runs a pod that backs up up a local (to the pod) directory
to an S3 bucket using the [MinIO Client][] (`mc`).

[minio client]: https://docs.min.io/docs/minio-client-complete-guide.html

### Generate Report
To generate a report manually, run the `generate_report()` PostgreSQL function on the database. The function takes a single argument specifying the time period over which to aggregate the collected data, which can be either *day*, *week*, or *month*. For instance, to generate a report for the current week, run `generate_report('week')`.

### Installation and Configuration
1. To install Curator, run `install.sh`. This will first prompt you to opt-in or opt-out of S3 back-up option and then prompt you to enter the configuration variables needed to run the project.

      a. At any time you can change the configuration by editing `Documentation/config/config.env` and `Documentation/credentials/credentials.env`
         If you change value for variable `HAS_S3_ACCESS` later, collected files will be either pushed or not depending on the value for variable.

   Optionally, you may set:

     - `MC_GLOBAL_FLAGS` -- flags passed to all invocations of the
       `mc` command
     - `MC_MIRROR_FLAGS` -- flags passed only to the `mc mirror`
       command

2. Deploy the application to OpenShift.

    - Run `oc apply -k .` to deploy this application into the
      namespace defined by the `namespace:` setting in
      `kustomization.yaml`.
	
    - If you have Kustomize installed seperately , run:

    ```
    kustomize build | oc apply -f-
    ```

    - To delete the application from OpenShift, run:

    ```
    kustomize build | oc delete -f-
    ```

3. Deploy the API to Openshift
    - Copy configuration file:
    ``` shell
    mkdir -p apis/config; cp Documentation/config/config.env apis/config/config.env
    ```
    - Install CRD
	
	This part was generated using [kubebuilder](https://github.com/kubernetes-sigs/kubebuilder), which requires go v1.16+.
	
        To use prebuilt image: 

    ```shell
    cd apis/report
    make install
    make deploy IMG=quay.io/operate-first/curator-crd
    cd ../..
    ```

    ​	If you would like to build CRD from scratch or you made change to the apis/report scource code:

    ``` shell
    cd apis/report
    make install
    make docker-build docker-push IMG=<some-registry>/<project-name>:tag
    make deploy IMG=<some-registry>/<project-name>:tag
    cd ../..
    ```
    - Create a example `Report` to define specification of report
        - reportingEnd: [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) Datetime. Create reports for the past N days until reportingEnd (includes reportingEnd).
        - reportPeriod: String, one of Day,Week,Month. Report period N = 1, 7, 30 days. 
        - namespace: String. Show report for namespace only. (Report metrics are grouped by namespace and accumulated by taking sum over the N days reportPeriod.)
    ``` shell 
    oc apply -f apis/report/config/samples/batch_v1_report.yaml
    ```
    - Deploy the HTTP API
    ``` shell
    kustomize build apis | oc apply -f-
    ```
    - Access `Report` data base on namespace and name of `Report` you just created. For example:
    ```shell
    oc port-forward $(oc get pods -l=app=curator-api -o name) 5000:5000
    curl -XGET "http://localhost:5000/report?reportName=report-sample&reportNamespace=report-system"
    ```

### Testing

Before deploying the application, you can run `verify_connection.sh` to test your S3 bucket and PostgreSQL database connectivity. 

To run database/S3 connectivity check: (OC cluster access required)
```shell
sh verify_connection.sh
```

To run test case with provided example test data: (Testing at local python environments. Some package required)
```shell
cd testing; python -m unittest curator-test.py
```


**WARNING** Make sure you don't add `credentials.env` to a Git
repository and accidentally expose your credentials.

[docker image]: https://hub.docker.com/r/minio/mc/
[s3cmd]: https://s3tools.org/s3cmd

### Planned development

+ Access for the cluster admin to view the system generated reports in the OCP console. 
+ Access for the cluster admin to run SQL queries on the infrastructure utilization data in the OCP console. 


### Development being considered
+ Access for the end-users to view the system generated reports of the projects they are running on OCP through the OCP console. 
+ Access for the end-users to run SQL queries on the infrastructure utilization data of the projects they are running on OCP through the OCP console. 
+ Utilization notification system. 
+ Synchronized data backup. 
+ CSV format sharable reports. 
+ Expand functionalities for multi-cluster OCP deployments.

### Communication
E-mail : curator@redhat.com Red Hat GChat : [Curator Project](https://join.slack.com/t/operatefirst/shared_invite/zt-o2gn4wn8-O39g7sthTAuPCvaCNRnLww)
