import React from 'react';
import { Table, TableHeader, TableBody, TableVariant, BodyCell } from '@patternfly/react-table';
import { Link } from 'react-router-dom';
import { dataObject } from '@app/project_page/demoProjectfilterform';

type DashboardTableProps = {
  columnTitle: object;
  tableData: Array<dataObject>;
};

type DashboardTableState = {
  columns: Array<object | string>;
  rows: Array<row>;
};

type row = {
  cells: cells;
};

type cells = Array<JSX.Element | number>;

class DashboardTable extends React.Component<DashboardTableProps, DashboardTableState> {
  constructor(myProps: DashboardTableProps) {
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
          // dataRow['namespace'],
          dataRow['activationTime']
          // dataRow['node'],
          // dataRow['periodStart'].toISOString(),
          // dataRow['periodEnd'].toISOString(),
          // dataRow['pod'],
          // dataRow['podUsageCpuCoreSeconds']
        ]
      });
    })

    this.state = {
      columns: [
        myProps.columnTitle['namespace'],
        myProps.columnTitle['activationTime']
        // myProps.columnTitle['node'],
        // myProps.columnTitle['periodStart'],
        // myProps.columnTitle['periodEnd'],
        // myProps.columnTitle['pod'],
        // myProps.columnTitle['podUsageCpuCoreSeconds']
      ],
      rows: rowData
    };
  }


  shouldComponentUpdate(nextProps: DashboardTableProps, nextState: DashboardTableState) {
    return JSON.stringify(nextProps.tableData) !== JSON.stringify(this.props.tableData)
  }

  UNSAFE_componentWillReceiveProps(nextProps: DashboardTableProps) {
    const rowData: Array<row> = [];

    nextProps.tableData.forEach(dataRow => {
      rowData.push({
        cells: [
          <BodyCell key={`/projectlist/${dataRow['namespace']}`}>
            <Link to={`/projectlist/${dataRow['namespace']}`} key={`/projectlist/${dataRow['namespace']}`}>
              {dataRow['namespace']}
            </Link>
          </BodyCell>,
          dataRow['activationTime']
          // dataRow['periodStart'].toISOString(),
          // dataRow['periodEnd'].toISOString(),
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
          caption="List of projects"
        >
          {/* rowWrapper={} */}
          <TableHeader />
          <TableBody />
        </Table>
      </div>
    );
  }
}
export { DashboardTable };
