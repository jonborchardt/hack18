import * as React from "react";
import styled from "styled-components";
import * as dc from "dc";

interface Props {
  className?: string;
}

const resetAll = (event) => {
  dc.filterAll();
  dc.redrawAll();
  event.stopPropagation()
};

const ResetFilters : React.SFC <Props> = props => {
  return (
    <a href="javascript:;" onClick={resetAll}>
      <span>reset filters</span>
    </a>
  );
};

export default styled(ResetFilters)`
`;
