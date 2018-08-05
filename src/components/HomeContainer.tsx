import * as React from 'react';

import { NoProps } from '../types';
import Page from './Page';
import Home from './Home';

interface State {
  isUpdating: boolean;
}

export default class HomeContainer extends React.Component<NoProps, State> {
  constructor(props: NoProps) {
    super(props);

    this.state = {
      isUpdating: false
    };
  }

  render() {
    return (
      <Page>
        <Home />
      </Page>
    );
  }
}