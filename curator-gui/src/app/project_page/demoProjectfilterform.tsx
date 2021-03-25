import React from 'react';
import { Grid, GridItem, Form, ActionGroup } from '@patternfly/react-core';
import axios from 'axios';
import { SimpleInputGroups } from '@app/DateComponent/DateComponent';
import { Button, FormGroup, InputGroup, TextInput } from '@patternfly/react-core';
import SearchToolBar from '@app/SearchToolbar/SearchToolBar';
import * as moment from 'moment';
import 'moment-timezone'

type myProps = {};
type myState = {
  startHrs: string;
  endHrs: string;
  startDate: Date;
  endDate: Date;
  conditionalRender: number;
  changingDate: boolean;
  api: string;
  clusterData: Array<dataObject> | null;
  err: string | null;
  isLoaded: boolean;
};
export type dataObject = {
  namespace: string;
  activationTime: number;
};

const convertDateToUTC = (date: Date) => {
  return Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(), date.getUTCHours(), 0, 0, 0);
};

class DemoProjectFilterForm extends React.Component<myProps, myState> {
  constructor(myProps) {
    super(myProps);

    var timeZone = "America/New_York";
    const startDate = new Date();
    startDate.setHours(new Date().getHours() - 1);
    startDate.setMinutes(0);
    startDate.setSeconds(0);

    const endDate = new Date();
    endDate.setHours(new Date().getHours());
    endDate.setMinutes(0);
    endDate.setSeconds(0);

    var d = new Date();
    var minutes = moment(d).minutes();


    if (minutes <= 15) {
      var formattedstartdatestr = moment(d).subtract(2, 'hours').subtract(minutes, 'minutes').tz(timeZone).format('HH:mm');
      var formattedenddatestr = moment(d).subtract(1, 'hours').subtract(minutes, 'minutes').tz(timeZone).format('HH:mm');
    }
    else {
      var formattedstartdatestr = moment(d).subtract(1, 'hours').subtract(minutes, 'minutes').tz(timeZone).format('HH:mm');
      var formattedenddatestr = moment(d).subtract(minutes, 'minutes').tz(timeZone).format('HH:mm');
    }

    this.state = {
      // startHrs: (new Date().getHours() - 1).toString() + ":" + (new Date().getMinutes().toString().length == 1 ? "0" + new Date().getMinutes().toString() : new Date().getMinutes().toString()),
      // endHrs: (new Date().getHours()).toString() + ":" + (new Date().getMinutes().toString().length == 1 ? "0" + new Date().getMinutes().toString() : new Date().getMinutes().toString()),
      startHrs: formattedstartdatestr,
      endHrs: formattedenddatestr,
      startDate: new Date(startDate),
      endDate: new Date(endDate),
      conditionalRender: 0,
      changingDate: true,
      api: 'https://c507295a-b340-4a31-a144-749e6fb4c08a.mock.pstmn.io/project_list_with_activation_time',
      clusterData: null,
      err: null,
      isLoaded: false
    };
    this.callAPI(false);
  }

  shouldComponentUpdate(nextProps, nextState) {
    //console.log(nextState);
    return JSON.stringify(this.state) !== JSON.stringify(nextState);
  }

  callAPI(onSubmit) {
    const startDate = new Date(convertDateToUTC(this.state.startDate)).toISOString().split('.')[0] + 'Z';
    const endDate = new Date(convertDateToUTC(this.state.endDate)).toISOString().split('.')[0] + 'Z';

    let apiUrl = this.state.api;
    if (onSubmit) {
      apiUrl = apiUrl + '/' + startDate + '/' + endDate;
    }

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

  changeToggle = () => {
    this.callAPI(true);
    console.log(this.state.startHrs)
    // const conditionalRender: number = this.state.conditionalRender;
    // this.setState({
    //   ...this.state,
    //   changingDate: false,
    //   conditionalRender: conditionalRender + 1
    // });
  };

  setStartHrs = (hrs: string) => {
    var hrsMints = hrs.split(":");
    console.log("HERE")
    console.log(hrsMints);
    const date = new Date(this.state.startDate);
    date.setHours(parseInt(hrsMints[0]));
    date.setMinutes(parseInt(hrsMints[1]));

    this.setState({
      ...this.state,
      changingDate: true,
      startHrs: hrs,
      startDate: new Date(date)
    });
    console.log({ debug: hrs })

  };

  setEndHrs = (hrs: string) => {

    console.log({ debug: hrs })

    var hrsMints = hrs.split(":")
    const date = new Date(this.state.endDate);
    date.setHours(parseInt(hrsMints[0]));
    date.setMinutes(parseInt(hrsMints[1]));
    this.setState({
      ...this.state,
      changingDate: true,
      endHrs: hrs,
      endDate: new Date(date)
    });

  };

  setStartDate = (date: Date) => {
    var hrsMints = this.state.startHrs.split(":")
    date = new Date(date);
    date.setHours(parseInt(hrsMints[0]));
    date.setMinutes(parseInt(hrsMints[1]));
    date.setDate(date.getDate() + 1);
    this.setState({ ...this.state, changingDate: true, startDate: new Date(date) });
  };

  setEndDate = (date: Date) => {
    var hrsMints = this.state.endHrs.split(":")
    date = new Date(date);
    date.setHours(parseInt(hrsMints[0]));
    date.setMinutes(parseInt(hrsMints[1]));
    date.setDate(date.getDate() + 1);
    this.setState({ ...this.state, changingDate: true, endDate: new Date(date) });
  };

  renderTable = () => {
    const columnTitle = {
      namespace: 'Namespace',
      activationTime: 'Project Active period'
    };

    return (
      <div>
        {this.state.clusterData !== null && (
          <SearchToolBar data={this.state.clusterData} columnTitle={columnTitle} />
        )}
      </div>
    );
  };

  render() {
    return (

      <React.Fragment>
        <Form>
          <Grid>
            <GridItem span={6}>
              <SimpleInputGroups changeDate={this.setStartDate} dateType="StartDate" key="StartDate" />
              {/* {convertDateToUTC(this.state.startDate).toISOString()} */}
            </GridItem>
            <GridItem span={6}>
              <SimpleInputGroups changeDate={this.setEndDate} dateType="EndDate" key="EndDate" />
            </GridItem>
          </Grid>
          <Grid>
            <GridItem span={6}>
              {/* Time element for start and end hours for data filter. Using default patternfly components */}
              <FormGroup label="Start Hrs" isRequired
                fieldId="Start Hrs">
                <InputGroup className="timergroup">

                  <TextInput
                    name="textInput"
                    id="Start Hrs"
                    type="time"
                    min="00:00"
                    max="24:00"
                    aria-label="Input Time"
                    onChange={value => { this.setStartHrs(value); }}
                    value={this.state.startHrs}
                  />
                  </InputGroup>
              </FormGroup>
            </GridItem>
            <GridItem span={6}>
              {/* Time element for start and end hours for data filter. Using default patternfly components */}
              <FormGroup label="End Hrs" isRequired
                fieldId="End Hrs">
                <InputGroup className="timergroup">
                  <TextInput
                    name="textInput"
                    id="End Hrs"
                    type="time"
                    aria-label="Input Time"
                    onChange={value => { this.setEndHrs(value); }}
                    value={this.state.endHrs}
                  />
                </InputGroup>
              </FormGroup>
            </GridItem>
          </Grid>
          <Grid>
            <ActionGroup>
              <GridItem span={6}>
                <Button onClick={() => this.changeToggle()}>Search</Button>
              </GridItem>
            </ActionGroup>
          </Grid>
          <Grid>
            <GridItem span={11} rowSpan={8}>
              {/* <ProjectListTable
              changingDate={this.state.changingDate}
              renderCount={this.state.conditionalRender}
              startDate={new Date(convertDateToUTC(this.state.startDate))}
              endDate={new Date(convertDateToUTC(this.state.endDate))}
            /> */}
              {this.state.isLoaded && this.renderTable()}
              {!this.state.isLoaded && this.state.err !== null && <div>{JSON.stringify(this.state.err["response"]["data"]["error"]["message"])}</div>}
            </GridItem>
          </Grid>
        </Form>
      </React.Fragment>
    );
  }
}
export { DemoProjectFilterForm };
