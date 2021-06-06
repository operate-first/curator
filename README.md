# Backup a directory to an S3 bucket

This collection of manifests will deploy a Cron job that
periodically runs a pod that backs up up a local (to the pod) directory
to an S3 bucket using the [MinIO Client][] (`mc`).

[minio client]: https://docs.min.io/docs/minio-client-complete-guide.html

## Configuration

1. Copy `credentials-example.env` to `credentials.env`
   and update it with your bucket credentials. 

2. Update `config.env`. The following configuration variables are
   required:

     - `BACKUP_SRC` -- the path to the directory you want to back up
     - `BACKUP_DST` -- the bucket name and path for backup destination
     - `S3_ENDPOINT` -- your S3 API endpoint

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
