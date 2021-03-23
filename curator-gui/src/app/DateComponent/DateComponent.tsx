import React from 'react';
import { CalendarAltIcon } from '@patternfly/react-icons';
import { InputGroup, InputGroupText, TextInput, FormGroup } from '@patternfly/react-core';

type myProps = {
  changeDate: Function;
  dateType: string;
  initialDate?: Date; // for unit testing/snapshots
}

type myState = {
  currentDate: Date;
}

class SimpleInputGroups extends React.Component<myProps, myState> {
  constructor(myProps: myProps) {
    super(myProps);

    this.state = {
      currentDate: myProps.initialDate || new Date()
    };
  }

  formatDate(date) {
    var d = new Date(date);
    var month = '' + (d.getMonth() + 1),
      day = '' + d.getDate(),
      year = d.getFullYear();

    if (month.length < 2)
      month = '0' + month;
    if (day.length < 2)
      day = '0' + day;

    return [year, month, day].join('-');
  }

  updateDateValue(newDate) {
    this.setState({ currentDate: newDate });
  }

  render() {
    return (
      <React.Fragment>
        <FormGroup label={this.props.dateType}
          isRequired
          fieldId={this.props.dateType}
        >
          <InputGroup>

            <TextInput
              name="textInput"
              id={this.props.dateType}
              type="date"
              aria-label="Input Date"
              onChange={value => { this.props.changeDate(value); this.updateDateValue(value) }}
              value={this.formatDate(this.state.currentDate)}
            />

            <InputGroupText component="label" htmlFor="textInput9">
              <CalendarAltIcon />
            </InputGroupText>

          </InputGroup>

        </FormGroup>

      </React.Fragment>
    );
  }
}

export { SimpleInputGroups };
