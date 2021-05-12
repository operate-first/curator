
# **Open Cloud Curator (OCC)**

# Project Requirements Document (PRD)
##### Document revision v0.1
##### May 12, 2021

## **Introduction**
### Background
The Red Hat Research team is on a mission to support and develop Open Clouds to help researchers and academicians to run their computations in a place where the development as well as the operations are open and are supported by Red Hat products. As part of this, it is essential that the infrastructure owners, project leaders, and individual researchers can easily track infrastructure usage over time. Even though we are now able to provide the computation infrastructure to researchers in Open Clouds such as Mass Open Cloud, at the moment we don’t have a system that can track the infrastructure utilization on-demand.

### Purpose
There is a need for a system that encapsulates the metering and monitoring facilities provided by tools like Prometheus and the Metering Operator for OpenShift and Telemetry for OpenStack. There is a requirement for a new metering system that aggregates and presents the resource utilization in the form of daily, weekly, and monthly usage reports to the Open Cloud administrators as well as the end users. It should also provide an easy-to-use web interface for exploring custom reports through which the user would be able to identify infrastructure utilization between any time period.  This metering tool will make the usage data easy to view and open to all users, making it possible for users and administrators to collaborate on data center resource management and efficiency. The infrastructure utilization data collected can also be used to analyze the dependencies between the cloud services.

As part of this plan, we are designing a metering system for the resource consumption in the Mass Open Cloud. As part of the initial stage, it will be recording all the resource consumption made by applications running on the OpenShift instances in Mass Open Cloud. Any user of the OpenShift instance in MOC will be able to login to the metering system using the same credentials used to login to MOC and get to know the resource consumption by their respective projects in the OpenShift cluster of MOC.

### **System users**
- #### Cloud administrator
These users will also be responsible for maintaining the OCC service. These users will be interested in knowing the infrastructure utilization across the cloud.
- #### Research leads
Users who create projects in the cloud for their research program. Research leads will be riveted in knowing how much infrastructure was utilized by projects owned by them between any time period.
- #### End users
Users who are part of a research group and who have a limited quota of resources. These users will be interested in knowing more about their quota utilization.
- #### Analysts
People who are interested in mapping relationships between services and infrastructure using the data that has been collected.  Typically, analysts look for resource usage trends to help with future resource planning.  An analyst could be planning for the entire open cloud, or for specific projects.

### **Document audience**
This document is intended for people who are interested in:
1. Metering in Open Cloud to create user accountability.
2. Monitoring in Open Cloud to improve service reliability.
3. Data analysis in Open Cloud to identify services dependencies.

### **Field study and reference material**
#### Metering Tools
As part of the field study, we explored the metering options available for OpenShift infrastructure utilization in the market. From our research, we identified three main options through which an administrator of an OCP cluster can get utilization metrics. They are:

- Project Koku
Koku's goal is to provide an open source solution for cost management of cloud and hybrid cloud environments. This solution is offered via a web interface that exposes resource consumption and cost data in easily digestible and filterable views. The project also aims to provide insight into this data and ultimately provide suggested optimizations for reducing cost and eliminating unnecessary resource usage.
- OpenShift cost tool
OpenShift cost management tool runs across hybrid environments. It captures metrics and metadata from OpenShift operator metering, AWS and Azure. It has a graphical interface and APIs. It provides the option for cost modeling as well as business mapping.
- OpenShift metering operator
OpenShift metering operator has weighted reporting for the infrastructure utilization. It provides raw data based on Prometheus metrics. Optionally, it can be integrated to Amazon EC2. It can be plugged into BI tools and provides SQL - like query language.

All the tools and services we have listed above caters to the cluster administrators. Also, OpenShift cost management tool and Project Koku are built as cost management tools and don’t provide raw data which can be used to showback the infrastructure utilization. However, our goal is to provide even the end users of the cloud the option to view their utilization metrics retrospectively. Hence we have decided to use the Koku-metrics operator to get the metrics from OpenShift and store them in persistent storage. We will be querying the persistent storage for the reports that will be generated. 

### **Feature requirements**
#### Project initiative
The metering system will have the following capabilities:
- Authentication and authorization
- Mapping of the Identity and resource consumption
- Recurring reports
- User Interface
- Metric Collection
- Persistent Storage

#### Feature category
Project - A project is a Kubernetes namespace with additional annotations, and is the central vehicle by which access to resources for regular users is managed.
Duration - A duration is a time period selected by the user as part of a query for a report generation.
Query - A query is a condition that has been put forward by the user to get the metrics from the infrastructure only for the duration mentioned.
Saved Query - Frequently used Queries can be saved for user convenience.
Report - A set of metrics will be automatically collected for all the projects in the open cloud infrastructure periodically (Daily, Weekly, Monthly).
Parameters - Parameters are the set of fields such as CPU and volume for which we can create a query about infrastructure utilization.
Reports - Reports is an option through which the users will be able to see the monthly, weekly and daily reports that are system generated.
Custom reports - Users will have the ability to view resource utilization between any time period with the help of custom reports.
Shareable report - Daily, weekly, monthly as well as the custom reports will also be available in the CSV format that can be shared with others.
Account - The account option will provide the option to view the associated project(s) tied to the user who has logged in.

### **User stories**
- As an administrator of the Open Cloud, I should be able to view the resource consumption of the entire OpenShift instance for any past time by logging in to the metering system.
- As an administrator of the Open Cloud, I should be able to view the resource consumption of the entire OpenShift instance for all the projects between any particular time frame.
- As an administrator of the Open Cloud, I should be able to view the automatically prepared daily, weekly and monthly resource reports of the entire OpenShift instance and for all projects in the instance.
- As a user of the Open Cloud, I should be able to view the resource consumption reports for daily, weekly and monthly reports in the OpenShift  instance for all the projects that are tied to my account.
- As a user of the Open Cloud, I should be able to view the resource consumption reports for any particular time frame in the OpenShift instance for all the projects that are tied to my account.
- As an administrator of the Open Cloud, I should be able to do any metering system operation that a user can do.

### **MoSCoW priorities**
#### Must have (P0)
- Authentication and authorization of users
- Administrator privileges to view the cloud metrics
- Resource Mapping
- Users privileges to view the project metrics
- User interface
- Recurring daily, weekly and monthly usage reports
- Persistent storage

#### Should have (P1)
- User specified time reports
- CSV format sharable reports
- Persistent storage backup
- Usage alerts

#### Could have (P2)
- OpenShift service monitoring
- Metric data analysis
- A combined metering system for OpenStack and OpenShift

#### Will not have
- Usage prediction
- Billing system

### **Milestones**
- Gather user requirements from MOC users and administrators.
- Define project/namespace.
- Design UI mockups.
- Develop UI.
- Install data gatherer using Koku Metrics operator.
- Build persistent storage.
- Build authentication and mapping of users to resources.
- Integrate metering platform with the OCP system.
- Deploy the metering system on OCP.
- Invite users (~20) to test the system on an OCP instance for a month.
- Deploy the application on production OCP in MOC.
- Track metering usage, proactively solicit more input from users, and maintain metering software and system until handoff to production MOC DevOps team.

### **Out of scope or later phases**
- OpenShift usage analysis
After the metering system starts to capture the resource utilization in a persistent storage, we can make the collected data available for interested groups such as the Telemetry Working Group provided the data can be shared with non-users of the infrastructure. The data can shed light on the interdependencies of the services as well as the user behavior.
- Integration of OpenStack and OpenShift metering
The final grand plan is to have one metering system which captures all the resources utilization across services such as OpenStack and OpenShift in one place for any specific user/research group. This will be equivalent to the billing system of public cloud providers such as AWS, Azure, and GCP.

