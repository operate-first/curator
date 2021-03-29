import React from 'react';
import { Toolbar, ToolbarContent, ToolbarItem, InputGroup, TextInput, Button, ButtonVariant } from '@patternfly/react-core';
import { SearchIcon, CloseIcon } from '@patternfly/react-icons';

import { DashboardTable } from '@app/DashboardTable/DashboardTable';

type myProps = {
  data: Array<dataObject>;
  columnTitle: object;
};

type dataObject = {
  namespace: string;
  activationTime: number;
};

type myState = {
  mainData: Array<dataObject>;
  displayData: Array<dataObject>;
  filterTag: string;
};

class SearchToolBar extends React.Component<myProps, myState> {
  constructor(props: myProps) {
    super(props);
    this.state = {
      mainData: this.props.data,
      displayData: this.props.data,
      filterTag: ''
    };
  }


  UNSAFE_componentWillReceiveProps(nextProps: myProps) {
    this.setState({
      mainData: nextProps.data,
      displayData: nextProps.data,
      filterTag: ''
    })
  }

  render() {
    return (
      <React.Fragment>

        {/*console.log(this.state.displayData)*/}
        {/*console.log(this.props.columnTitle)*/}
        <DashboardTable tableData={this.state.displayData} columnTitle={this.props.columnTitle} />
      </React.Fragment>
    );
  }
  reset() {
    this.setState({ ...this.state, filterTag: "", displayData: this.props.data, mainData: this.props.data })
  }
  search(filterTag: string) {
    const tags = filterTag.trim().split(" ");
    const regExps: Array<RegExp> = tags.map(tag => new RegExp(tag));
    const filterData: Array<dataObject> = this.state.mainData;
    const newData = filterData.filter(object => regExps.some(exp => object.namespace.match(exp)))
    this.setState({ ...this.state, filterTag: filterTag, displayData: newData, mainData: this.props.data })
  }
}

export default SearchToolBar;
