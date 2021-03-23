import * as React from 'react';
import { PageSection, Title } from '@patternfly/react-core';
import { useParams } from 'react-router-dom';
import axios from 'axios';

import { Table, TableHeader, TableBody, TableVariant } from '@patternfly/react-table';

import { DashboardTable } from '@app/DashboardTable/DashboardTable';

let cluster_data = [] as any;
const ProjectDetail: React.FunctionComponent<{}> = () => {
    const [name, setName] = React.useState("")
    const [node, setNode] = React.useState("")
    const [start, setStart] = React.useState("")
    const [end, setEnd] = React.useState("")
    const [pod, setPod] = React.useState("")
    const [cpusage, setCpusage] = React.useState("")


    let { projectId } = useParams();
    //console.log(projectId)
    React.useEffect(() => {
        axios.get("https://bce15001-2baf-4479-8f5b-2a6a09ee7744.mock.pstmn.io/projectlist/" + projectId).then(res => {

            cluster_data = res.data;

            cluster_data.map((item: any) => {
                setName(item.namespace)
                setNode(item.node)
                setStart(item.period_start)
                setEnd(item.period_end)
                setPod(item.pod)
                setCpusage(item.pod_usage_cpu_core_seconds)
            })

        }).catch(err => {
            if (err.response) {
                //console.log(err.response + "--" + err.message)
            }
            else {
                // console.log(err.message)

            }
        });
    }, []);

    const columns = ['', '']
    const values = [['Name', name], ['Node', node], ['Start Time', start],
    ['End Time', end], ['Pod Time', pod], ['CPU Utilization', cpusage]]

    const rows =
        values.map(avalue => (
            { cells: avalue }
        ))


    return (

        <PageSection>
            <Title headingLevel="h1" size="lg">Projectpage</Title>
            <Table
                key={'dataTable'}
                aria-label="Compact Table"
                variant={TableVariant.compact}
                cells={columns}
                rows={rows}
            >
                <TableHeader />
                <TableBody />
            </Table>
        </PageSection>



    )
}

export { ProjectDetail };
