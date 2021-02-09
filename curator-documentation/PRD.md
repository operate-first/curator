#  Infrastructure Metering in Open Cloud
### Version 1.0 18/01/2021

## Background
The Red Hat Research team is on a mission to support and develop Open Clouds to help researchers and academicians to run their computations in a place where the development as well as the operations are open and are supported by Red Hat products. As part of this, it is essential that resource owners, project leaders, and individual researchers can easily track resource usage over time. There is a need for a system that encapsulates the metering and monitoring facilities provided by tools like Prometheus and the Metering Operator for OpenShift and Telemetry for OpenStack. The new metering system aggregates and presents the resource utilization totals in the form of daily, weekly, and monthly resource reports, as well as it will provide an easy-to-use web interface for exploring custom reports.  This metering tool will make the usage data easy to view and open to all users, making it possible for users and administrators to collaborate on data center resource management and efficiency. 

## Phase 1 - OpenShift Metering in MOC
### Goals 
A metering system should be built for all the resource consumption made by the OpenShift instances in Mass Open Cloud. Any user of the OpenShift instance in MOC should be able to login to the metering system using the same credentials used to login to MOC and get to know the resource consumption <metrics needs to be defined> tied to the username in one or more  OpenShift clusters.   

### Specifications
The metering system should have the following capabilities:
 - Authentication and Identification (CILogon)
 - Mapping of the Identity and resource consumption (To be built)
- User Interface (To be built)
- Metric Collection (Metering Operator) 
- Persistent Storage (S3 compatible - <Hive?>)
- Data Analysis tool (Prometheus)

### User Stories
 - As an administrator of the Open Cloud, I should be able to view the resource consumption of the entire OpenShift instance at any given time by logging in to the system.
 - As an administrator of the Open Cloud, I should be able to view the resource consumption of the entire OpenShift instance for all the projects between any particular time frame. 
 - As an administrator of the Open Cloud, I should be able to view the automatically prepared daily, weekly and monthly resource reports of the entire OpenShift instance and for all projects in the instance.
 - As a user of the Open Cloud, I should be able to view the resource consumption reports for daily, weekly and monthly reports of the resource consumption in the OpenShift  instance for all the projects that are tied to my account.
 - As an administrator of the Open Cloud, I should be able to do any metering system operation that a user can do. 

### Milestones and Timelines
 - Gather user requirements from MOC users and administrators. 
 - Define project/namespace.
 - Design UI mockups.
 - Develop UI.
 - Install Metering Operator.
 - Build persistent storage.
 - Integrate metering platform with the OCP system. 
 - Deploy the metering system on a Single Node OCP.
 - Invite users (~20) to test the system on a Single Node OCP.
 - Identify bugs and collect feedback.
 - Deploy the application on production OCP in MOC. 
 - Track metering usage, proactively solicit more input from users, and maintain metering software and system until handoff to production MOC DevOps team.


