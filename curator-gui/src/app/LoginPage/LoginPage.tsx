import React from 'react';
import {
  LoginPage as PatternflyLoginPage,
  ListVariant,
  Button
} from '@patternfly/react-core';
import { LoginForm } from './LoginPageForm';
import { ExclamationCircleIcon } from '@patternfly/react-icons';
import * as OAuth from 'oauth2-client-js';

import { Role } from '..';
import mocLogo from './moc_logo.png';
import { ResetPasswordForm } from './ResetPasswordForm';
import axios from 'axios';
import { debug } from 'console';

// get user info from CILogon
async function getUserEmail(code: string) {
  const { access_token } = await fetch('https://cilogon.org/oauth2/token', {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    method: "POST",
    body: `grant_type=authorization_code&client_id=cilogon:/client_id/566ba77604386302bd6e0f63cfa0efe0&client_secret=${process.env.CILOGON_SECRET}&redirect_uri=http://localhost:9000&code=${code}`
  }).then(r => r.json());
  const userInfo = await fetch('https://cilogon.org/oauth2/userinfo', {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    method: 'POST',
    body: `access_token=${access_token}`
  }).then(r => r.json());
  return userInfo.email;
}

type LoginState = {
  username: string;
  password: string;
  submit: boolean;
  error?: string;
  isLoginPage: boolean;
  api: string;
  isValidUser: boolean;
  isValidOldPassword?: boolean;
  isResetPasswordProcessed?: boolean;
  oldPassword: string;
  newPassword: string;
  confirmPassword: string;
};

type ResetPasswordState = {
  oldPassword: string;
  newPassword: string;
  confirmPassword: string;
  submit: boolean;
  error?: string;
};

type LoginProps = {
  setRole: Function;
  setEmail: Function;
};

class LoginPage extends React.Component<LoginProps, LoginState, ResetPasswordState> {
  constructor(props: LoginProps) {
    super(props);
    this.state = {
      username: '',
      password: '',
      submit: false,
      isLoginPage: true,
      api: 'https://cce4c6f9-ed0c-4bd9-94c7-6f174f7ae024.mock.pstmn.io/login',
      isValidUser: true,
      isValidOldPassword: undefined,
      isResetPasswordProcessed: undefined,
      oldPassword: "",
      newPassword: "",
      confirmPassword: "",
    };
  }

  // Detect if CILogon has authenticated, then log into app if it has.
  async componentDidMount() {
    const query = window.location.search;
    if (query.includes('code')) { // CILogon has returned with code
      // remove query & CILogon state from URL, without reloading page
      console.log('hi')
      const code = new URLSearchParams(query).get('code');
      const urlWithoutQuery = window.location.protocol + "//" + window.location.host + window.location.pathname
      window.history.pushState({ path: urlWithoutQuery }, '', urlWithoutQuery);
      this.props.setRole(Role.ADMIN);
      localStorage.setItem('login', 'ADMIN');
      if (code) {
        const email = await getUserEmail(code);
        this.props.setEmail(email);
        localStorage.setItem('email', email);
      }
    } else if (localStorage.getItem('login')) {
      const storedRole = localStorage.getItem('login');
      if (storedRole === 'ADMIN') {
        this.props.setRole(Role.ADMIN);
      } else if (storedRole === 'DEVELOPER') {
        this.props.setRole(Role.DEVELOPER);
      }
    }
    if (localStorage.getItem('email')) {
      this.props.setEmail(localStorage.getItem('email'));
    }
  }

  handleOldPasswordChange = (oldPassword: string) => {
    this.setState({ oldPassword: oldPassword });
  }
  handlenewPasswordChange = (newPassword: string) => {
    this.setState({ newPassword: newPassword });
  }
  handleConfirmPasswordChange = (confirmPassword: string) => {
    this.setState({ confirmPassword: confirmPassword });
  }

  handleUsernameChange = (userNameInput: string) => {
    this.setState({ username: userNameInput });
  }

  handlePasswordChange = (passwordInput: string) => {
    this.setState({ password: passwordInput });
  }

  validateOldPassword = () => {
    let apiUrl = "https://cce4c6f9-ed0c-4bd9-94c7-6f174f7ae024.mock.pstmn.io/validate_old_password?old_password="
    axios
      .get(apiUrl + this.state.oldPassword)
      .then(res => {
        if (res && res.data) {
          if (res.data["is_valid"] == "true") {
            this.setState({ ...this.state, isValidOldPassword: true });
          }
          else {
            this.setState({ ...this.state, isValidOldPassword: false });
          }
        }
      })
      .catch(err => {
        this.setState({ ...this.state, isValidUser: false, error: err });
      });
  }

  resetPassword = (event: React.MouseEvent) => {
    event.preventDefault();
    let apiUrl = "https://cce4c6f9-ed0c-4bd9-94c7-6f174f7ae024.mock.pstmn.io/reset"
    const credential = {
      oldPassword: this.state.oldPassword,
      newPassword: this.state.newPassword
    };
    this.setState({ isValidOldPassword: undefined })
    axios
      .post(apiUrl, { credential })
      .then(res => {
        if (res && res.data) {
          if (res.data["status"] == "true") {
            this.setState({ ...this.state, isResetPasswordProcessed: true });
          }
          else {
            this.setState({ ...this.state, isResetPasswordProcessed: false, error: "Invalid Username/Password" });
          }
          this.setState({ ...this.state, oldPassword: "", newPassword: "", confirmPassword: "" });
        }
      })
      .catch(err => {
        this.setState({ ...this.state, isResetPasswordProcessed: false, error: err });
      });
  }

  handleSubmit = (event: React.MouseEvent) => {
    event.preventDefault();
    this.setState({ error: "" })
    // dynamic call
    const { username, password } = this.state;
    let role: Role;
    let apiUrl = this.state.api;
    const credential = {
      username: username,
      password: password
    };
    axios
      .post(apiUrl, { credential })
      .then(res => {
        if (res && res.data) {
          if (res.data["is_valid"] == "true") {
            this.setState({ ...this.state, isValidUser: true });
            role = Role.ADMIN;
            this.props.setRole(role);
          }
          else {
            this.setState({ ...this.state, isValidUser: false, error: "Invalid Username/Password" });
          }
        }
      })
      .catch(err => {
        this.setState({ ...this.state, isValidUser: false, error: err });
      });

    // if (username === 'admin' && password === 'adminpass') {
    //   role = Role.ADMIN;
    //   localStorage.setItem('login', 'ADMIN');
    // } else if ((username === 'developer1' && password === 'developer1pass') || (username === 'developer2' && password === 'developer2pass')) {
    //   role = Role.DEVELOPER;
    //   localStorage.setItem('login', 'DEVELOPER');
    // } else {
    //   role = Role.NONE;
    //   this.setState({ ...this.state, error: "Invalid Username/Password" })
    // }
    // this.props.setRole(role);
  }

  handleCiLogon = () => {
    // Register provider
    const ciLogonProvider = new OAuth.Provider({
      id: 'cilogon',
      authorization_url: 'https://cilogon.org/authorize'
    })

    // Create a new request
    var request = new OAuth.Request({
      client_id: 'cilogon:/client_id/566ba77604386302bd6e0f63cfa0efe0',  // required
      redirect_uri: 'http://localhost:9000',
      scope: 'openid+profile+email+org.cilogon.userinfo',
      response_type: 'code'
    });

    // Give it to the provider
    var uri = ciLogonProvider.requestToken(request);

    // Redirect to CILogon authentication page
    window.location.href = uri;
  }

  showResetPasswordScreen = () => {
    this.setState({ isLoginPage: false });
  }
  showLoginScreen = () => {
    this.setState({ isLoginPage: true });
  }

  render() {

    const loginForm = (
      <LoginForm
        showHelperText={!!this.state.error}
        helperText={this.state.error}
        helperTextIcon={<ExclamationCircleIcon />}
        usernameLabel="Username"
        usernameValue={this.state.username}
        onChangeUsername={this.handleUsernameChange}
        passwordLabel="Password"
        passwordValue={this.state.password}
        onChangePassword={this.handlePasswordChange}
        onLoginButtonClick={this.handleSubmit}
        onResetButtonClick={this.showResetPasswordScreen}
      />

    );

    const resetForm = (
      <ResetPasswordForm
        showHelperText={!!this.state.error}
        helperText={this.state.error}
        helperTextIcon={<ExclamationCircleIcon />}
        oldPasswordValue={this.state.oldPassword}
        oldPasswordLabel="Old Password"
        onChangeOldPassword={this.handleOldPasswordChange}
        onBlurOldPasswordValue={this.validateOldPassword}
        newPasswordValue={this.state.newPassword}
        newPasswordLabel="New password"
        onChangeNewPassword={this.handlenewPasswordChange}
        onChangeConfirmPassword={this.handleConfirmPasswordChange}
        confirmPasswordValue={this.state.confirmPassword}
        confirmPasswordLabel="Confirm password"
        onLoginButtonClick={this.resetPassword}
        onResetButtonClick={this.showLoginScreen}
      />
    );

    return (

      <PatternflyLoginPage
        style={{
          background: 'linear-gradient(0deg, gray, transparent)',
        }}
        footerListVariants={ListVariant.inline}
        footerListItems={[
          <Button onClick={this.handleCiLogon} key="cilogon">Login with Institution/Google Account</Button>
        ]}
        brandImgSrc={mocLogo}
        brandImgAlt="MOC logo"
        textContent="Mass Open Cloud OCP Metering"
        loginTitle={this.state.isLoginPage ? "Log in to your account" : "Reset Your Password"}
        loginSubtitle={this.state.isLoginPage ? "Please use your MOC credentials" : "Please use your MOC previous credentials to reset your password"}
      >
        {this.state.isLoginPage ? loginForm : resetForm}
        {/* {this.state.isLoginPage ? <div style={{ color: "red" }} > {this.state.isValidUser == false ? "Invalid Credentials" : null}</div> : null}*/}
        {(this.state.isLoginPage == false && this.state.isValidOldPassword != undefined) ? <div style={{ color: this.state.isValidOldPassword ? "green" : "red" }} > {this.state.isValidOldPassword == true ? "Verified Old Password" : "Invalid Old Password"}</div> : null}
        {(this.state.isLoginPage == false && this.state.isResetPasswordProcessed != undefined) ? <div style={{ color: this.state.isResetPasswordProcessed ? "green" : "red" }} > {this.state.isResetPasswordProcessed ? "Updated your password successfully" : "Error is occured. Please contact admin!"}</div> : null}
      </PatternflyLoginPage >
    );
  }
}

export { LoginPage };
