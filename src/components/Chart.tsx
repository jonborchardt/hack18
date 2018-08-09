
import * as React from 'react';
import styled from 'styled-components';

interface Props {
  className?: string;
  title: string;
  subTitle?: string;
  children: JSX.Element
}

const Chart: React.SFC<Props> = props => {
  return (
    <div className={props.className}>
      <ChartTitle>{props.title}</ChartTitle>
      <ChartSubTitle>{props.subTitle}</ChartSubTitle>
      {props.children}
    </div>
  );
};

const ChartTitle = styled.div`
  font-size: 13px;
  margin-left: 35px;
  font-weight: bold;
`;

const ChartSubTitle = styled.div`
  margin-left: 35px;
  font-size: 11px;
`;

export default styled(Chart)`
  margin: 10px;
  display: flex;
  flex-direction: column;
`;
