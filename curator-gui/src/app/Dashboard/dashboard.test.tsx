import React from 'react';
import { shallow } from 'enzyme';
import { Dashboard } from './Dashboard';

describe('Dashboard tests', () => {

  // Dashboard currently does not use state, so further tests are not needed
  test('should render default Dashboard component', () => {
    const view = shallow(<Dashboard />);
    expect(view).toMatchSnapshot();
  })

})