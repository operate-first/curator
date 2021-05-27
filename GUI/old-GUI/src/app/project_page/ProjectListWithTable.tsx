import React from 'react';
import axios from 'axios';
import { DashboardTable } from '@app/DashboardTable/DashboardTable';
import { Link } from 'react-router-dom';
import SearchToolBar from '@app/SearchToolbar/SearchToolBar';

type myProps = {
  startDate: Date;
  endDate: Date;
  renderCount: number;
  changingDate: boolean;
};
type myState = {
  isLoaded: boolean;
  clusterData: Array<dataObject>;
  api: string;
  err: string;
};

// Previous Data Object
// type dataObject = {
//   namespace: string;
//   node: string;
//   pod: string;
//   podUsageCpuCoreSeconds: string;
//   periodEnd: Date;
//   periodStart: Date;
// };

type dataObject = {
  namespace: string;
  activationTime: number;
};

// To convert the date from the string format TODO:Fix
const parseISOString = (s: string) => {
  const b: Array<string> = s.split(/\D+/);
  return new Date(
    Date.UTC(
      Number.parseInt(b[0]),
      Number.parseInt(b[1]) - 1,
      Number.parseInt(b[2]),
      Number.parseInt(b[3]),
      Number.parseInt(b[4]),
      Number.parseInt(b[5])
    )
  );
};

class ProjectListWithTable extends React.Component<myProps, myState> {
  constructor(myProps) {
    super(myProps);

    this.state = {
      isLoaded: false,
      clusterData: [],
      api: 'https://c507295a-b340-4a31-a144-749e6fb4c08a.mock.pstmn.io/project_list_with_activation_time',
      err: ''
    };

    this.callAPI(this.props);
  }

  UNSAFE_componentWillReceiveProps(nextProps) {
    // console.log("HEYYYY")
    if (nextProps.changingDate === false) {
      this.callAPI(nextProps);
    }
  }

  callAPI(props) {
    const startDate = props.startDate.toISOString().split('.')[0] + 'Z';
    const endDate = props.endDate.toISOString().split('.')[0] + 'Z';

    let apiUrl = this.state.api;
    apiUrl = apiUrl + '/' + startDate + '/' + endDate;
    // console.log(apiUrl);

    axios
      .get(apiUrl)
      .then(res => {
        const tableData: Array<dataObject> = [];
        res.data.forEach(clusterInfo => {
          tableData.push({
            namespace: clusterInfo['namespace'],
            activationTime: clusterInfo['activation_time']
          });
        });
        this.setState({ ...this.state, isLoaded: true, clusterData: tableData });
      })
      .catch(err => {
        this.setState({ ...this.state, isLoaded: false, err: err });
      });
  }

  renderTable = () => {
    const columnTitle = {
      namespace: 'Namespace',
      activationTime: 'Project Active period'
    };

    return (
      <div>
        {this.state.clusterData.length !== 0 && (
          // <DashboardTable
          //   startDate={this.props.startDate}
          //   endDate={this.props.endDate}
          //   columnTitle={columnTitle}
          //   tableData={this.state.clusterData}
          // />
          <SearchToolBar data={this.state.clusterData} columnTitle={columnTitle}/>
        )}
      </div>
    );
  };

  render() {
    return (
      <div>
        {this.renderTable()}
        {/* {this.state.isLoaded && this.renderTable()} */}
        {/* {!this.state.isLoaded && <div>{this.state.err.toString()}</div>} */}
      </div>
    );
  }
}

export { ProjectListWithTable };
