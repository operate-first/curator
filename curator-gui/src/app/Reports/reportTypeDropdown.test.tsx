import React from 'react';
import { shallow } from 'enzyme';
import ReportTypeDropdown from './ReportTypeDropdown';

describe('Report Frequency Dropdown tests', () => {

  test('should render ReportTypeDropdown component', () => {

    const dropdown = shallow(<ReportTypeDropdown setReportType={() => {}} ReportType='Standard'/>);
    expect(dropdown.find('option')).toHaveLength(3);
    expect(dropdown.find('select').prop('value')).toEqual('Standard');
  });

  test('should handle ReportTypeDropdown change', () => {
    // eslint-disable-next-line no-undef
    const callback = jest.fn();
    const dropdown = shallow(<ReportTypeDropdown setReportType={callback} ReportType='Standard'/>);

    // simulate user changing value of component
    dropdown.find('select').simulate('change', { currentTarget: { value: 'Analytical' } });

    expect(callback.mock.calls.length).toBe(1);
    expect(callback.mock.calls[0][0]).toBe('Analytical'); // callback should be called with new value
  })
})