import React from 'react';
import { shallow } from 'enzyme';
import ReportFrequencyDropdown from './ReportFrequencyDropdown';

describe('Report Frequency Dropdown tests', () => {

  test('should render ReportFrequencyDropdown component', () => {

    const dropdown = shallow(<ReportFrequencyDropdown setReportFrequency={() => {}} ReportFrequency='Daily'/>);
    expect(dropdown.find('option')).toHaveLength(3);
    expect(dropdown.find('select').prop('value')).toEqual('Daily');
  });

  test('should handle ReportFrequencyDropdown change', () => {
    // eslint-disable-next-line no-undef
    const callback = jest.fn();
    const dropdown = shallow(<ReportFrequencyDropdown setReportFrequency={callback} ReportFrequency='Daily'/>);

    // simulate user changing value of component
    dropdown.find('select').simulate('change', { currentTarget: { value: 'Weekly' } });

    expect(callback.mock.calls.length).toBe(1);
    expect(callback.mock.calls[0][0]).toBe('Weekly'); // callback should be called with new value
  })
})