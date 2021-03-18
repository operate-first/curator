import React from 'react';
import { shallow } from 'enzyme';
import { SimpleInputGroups as DateComponent } from './DateComponent';

describe('DateComponent tests', () => {

  test('should render DateComponent component', () => {

    const dropdown = shallow(<DateComponent changeDate={() => { }} dateType='StartDate' initialDate={new Date(946750000000)}/>);
    expect(dropdown).toMatchSnapshot();
  });

  test('should handle DateComponent change', () => {
    // eslint-disable-next-line no-undef
    const callback = jest.fn();
    const dropdown = shallow(<DateComponent changeDate={callback} dateType='StartDate' />);

    // simulate user changing value of component
    dropdown.find('#StartDate').simulate('change', 3);

    expect(callback.mock.calls.length).toBe(1);
    expect(callback.mock.calls[0][0]).toBe(3); // callback should be called with new value
  })

})
