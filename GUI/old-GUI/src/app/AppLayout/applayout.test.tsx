import React from 'react';
import { shallow, mount } from 'enzyme';
import { AppLayout } from './AppLayout';
import { BrowserRouter as Router } from 'react-router-dom';
import { Role } from '..';

describe('AppLayout tests', () => {

  test('should render AppLayout component', () => {
    const layout = shallow(<AppLayout role={Role.ADMIN} logout={() => {}}><span /></AppLayout>);
    expect(layout).toMatchSnapshot();
  });


  test('should hide the sidebar when clicking the nav-toggle button', () => {
    const wrapper = mount(<Router><AppLayout role={Role.ADMIN} logout={() => {}}><span /></AppLayout></Router>);
    const button = wrapper.find('#nav-toggle').hostNodes();
    expect(wrapper.find('#page-sidebar').hasClass('pf-m-collapsed')).toBeTruthy();

    button.simulate('click');
    expect(wrapper.find('#page-sidebar').hasClass('pf-m-expanded')).toBeTruthy();
    expect(wrapper.find('#page-sidebar').hasClass('pf-m-collapsed')).toBeFalsy();
  });

  test('should auto-close nav in mobile view', () => {
    const wrapper = mount(<Router><AppLayout role={Role.ADMIN} logout={() => {}}><span /></AppLayout></Router>);
    global.innerWidth = 500;
    // Trigger the window resize event
    global.dispatchEvent(new Event('resize'));
    expect(wrapper.find('#page-sidebar').hasClass('pf-m-collapsed')).toBeTruthy();
  })

})
