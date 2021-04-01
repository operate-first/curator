import React from 'react';
import { Grid, GridItem, Form, ActionGroup, Alert } from '@patternfly/react-core';
import axios from 'axios';
import { SimpleInputGroups } from '@app/DateComponent/DateComponent';
import { Button } from '@patternfly/react-core';
import ReportsList from './ReportsList';
import CsvDownload from 'react-json-to-csv';
import ReportTypeDropdown from './ReportTypeDropdown';
import ReportFrequencyDropdown from './ReportFrequencyDropdown';
import ReportsAnalytical from './ReportsAnalytical';

type myProps = {};
type myState = {
    startDate: Date;
    conditionalRender: number;
    changingDate: boolean;
    api: string;
    clusterData: Array<dataObject> | null;
    err: string | null;
    isLoaded: boolean;
    reportType: string;
    changingReportType: boolean;
    reportFrequency: string;
    changingReportFrequency: boolean;
};
export type dataObject = {
    namespace: string;
    podUsageCpuCoreSeconds: number;

};

const convertDateToUTC = (date: Date) => {
    return Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(), date.getUTCHours(), 0, 0, 0);
};

/*
Form for users to specify the start date, report frequency(daily, weekly, monthly), and report type
(standard, analytical, custom) of a metering report. Also offers an option to export metering data from the
backend as csv.
*/
class ReportsDataFilterForm extends React.Component<myProps, myState> {
    constructor(myProps) {
        super(myProps);

        this.state = {
            startDate: new Date(),
            conditionalRender: 0,
            changingDate: true,
            api: 'http://localhost:8000/namespace_cpu_request',
            clusterData: null,
            err: null,
            isLoaded: false,
            reportType: 'standard',
            changingReportType: false,
            reportFrequency: 'day',
            changingReportFrequency: false
        };

        this.callAPI(false);
    }


    shouldComponentUpdate(nextProps, nextState) {
        return JSON.stringify(this.state) !== JSON.stringify(nextState);
    }


    callAPI(onSubmit) {
        const startDate = new Date(convertDateToUTC(this.state.startDate)).toISOString().split('T', 1)[0];

        let apiUrl = this.state.api;
        if (onSubmit) {
            apiUrl = apiUrl + '/' + this.state.reportType + '?start=' + startDate + '&frequency=' + this.state.reportFrequency;
        }

        axios
            .get(apiUrl)
            .then(res => {
                this.setState({ ...this.state, isLoaded: true, clusterData: res.data });
            })
            .catch(err => {
                this.setState({ ...this.state, isLoaded: false, err: err });
            });
    }

    changeToggle() {
        this.callAPI(true);
    }

    setDate = (date: Date) => {
        date = new Date(date);
        date.setDate(date.getDate() + 1);
        this.setState({ ...this.state, changingDate: true, startDate: new Date(date) });
    };

    setReportType = (aType: string) => {
        this.setState({ ...this.state, changingReportType: true, reportType: aType });
    };

    setReportFrequency = (aFrequency: string) => {
        this.setState({ ...this.state, changingReportFrequency: true, reportFrequency: aFrequency });
    };

    renderReport = () => {
        switch (this.state.reportType) {
            case 'standard':
                return (this.renderStandard());
            case 'analytics':
                return (this.renderAnalytical());
            case '':
                return (this.renderReportingError('Unable to generate report. Report Type not specified.'));
            default:
                return (this.renderReportingError('Unable to generate report. Report Type not yet supported.'));
        }
    }

    // Renders a error banner which displays a provided string value
    renderReportingError(message: string) {
        return (
            <React.Fragment>
                <Alert variant="danger" isInline title={message} />
            </React.Fragment>
        )
    }

    // Generates a standard report, a table with columns for namespace, cpu usage, network usage,
    // and memory usage.
    renderStandard = () => {
        const columnTitle = {
            namespace: 'namespace',
            podUsageCpuCoreSeconds: 'Pod CPU Usage in Seconds',

        };

        const tableData: Array<dataObject> = [];

        if (this.state.clusterData !== null) {
            this.state.clusterData['reports'].forEach(clusterInfo => {
                tableData.push({
                    namespace: clusterInfo['namespace'],
                    // Note: The line below should be `podUsageCpuCoreSeconds: clusterInfo['pod_usage_cpu_core_seconds']`
                    // The mock API call only supports 'pod_request_cpu_core_seconds' but
                    // I want to ensure that the value gets rendered.
                    podUsageCpuCoreSeconds: clusterInfo['pod_request_cpu_core_seconds'],
                })
            })
        }

        return (
            <div>
                {this.state.clusterData !== null && (
                    <ReportsList
                        key={'ReportsList'}
                        startDate={this.state.startDate}
                        columnTitle={columnTitle}
                        tableData={tableData}
                    />
                )}
            </div>
        );
    };

    // Generates an analytical report: line graphs for each namespace with
    // lines denoting CPU, network, and memory usage.
    renderAnalytical = () => {
        const columnTitle = {};
        let idx = 0;
        return (
            <div>
                {this.state.clusterData !== null && (this.state.clusterData['reports']
                    .map((value, idx) => {
                        idx++;
                        return (
                            <ReportsAnalytical
                                key={idx}
                                indexNum={idx}
                                columnTitle={columnTitle}
                                cpuUsage={value['cpu_usage']}
                                networkUsage={value['network_usage']}
                                memoryUsage={value['memory_usage']}
                                namespace={value['namespace']}
                                startDate={this.state.startDate}
                                reportFrequency={this.state.reportFrequency} />)
                    }))}
            </div>
        )
    }

    render() {
        return (
            <React.Fragment>
                <Form>
                    <div>Select a date range to view available Daily, Weekly, and Monthly reports.</div>
                    <Grid>
                        <GridItem span={8}>
                            <SimpleInputGroups changeDate={this.setDate} dateType="Date" key="Date" />
                        </GridItem>
                    </Grid>
                    <Grid>
                        <GridItem span={6}>
                            <CsvDownload data={this.state.clusterData}>Download as CSV</CsvDownload>
                        </GridItem>
                    </Grid>
                    <Grid>
                        <GridItem span={8}>
                            <ReportTypeDropdown setReportType={this.setReportType} ReportType={this.state.reportType} />
                        </GridItem>
                    </Grid>
                    <Grid>
                        <GridItem span={8}>
                            <ReportFrequencyDropdown setReportFrequency={this.setReportFrequency} ReportFrequency={this.state.reportFrequency} />
                        </GridItem>
                    </Grid>
                    <Grid>
                        <ActionGroup>
                            <GridItem span={6}>
                                <Button onClick={() => this.changeToggle()}>Submit</Button>
                            </GridItem>
                        </ActionGroup>
                    </Grid>
                    <Grid>
                        <GridItem span={10} rowSpan={8}>
                            {this.state.isLoaded && this.renderReport()}
                            {!this.state.isLoaded && this.state.err !== null && <div>{this.state.err.toString()}</div>}
                        </GridItem>
                    </Grid>
                </Form>
            </React.Fragment>
        );
    }
}

export { ReportsDataFilterForm };
