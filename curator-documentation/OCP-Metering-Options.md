# OCP Metering Options


# Purpose

The purpose of this document is to explore OCP Metering projects/options to gain potential insights that help with identifying Curator project requirements. Additionally this document highlights the unique use cases that Curator provides in comparison with other OCP Metering Options


# Similar Metering Options



1. Red Hat SaaS offering for cost management on Openshift
    *   Available in OpenShift 4.3+
    *   Names and Tags- There is a guide to point out what particular tags might need to be included in the metadata and configurations. Once the single node cluster is up and running, this might come in handy for the deployment of our project onto the single node.
    *   They look quite in depth to the ownership and usage as well as governance for resources on the cloud (Not sure if this fits with our use case since this tool is particularly for students and researchers and they will be admins)


*   What is their use case?
    *   OpenShift Visibility- multiple OCP clusters on AWS with a consolidated dashboard
    *   OpenShift Infrastructure Costs- Multiple OCP structures on AWS
    *   OpenShift cost per project- If you have several projects in different OCP clusters

2. Red Hat and Koku- Open source project looking particularly at cost management on the cloud
*   Koku documentation to adding an OCP source
    1. Running OCP version 3.11 or newer.
    2. I[nstall Operator Metering](https://github.com/operator-framework/operator-metering/blob/master/Documentation/install-metering.md) on your OCP cluster.
    3. E[xpose a route](https://github.com/operator-framework/operator-metering/blob/master/Documentation/configuring-reporting-operator.md#openshift-route) for the reporting operator.
    4. Install and configure the [Red Hat Insights Client](https://access.redhat.com/products/red-hat-insights/#getstarted) on a system with network access to your OCP cluster.
    5. Install [Ansible](https://docs.ansible.com/ansible/2.7/installation_guide/intro_installation.html) and the [EPEL repository](https://fedoraproject.org/wiki/EPEL#Quickstart) on the system where the Red Hat Insight Client is installed.
    6. I[nstall the OCP command line, oc](https://docs.openshift.com/container-platform/3.3/cli_reference/get_started_cli.html#cli-linux), on the system where the Red Hat Insights Client is installed.
    7. They have an Ansible playbook called OCP Usage Collector that needs to be setup as well
    8. OCP usage collector retrieves the data from Metering Operator endpoint (similar to our back end)
*   Documentation: [https://koku.readthedocs.io/en/latest/sources.html#dependencies](https://koku.readthedocs.io/en/latest/sources.html#dependencies)
*   Github:
    9. [https://github.com/project-koku/](https://github.com/project-koku/)


3.  Tectonic- This is a container as a service tool that manages containers and deploys application
*   Tectonic Chargeback- aggregates Prometheus data and generates reports based on the collected usage information
*   Only available in admin console on OpenShift (cannot find a lot of information on this
4. ACM with prometheus


# Koku UI


**For OCP they have 4 different api calls on the UI:**


```
[ReportType.cost]: 'reports/openshift/costs/',
 [ReportType.cpu]: 'reports/openshift/compute/',
[ReportType.memory]: 'reports/openshift/memory/',
[ReportType.volume]: 'reports/openshift/volumes/'
```


**From the backend code, you can see 4 different types of queries:**



*   Node Queries
    *   `Node-allocatable-cpu-core-seconds`
    *   `Node-allocatable-memory-byte-seconds-.`
    *   `Node-capacity-cpu-core-seconds`
    *   `Node-capacity-memory-byte-seconds`
*   Volume Queries
    *   `Persistentvolumeclaim-request-byte-seconds`
    *   `Persistentvolumeclaim-capacity-byte-seconds`
    *   `Persistentvolumeclaim-usage-byte-seconds`
*   Pod Queries
    *   `Pod-limit-cpu-core-seconds`
    *   `Pod-limit-memory-byte-seconds`
    *   `Pod-request-cpu-core-seconds`
    *   `Pod-request-memory-byte-seconds`
    *   `Pod-usage-cpu-core-seconds`
    *   `pod-usage-memory-byte-seconds`


# **Accessing OCP metrics through Koku backend:**



*   Golang codebase
*   They utilize a thanos querier command to implement a Prometheus HTTP client to query the data.
*   Link to exact queries utilized in the backend: [https://github.com/project-koku/koku-metrics-operator/blob/master/collector/queries.go](https://github.com/project-koku/koku-metrics-operator/blob/master/collector/queries.go)
*   This is then loaded into resulting csvs (csv definitions are provided in the following link):
    *   [https://github.com/project-koku/koku-metrics-operator/blob/master/collector/types.go](https://github.com/project-koku/koku-metrics-operator/blob/master/collector/types.go)
*   Example of expected reports produced:
    *   [https://github.com/project-koku/koku-metrics-operator/tree/master/collector/test_files/expected_reports](https://github.com/project-koku/koku-metrics-operator/tree/master/collector/test_files/expected_reports)


# Curator Use Case

This is particularly a metiring system built for instances in the MOC. The end users for Curator are researchers and academicians who are looking for monitoring and metering capabilities for their project. Metrics as of now are defined by resource usage by projects/namespaces as opposed to being translated into any other (financial) costs.
