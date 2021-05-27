# **Curator**

## About
An infrastructure consumption showback project for OCP. The curator project retrieves infrastructure utilization as raw data using [koku-metrics-operator](https://github.com/project-koku/koku-metrics-operator).

You need administrator access to an OpenShift v.4.5+ cluster. 

The project is being incubated in the [Operate First](https://www.operate-first.cloud/) environment. To submit an issue or a feature request, please raise an issue at https://github.com/operate-first/curator/issues. 

### Functionalities
+ Download raw data of OCP infrastructure utilization. (v0.1 - 05/26/2021)

### Planned development
+ Automation of storing infrastructure utilization data in a S3-compatible persistent volume. (v0.2 - 06/09/2021)
+ Generation of the system reports for daily, weekly and monthly infrastructure utilization. (v0.3 - 06/23/2021)
+ Pre-defined SQL query support for the infrastructure utilization data. (v0.4 - 07/07/2021)
+ Custom SQL query support for the infrastructure utilization data. (v0.4 - 07/07/2021)
+ Access for the cluster admin to view the system generated reports in the OCP console. (v0.5 - 07/21/2021)
+ Access for the cluster admin to run SQL queries on the infrastructure utilization data in the OCP console. (v0.5 - 07/21/2021)

### Development being considered
+ Access for the end-users to view the system generated reports of the projects they are running on OCP through the OCP console. (Late August 2021)
+ Access for the end-users to run SQL queries on the infrastructure utilization data of the projects they are running on OCP through the OCP console. (Late August 2021)
+ Utilization notification system. (September 2021)
+ Synchronized data backup. (September 2021)
+ CSV format sharable reports. (Late August 2021)
+ Expand functionalities for multi-cluster OCP deployments. (Late 2021)

### Generate reports
+ Update the configuration for the koku-metrics-operator using the [YAML file](https://github.com/operate-first/curator/blob/main/Documentation/config/kokumetric-config.yaml).
+ Download the report locally using the [rsync command](https://github.com/operate-first/curator/blob/main/Documentation/config/kokumetric-report.yaml). 

### Communication
E-mail : curator@redhat.com Red Hat GChat : [Curator Project](https://mail.google.com/chat/u/0/#chat/space/AAAAnkClSoU)

