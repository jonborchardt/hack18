import { isEmpty } from 'lodash';
import * as React from 'react';
import styled from 'styled-components';

interface Props {
  children: JSX.Element[] | React.ReactNode;
}

interface State {
  error?: Error;
  errorInfo?: React.ErrorInfo;
}

class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      error: null,
      errorInfo: null
    };

    this.getComponentNameFromStack = this.getComponentNameFromStack.bind(this);
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
  }

  getComponentNameFromStack() {
    const split = this.state.errorInfo.componentStack.split('\n');
    // The stack has a newline before the first component (usually?)
    const topComponentString = isEmpty(split[0]) ? split[1] : split[0];
    // Matches "in [ComponentNameHere] ("
    const componentNameRegex = /in\s+(\w+)\s+\(/;
    const res = componentNameRegex.exec(topComponentString);

    if (res && res.length >= 2) {
      // Return the component name if the regex matched something
      return res[1];
    } else {
      // Otherwise do something reasonable...
      return 'UNKNOWN';
    }
  }

  render() {
    if (this.state.errorInfo) {
      return (
        <React.Fragment>
          <h1>That's an error you've got there.</h1>
          <h2>Looks like the problem is in your {this.getComponentNameFromStack()} component.</h2>
          <h4>(But check out the details for the exact problem).</h4>
          <details>
            {this.state.error && this.state.error.toString()}
            <br />
            {this.state.errorInfo.componentStack}
          </details>
        </ React.Fragment>
      );
    }
    return this.props.children;
  }
}

export default styled(ErrorBoundary)`
  details {
    whiteSpace: 'pre-wrap';
  }
`;