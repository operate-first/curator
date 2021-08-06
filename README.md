# **Curator**

## Release Information
Version 0.4 07/30/2021
+ Dowload raw data of OCP infrastructure utilization.
+ Automation of storing infrastructure utilization data in an S3-compatible persistent volume.
+ Unzipped metrics are being stored in an S3-compatible volume.
+ Pre-defined SQL query support for the infrastructure utilization data. 
+ Custom SQL query support for the infrastructure utilization data. 

## About
An infrastructure consumption showback project for OCP. The curator project retrieves infrastructure utilization as raw data using [koku-metrics-operator](https://github.com/project-koku/koku-metrics-operator).

You need administrator access to an OpenShift v.4.5+ cluster. 

The project is being incubated in the [Operate First](https://www.operate-first.cloud/) environment. To submit an issue or a feature request, please raise an issue at https://github.com/operate-first/curator/issues. 

### Functionalities
+ Download raw data of OCP infrastructure utilization. (v0.1 - 05/26/2021)
+ Automation of storing infrastructure utilization data in an S3-compatible persistent volume. (v0.2 - 06/09/2021)
+ Pre-defined SQL query support for the infrastructure utilization data. (v0.4 - 07/30/2021)
+ Custom SQL query support for the infrastructure utilization data. (v0.4 - 07/30/2021)


### Backup a directory to an S3 bucket
This collection of manifests will deploy a Cron job that periodically runs a pod that backs up up a local (to the pod) directory
to an S3 bucket using the [MinIO Client][] (`mc`).

[minio client]: https://docs.min.io/docs/minio-client-complete-guide.html

### Generate Report
To generate a report manually, run the `generate_report()` PostgreSQL function on the database. The function takes a single argument specifying the time period over which to aggregate the collected data, which can be either *day*, *week*, or *month*. For instance, to generate a report for the current week, run `generate_report('week')`.

### Configuration
1. Copy `credentials-example.env` to `credentials.env`
   and update it with your bucket credentials. 
   
   We will pull all environment variable into a secret generator which results in secrets. 
   That secret is being deployed and imported into OpenShift.

2. Update `config.env`. The following configuration variables are
   required:

     - `BACKUP_SRC` -- the path to the directory you want to back up
     - `BACKUP_DST` -- the bucket name and path for backup destination
     - `S3_ENDPOINT` -- your S3 API endpoint
     - `BUCKET_NAME` -- the bucket name for unzipped files

    Also provide information for all database related variable in `config.env` listed below.

       `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `HOST_NAME`, `PORT_NUMBER`
  
   Optionally, you may set:

     - `MC_GLOBAL_FLAGS` -- flags passed to all invocations of the
       `mc` command
     - `MC_MIRROR_FLAGS` -- flags passed only to the `mc mirror`
       command

3. Deploy the application to OpenShift.

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

**WARNING** Make sure you don't add `credentials.env` to a Git
repository and accidentally expose your credentials.

[docker image]: https://hub.docker.com/r/minio/mc/
[s3cmd]: https://s3tools.org/s3cmd

### Planned development

+ Access for the cluster admin to view the system generated reports in the OCP console. 
+ Access for the cluster admin to run SQL queries on the infrastructure utilization data in the OCP console. 


### Development being considered
+ Access for the end-users to view the system generated reports of the projects they are running on OCP through the OCP console. (Late August 2021)
+ Access for the end-users to run SQL queries on the infrastructure utilization data of the projects they are running on OCP through the OCP console. (Late August 2021)
+ Utilization notification system. 
+ Synchronized data backup. 
+ CSV format sharable reports. 
+ Expand functionalities for multi-cluster OCP deployments.

### Communication
E-mail : curator@redhat.com Red Hat GChat : [Curator Project](https://join.slack.com/t/operatefirst/shared_invite/zt-o2gn4wn8-O39g7sthTAuPCvaCNRnLww)
