import * as React from 'react';
import { LoginPage } from './LoginPage';
import { shallow } from 'enzyme';
import { Role } from '..';

describe('LoginPage tests', () => {
  test('should render default LoginPage component', () => {
    const view = shallow(<LoginPage setRole={() => {}} setEmail={() => {}} />);
    expect(view).toMatchSnapshot();
  });

  test('should login after CILogon redirect', () => {
    const setRole = jest.fn();
    delete window.location;
    // @ts-ignore mock window location to include CILogon code
    window.location = {
        search: '?code=123',
    };
    shallow(<LoginPage setRole={setRole} setEmail={() => {}} />);
    expect(setRole).toBeCalledWith(Role.ADMIN)
  })
});
