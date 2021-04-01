import React from 'react';
import { shallow } from 'enzyme';
import ReportsList from './ReportsList';

describe('ReportsList tests', () => {
   
  // ReportsList tests. These tests check against a ReportsList component snapshot 
  // that is generated with sample test data. 
  test('should render default DashboardTable component', () => {
    const testDate = new Date();
    const testTableData = 
    [{namespace: "openshift-monitoring", podUsageCpuCoreSeconds: 21.1, network: 12, memory: 0},
    {namespace: "hello-world", podUsageCpuCoreSeconds: 13.4, network: 5, memory: 0},
    {namespace: "myproject", podUsageCpuCoreSeconds: 22.4, network: 0, memory: 0},
    {namespace: "sample-project", podUsageCpuCoreSeconds: 33.5, network: 6, memory: 0},
    {namespace: "sample-project-1", podUsageCpuCoreSeconds: 16.1, network: 7, memory: 0},
    {namespace: "sample-project-2", podUsageCpuCoreSeconds: 17.4, network: 8, memory: 0},
    {namespace: "sample-project-3", podUsageCpuCoreSeconds: 15.5, network: 9, memory: 0}]
    const testColumnTitle = {
        namespace: 'Report Name',
        podUsageCpuCoreSeconds: 'Pod CPU Usage in Seconds',
        network: 'Network Usage in Megabits per Second',
        memory: 'Memory Usage in Gigabytes'
    }
    const view = shallow(<ReportsList key={'ReportsList'} startDate={testDate}
        tableData={testTableData} columnTitle={testColumnTitle}/>);
    expect(view).toMatchSnapshot();
  })

})