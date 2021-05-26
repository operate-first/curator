import React from 'react';
import { shallow } from 'enzyme';
import { DashboardTable } from './DashboardTable';

describe('Dashboard tests', () => {
   
  // DashboardTable tests
  test('should render default DashboardTable component', () => {
    const testTableData = [{namespace: "openshift-monitoring", activationTime: 2},
    {namespace: "hello-world", activationTime: 1},
    {namespace: "myproject", activationTime: 2},
    {namespace: "sample-project", activationTime: 3},
    {namespace: "sample-project-1", activationTime: 1},
    {namespace: "sample-project-2", activationTime: 1},
    {namespace: "sample-project-3", activationTime: 1}]
    const testColumnTitle = {namespace: "Namespace", activationTime: "Project Active period"}
    const view = shallow(<DashboardTable tableData={testTableData} columnTitle={testColumnTitle}/>);
    expect(view).toMatchSnapshot();
  })

})