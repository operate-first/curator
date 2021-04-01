import React from 'react';
import { shallow } from 'enzyme';
import { ReportsDataFilterForm } from './ReportsDataFilterForm';

// Tests for the reports page's filter form. 
describe('Reports Page Filter Form tests', () => {
  test('should render default Reports page filter form component', () => {
    const view = shallow(<ReportsDataFilterForm />);
    expect(view).toMatchSnapshot();
  })
})