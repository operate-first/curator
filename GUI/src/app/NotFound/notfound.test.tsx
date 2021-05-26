import React from 'react';
import { shallow } from 'enzyme';
import { NotFound } from './NotFound';

describe('NotFound tests', () => {

  test('should render default NotFound component', () => {
    const view = shallow(<NotFound />);
    expect(view).toMatchSnapshot();
  })

})
