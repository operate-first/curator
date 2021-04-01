import React, { EventHandler } from 'react';

type myProps = {
  setReportFrequency: Function;
  ReportFrequency: string;
}

type myState = {
}

/*
Dropdown component for the Reports page to specify one of three report frequencies:
Daily, Weekly, and Monthly.
*/
class ReportFrequencyDropdown extends React.Component<myProps,myState>{
  constructor(myProps) {
    super(myProps);
    this.state = {
    }
  }

  ReportFrequency=(event: React.FormEvent<HTMLSelectElement>)=>{
    this.props.setReportFrequency(event.currentTarget.value)
  }

  createDropDowns(key: string, reportFrequencies: Array<string>, onChange: Function, def: string ) {
    return(
      <React.Fragment>
        <label>Select Report Frequency</label>
      <select key={key} onChange={e=>onChange(e)} value={def} aria-label="Report Frequency">
         
        {reportFrequencies.map((i)=>{ 
          return(<option key={key+i} value={i}>{i}</option>)
        } )}
      </select>

      </React.Fragment>      
    )  
  }

  render() {
    const reportTypes: Array<string> = ['day', 'week', 'month']
    return (
      
      <div>
        {this.createDropDowns("Report Frequency",reportTypes,this.ReportFrequency,this.props.ReportFrequency)}
      </div>
    );
  }
}

export default ReportFrequencyDropdown
