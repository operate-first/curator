
# Curator Reporting Metrics
### Purpose
The purpose of this document is to identify what specific metrics the Curator will need from Openshift Reporting Backend. Prior research of project Koku has been utilized to come up with these metrics.

### Project Koku Research
Project Koku utilizes a koku-metrics-operator to retrieve OCP usage data and upload it to the front end. Koku specifies a function ([Here](https://github.com/project-koku/koku-metrics-operator/blob/master/collector/collector.go#L125)) that queries prometheus and writes the result to report files. For each level of collection there is a CSV output report of the data queried (columns of the csvs generated are specified below with units).

*   Koku metrics are organized as
    1. Pods
        - Report_period_start - UTC
        - Report_period_end - UTC
        - Interval_start - UTC
        - Interval_end - UTC
        - Node -  string value of node
        - Namespace - string value of namespace
        - Pod - string value of pod
        - Pod_usage_cpu_core_seconds - total compute core seconds used by each pod
        - Pod_request_cpu_core_seconds - total compute core seconds needed by each pod
        - Pod_limit_cpu_core_seconds - total compute core seconds allocated by pod
        - Pod_usage_memory_byte_seconds - memory in bytes/second used by each pod
        - Pod_request_memory_byte_seconds- memory in bytes/second needed by each pod
        - Pod_limit_memory_byte_seconds
        - Node_capacity_cpu_cores
        - Node_capacity_cpu_core_seconds
        - Node_capacity_memory_bytes
        - Node_capacity_memory_byte_seconds
        - Resource_id
        - Pod_labels - string value of all labels pertaining to a pod
    2. Volume
        - Report_period_start
        - Report_period_end
        - Interval_start
        - Interval_end
        - Namespace
        - Pod
        - Persistentvolumeclaim
        - Persistentvolume
        - Storageclass
        - Persistentvolumeclaim_capacity_bytes
        - Persistentvolumeclaim_capacity_byte_seconds
        - Volume_request_storage_byte_seconds
        - Persistentvolumeclaim_usage_byte_seconds
        - Persistentvolume_labels
        - Persistentvolumeclaim_labels
    3. Node
        - Report_period_start - UTC
        - Report_period_end - UTC
        - Interval_start - UTC
        - Interval_end - UTC
        - Node -  string value of node
        - Node_labels - string value of all labels pertaining to node
    4. Namespace
        - Report_period_start - UTC
        - Report_period_end - UTC
        - Interval_start - UTC
        - Interval_end - UTC
        - Namespace -  string value of node
        - Namespace_labels - string value of all labels pertaining to node


### Curator

Curator backend utilizes the metering operator, which relies on Prometheus as the default datasource in order to collect in-cluster information. By querying the metering operator, we are able to aggregate a series of scheduled reports that display the necessary metrics for the end user. From Openshift Metering, there is currently the option of either retrieving data from the predefined report-queries that come with the metering operator installation or there is the option of custom queries.

For each level of metering/data collection, the following are the metrics made available from the standard report data source that correspond to metrics collected from Koku. However, there are also cluster level cpu, memory, volume metric collections that are available from the standard reports. More queries (custom and standard) can be added  based on user/team feedback on the reports generated.

* The following are standard reports available on the metering operator that correspond with the levels of data collection from Project Koku:

    1. Pods
        - pod-cpu-request                              
        - pod-cpu-request-raw                          
        - pod-cpu-usage                                
        - pod-cpu-usage-raw                            
        - pod-memory-request                           
        - pod-memory-request-raw                       
        - pod-memory-usage                             
        - pod-memory-usage-raw                         
    2. Volume
        - persistentvolumeclaim-capacity               
        - persistentvolumeclaim-capacity-raw           
        - persistentvolumeclaim-phase-raw              
        - persistentvolumeclaim-request                
        - persistentvolumeclaim-request-raw            
        - persistentvolumeclaim-usage                  
        - persistentvolumeclaim-usage-raw              
        - persistentvolumeclaim-usage-with-phase-raw   
    3. Node
        - node-cpu-allocatable                         
        - node-cpu-allocatable-raw                    
        - node-cpu-capacity                           
        - node-cpu-capacity-raw                        
        - node-cpu-utilization                        
        - node-memory-allocatable                      
        - node-memory-allocatable-raw                  
        - node-memory-capacity                         
        - node-memory-capacity-raw                     
        - node-memory-utilization**<code> </code></strong>
    4. Namespace
        - namespace-cpu-request                        
        - namespace-cpu-usage                          
        - namespace-cpu-utilization                    
        - namespace-memory-request                     
        - namespace-memory-usage                       
        - namespace-memory-utilization                 
        - namespace-persistentvolumeclaim-request      
        - namespace-persistentvolumeclaim-usage        


### Query outputs
This section describes the example output from queries that Curator backend will aggregate. One proposal is to retrieve the data directly from the Hive database utilizing the reporting API and output data as a JSON. Another proposal is to collect data from the queries and output them into a csv file.  Storage configurations/options for all collected data will need to be explored after the mvp so that user data is not lost even if the metering operator needs to be redeployed. The following is an example report output for namespace-cpu-request-daily (pod information organized by namespace).

| namespace | period_end | period_start | pod_request_cpu_core_seconds |
| --- | ----------- | ---- | ------------ |
| openshift-service-ca-operator | 2019-12-30 23:59:59 +0000 UTC | 2019-01-01 00:00:00 +0000 UTC | 134.872 |

### Curator Backend API structure
The following table defines potential curator backend endpoints with REST structure to handle data collected through the metering operator.

Currently implemented routes are utilizing namespace cpu usage data. Metrics
that will be added based on Koku research and the standard reports available on the metering operator are
- pod cpu/memory usage
- persistantvolume claim usage
- node memory usage/ cpu capacity
- namespace memory usage/ persistent volume claim usage

| Resource | Explanation | Request Method |
| --- | ----------- | ---- |
| /namespace-cpu-request/reports/standard?start=2020-12-04&frequency=day | Retrieves a standard report of CPU usage in seconds for each namespace every day from 2020-12-04 to current date | GET |
| /namespace-cpu-request/reports/custom?start=2020-12-04&frequency=week | Retrieves a custom report of CPU usage in seconds for each namespace for each week from week of 2020-12-04 to current week | GET |
| /namespace-cpu-request/reports/analytical?start=2020-12-04&frequency=month | Retrieves an analytical report of CPU usage in seconds for each namespace every day from month of 2020-12-04 to current month | GET |

In addition to showing, discrete values, Curator could contrast request and usage so users have a good idea of the management of their projects. The routes above have been implemented currently and the metrics have been included as future work.



### Curator Reports on the UI

The following visuals are based on what Curator would display on its frontend to the end user.
