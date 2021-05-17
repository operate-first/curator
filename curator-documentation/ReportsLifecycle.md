# Report Lifecycle

### Purpose

The purpose of this document is to understand the report structure of reports being generated, define metrics that will be displayed, and define the lifecycle of reports for a user.

#### Lifecycle of reports
For the sake of efficiency and maintenance, a hot and cold storage system will be used. The hot storage will hold data for 30 days prior. If a user requires clarification of resource usage prior to that, the cold storage would need to be accessed. This would be an exported version of the database (stored in S3 for example). There should be a routine daily check automated that removes data that would need to be archived.

### Data collection, processing, storage

There are two ways to retrieve data from koku-metrics-operator into Curator database.

1. Extract Transform Load - Retrieve raw data from koku as csv, transform it before reaching the database (process the data), then load it to database. The effort here is in the beginning so you are storing the clean data.

2. Extract Load Transform - Retrieve raw data from koku as csv, load raw into database and then transform it in place. With this option you can either have a copy of the raw as well as the processed metric or you can transform the raw in place without extra memory.

![](DatabaseDiagram.png)
*Figure 1: Curator database with data collection through koku-metrics-operator.*


Diagram was built in Mermaid Live Editor with the following markdown.

```
erDiagram
    User ||..|{ OCPCluster : has
    OCPCluster ||..|{ Namespace : has

    Namespace ||..|{ PodMetrics : has
    Namespace ||..|{ VolumeMetrics : has
    OCPCluster ||..|{ NodeMetrics : has

    User ||..|{ Export : has
    Export ||..|| Report : has


    User {
        string id
        string username
        string encrypted_password
        string location
    }

    OCPCluster {
        string userId
        string ocpToken
        string ipAddress
    }

    Namespace {
        string id
        string namespaceLabel
    }

    PodMetrics {
        string id
        string namespaceId
        string podLabel
        datetime periodStart
        datetime periodEnd
        double podUsageCpu
        double podRequestCpu
        double podLimitCpu
        double podUsageMemory
        double podRequestMemory
        double podLimitMemory
    }

    VolumeMetrics {
        string podId
        string namespaceId
        string volumeLabel
        datetime periodStart
        datetime periodEnd
        double pvc
        double pvcCapacityByteSeconds
        double pvcRequest
        double pvcUsage
    }

    NodeMetrics {
        string id
        string node_labels
        datetime periodStart
        datetime periodEnd
    }

    Export {
        string userId
        datetime timeOfExport
        date startDate
        date endDate
        ENUM reportFrequency
        string downloadLink
    }
```
