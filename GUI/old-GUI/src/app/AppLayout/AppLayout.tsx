import * as React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Nav,
  NavList,
  NavItem,
  Page,
  PageHeader,
  PageSidebar,
  SkipToContent,
  PageHeaderTools,
  Button
} from '@patternfly/react-core';
import { routes } from '@app/routes';
import { Role, RoleMap } from '@app/index';
import styles from '@patternfly/react-styles/css/components/Page/page';
import { css } from '@patternfly/react-styles';

interface IAppLayout {
  children: React.ReactNode;
  role: Role;
  email: string;
  logout: Function;
}

const AppLayout: React.FunctionComponent<IAppLayout> = ({ children, role, email, logout }) => {
  
  const [isNavOpen, setIsNavOpen] = React.useState(true);
  const [isMobileView, setIsMobileView] = React.useState(true);
  const [isNavOpenMobile, setIsNavOpenMobile] = React.useState(false);

  const onNavToggleMobile = () => {
    setIsNavOpenMobile(!isNavOpenMobile);
  };
  const onNavToggle = () => {
    setIsNavOpen(!isNavOpen);
  };
  const onPageResize = (props: { mobileView: boolean; windowSize: number }) => {
    setIsMobileView(props.mobileView);
  };
  const Header = (
    <PageHeader
      logo="Mass Open Cloud"
      headerTools={
        <PageHeaderTools>
          <a className={css(styles.pageHeaderBrandLink)}>
          {email || RoleMap[role]}
          </a>
          &nbsp;
          <Button onClick={() => logout()}> LOGOUT </Button>
        </PageHeaderTools>
      }
      showNavToggle
      isNavOpen={isNavOpen}
      onNavToggle={isMobileView ? onNavToggleMobile : onNavToggle}
    />
  );

  const Navigation = (
    <Nav id="nav-primary-simple" theme="dark">
      <NavList id="nav-list-simple">
        {routes.map(
          (route, idx) =>
            route.label && (
              <NavItem key={`${route.label}-${idx}`} id={`${route.label}-${idx}`}>
                <NavLink exact to={route.path} activeClassName="pf-m-current">
                  {route.label}
                </NavLink>
              </NavItem>
            )
        )}
      </NavList>
    </Nav>
  );
  const Sidebar = <PageSidebar theme="dark" nav={Navigation} isNavOpen={isMobileView ? isNavOpenMobile : isNavOpen} />;
  //const PageSkipToContent = <SkipToContent href="#primary-app-container">Skip to Content</SkipToContent>;

  return (
    <Page
      mainContainerId="primary-app-container"
      header={Header}
      sidebar={Sidebar}
      onPageResize={onPageResize}
     // skipToContent={PageSkipToContent}
    >
      {children}
    </Page>
  );
};

export { AppLayout };
