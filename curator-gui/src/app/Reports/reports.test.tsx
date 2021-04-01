import React from 'react';
import { shallow } from 'enzyme';
import { Reports } from './Reports';

describe('Reports tests', () => {

    // Reports currently does not use state, so further tests are not needed
    test('should render default Reports component', () => {
      const view = shallow(<Reports />);
      expect(view).toMatchSnapshot();
    })
  
  })