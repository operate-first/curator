import React from 'react';
import '@patternfly/react-core/dist/styles/base.css';
import { Table, TableHeader, TableBody, TableVariant, BodyCell } from '@patternfly/react-table';
import { Link } from 'react-router-dom';
import { dataObject } from './ReportsDataFilterForm';

type myProps = {
  columnTitle: object;
  tableData: Array<dataObject>;
  startDate: Date;
};

type myState = {
  columns: Array<object | string>;
  rows: Array<row>;
};

type row = {
  cells: cells;
};

type cells = Array<JSX.Element | number | string>;

/*
The table/list which displays metering report data for the Standard Report Type.
Currently displays columns for namespace, cpu usage, network usage, and memory usage.
*/
class ReportsList extends React.Component<myProps, myState> {
  constructor(myProps) {
    super(myProps);

    const rowData: Array<row> = [];
    myProps.tableData.forEach(dataRow => {
      rowData.push({
        cells: [
          <BodyCell key={`/projectlist/${dataRow['namespace']}`}>
            <Link to={`/projectlist/${dataRow['namespace']}`} key={`/projectlist/${dataRow['namespace']}`}>
              {dataRow['namespace']}
            </Link>
          </BodyCell>,
          dataRow['podUsageCpuCoreSeconds'],

        ]
      });
    })

    this.state = {
      columns: [
        myProps.columnTitle['namespace'],
        myProps.columnTitle['podUsageCpuCoreSeconds']
      ],
      rows: rowData
    };
  }

  shouldComponentUpdate(nextProps: myProps,nextState: myState){
    console.log(nextProps.tableData);
    console.log(JSON.stringify(nextProps)!== JSON.stringify(this.props))
    return JSON.stringify(nextProps)!== JSON.stringify(this.props)
  }

  UNSAFE_componentWillReceiveProps(nextProps: myProps) {
      const rowData: Array<row> = [];

      nextProps.tableData.forEach(dataRow => {
        rowData.push({
          cells: [
            <BodyCell key={`/projectlist/${dataRow['namespace']}`}>
              <Link to={`/projectlist/${dataRow['namespace']}`} key={`/projectlist/${dataRow['namespace']}`}>
              {dataRow['namespace']}
              </Link>
            </BodyCell>,
            dataRow['podUsageCpuCoreSeconds']
          ]
        });
      });
      this.setState({ ...this.state, rows: rowData });
  }

  render() {
    return (
      <div>
        <Table
          key={'dataTable'}
          aria-label="Compact Table"
          variant={TableVariant.compact}
          cells={this.state.columns}
          rows={this.state.rows}
          caption="List of reports"
        >
          <TableHeader />
          <TableBody />
        </Table>
      </div>
    );
  }
}
export default ReportsList;
