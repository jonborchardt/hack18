import * as React from 'react';
import styled from 'styled-components';

import ErrorBoundary from './ErrorBoundary';

interface Props {
  children: JSX.Element[] | React.ReactNode;
  className?: string;
}

// outer base page for all pages
const Page: React.SFC<Props> = (props) => {
  return (
    <ErrorBoundary>
      <section className={props.className}>
        {props.children}
      </section>
    </ErrorBoundary>
  );
};

export default styled(Page)`
  max-width: ${(props) => props.theme.dimensions.maxContentWidth};
  margin: 0 auto;
`;