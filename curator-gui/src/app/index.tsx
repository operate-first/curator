import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import '@patternfly/react-core/dist/styles/base.css';

import { AppLayout } from '@app/AppLayout/AppLayout';
import { AppRoutes } from '@app/routes';
import '@app/app.css';
import { LoginPage } from './LoginPage/LoginPage';

type myState = {
  role: Role;
  email?: string;
};

export const enum Role {
  ADMIN,
  DEVELOPER,
  NONE
}

export const RoleMap = ["Admin", "Developer"]
type myProps = {};

class App extends React.Component<myProps, myState> {
  constructor(props) {
    super(props);
    this.state = {
      role: Role.NONE
    };
  }

  handleRoleChange = (role: Role) => {
    this.setState({ role: role });
  }

  handleEmailChange = (email: string) => {
    this.setState({ email });
  }

  logout = () => {
    this.setState({ role: Role.NONE, email: ''});
    localStorage.removeItem('login');
    localStorage.removeItem('email');
  }

  render() {
    return (
      <div role="heading" aria-label="OCP Metering" aria-level={0}>
        {this.state.role=== Role.NONE && <LoginPage setRole={this.handleRoleChange} setEmail={this.handleEmailChange} />}
        {this.state.role !== Role.NONE && (
          <Router>
            <AppLayout role={this.state.role} logout={this.logout} email={this.state.email || ''}>
              <AppRoutes />
            </AppLayout>
          </Router>
        )}
      </div>
    );
  }

}


export { App };

