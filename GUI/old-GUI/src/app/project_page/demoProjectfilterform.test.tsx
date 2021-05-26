import React from 'react';
import { shallow } from 'enzyme';
import { DemoProjectFilterForm } from './demoProjectfilterform';

// Tests for the dashboard's project filter form page. 
// Dashboard Table and Dropdown Component have their own test files.
describe('Dashboard tests', () => {
  test('should render default Dashboard component', () => {
    const view = shallow(<DemoProjectFilterForm />);
    expect(view.state('startDate')).toBeInstanceOf(Date);
    expect(view.state('endDate')).toBeInstanceOf(Date);
    expect(view.state('changingDate')).toBeTruthy();
    expect(view.state('api')).toEqual(expect.any(String));
  })
})