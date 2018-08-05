import "dc/dc.css";
import "bootstrap/dist/css/bootstrap.css";
import * as React from "react";
import styled from "styled-components";
import { withRouter } from "react-router";
import {
  ChartContainer,
  PieChart,
  RowChart,
  BubbleChart,
  DataTable,
  DataCount,
  BarChart,
  LineChart
} from "dc-react";
import * as crossfilter from "crossfilter2";
import * as d3 from "d3";
import * as dc from "dc";

import { EmptyRouteAwareComponentProps } from "../util";
import ResetFilters from './ResetFilters';

interface Props {
  className?: string;
}

const dateFormat = d3.time.format("%m/%d/%Y");
const numberFormat = d3.format(".2f");
const weekdayLabels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

class CrossfilterContext {
  public data;
  public crossfilter;
  public groupAll;
  public dateDimension;
  public yearlyDimension;
  public dayOfWeekDimension;
  public dayOfWeekGroup;
  public gainOrLossDimension;
  public gainOrLossGroup;
  public quarterDimension;
  public quarterGroup;
  public fluctuationDimension;
  public fluctuationGroup;
  public moveMonthsDimension;
  public moveMonthsGroup;
  public _indexAvgByMonthGroup;
  public _yearlyPerformanceGroup;

  constructor(data) {
    this.data = data;
    this.crossfilter = crossfilter(data);
    this.groupAll = this.crossfilter.groupAll();
    this.dateDimension = this.crossfilter.dimension(d => d.dd);
    this.yearlyDimension = this.crossfilter.dimension(d =>
      d3.time.year(d.dd).getFullYear()
    );
    this.dayOfWeekDimension = this.crossfilter.dimension(d => {
      var day = d.dd.getDay();
      return `${day}.${weekdayLabels[day]}`;
    });
    this.dayOfWeekGroup = this.dayOfWeekDimension.group();
    this.gainOrLossDimension = this.crossfilter.dimension(
      d => (d.open > d.close ? "Loss" : "Gain")
    );
    this.gainOrLossGroup = this.gainOrLossDimension.group();

    this.quarterDimension = this.crossfilter.dimension(d => {
      let quarter = Math.floor(d.dd.getMonth() / 3) + 1;
      return `Q${quarter}`;
    });
    this.quarterGroup = this.quarterDimension.group().reduceSum(d => d.volume);

    this.fluctuationDimension = this.crossfilter.dimension(d =>
      Math.round(((d.close - d.open) / d.open) * 100)
    );
    this.fluctuationGroup = this.fluctuationDimension.group();

    this.moveMonthsDimension = this.crossfilter.dimension(d => d.month);
    this.moveMonthsGroup = this.moveMonthsDimension
      .group()
      .reduceSum(d => Math.abs(d.close - d.open));
  }

  get indexAvgByMonthGroup() {
    if (this._indexAvgByMonthGroup) {
      return this._indexAvgByMonthGroup;
    }

    this._indexAvgByMonthGroup = this.moveMonthsDimension.group().reduce(
      (p, v) => {
        ++p.days;
        p.total += (v.open + v.close) / 2;
        p.avg = Math.round(p.total / p.days);
        return p;
      },
      (p, v) => {
        --p.days;
        p.total -= (v.open + v.close) / 2;
        p.avg = p.days ? Math.round(p.total / p.days) : 0;
        return p;
      },
      () => {
        return { days: 0, total: 0, avg: 0 };
      }
    );

    return this._indexAvgByMonthGroup;
  }

  get yearlyPerformanceGroup() {
    if (this._yearlyPerformanceGroup) {
      return this._yearlyPerformanceGroup;
    }

    this._yearlyPerformanceGroup = this.yearlyDimension.group().reduce(
      (p, v) => {
        ++p.count;
        p.absGain += v.close - v.open;
        p.fluctuation += Math.abs(v.close - v.open);
        p.sumIndex += (v.open + v.close) / 2;
        p.avgIndex = p.sumIndex / p.count;
        p.percentageGain = p.avgIndex ? (p.absGain / p.avgIndex) * 100 : 0;
        p.fluctuationPercentage = p.avgIndex
          ? (p.fluctuation / p.avgIndex) * 100
          : 0;
        return p;
      },
      (p, v) => {
        --p.count;
        p.absGain -= v.close - v.open;
        p.fluctuation -= Math.abs(v.close - v.open);
        p.sumIndex -= (v.open + v.close) / 2;
        p.avgIndex = p.count ? p.sumIndex / p.count : 0;
        p.percentageGain = p.avgIndex ? (p.absGain / p.avgIndex) * 100 : 0;
        p.fluctuationPercentage = p.avgIndex
          ? (p.fluctuation / p.avgIndex) * 100
          : 0;
        return p;
      },
      () => {
        return {
          count: 0,
          absGain: 0,
          fluctuation: 0,
          fluctuationPercentage: 0,
          sumIndex: 0,
          avgIndex: 0,
          percentageGain: 0
        };
      }
    );

    return this._yearlyPerformanceGroup;
  }
}

// Home Page Content
const Home: React.SFC<EmptyRouteAwareComponentProps<Props>> = props => {
  let crossfilterContext = null;
  function getCrossfilterContext(callback) {
    if (!crossfilterContext) {
      const records = require("../assets/data/d1.json");
      const vals = records.map(d => {
        return {
          dd: dateFormat.parse(d.date),
          month: d3.time.month(dateFormat.parse(d.date)),
          close: +d.close,
          open: +d.open,
          date: d.date,
          high: d.high,
          low: d.low,
          volume: d.volume,
          oi: d.oi
        };
      });
      crossfilterContext = new CrossfilterContext(vals);
    }
    if (!callback) {
      return crossfilterContext;
    }
    callback(crossfilterContext);
  }

  return (
    <div className={props.className}>
     <ChartContainer className="container" crossfilterContext={getCrossfilterContext}>
        <h1>Nasdaq 100 Index 1985/11/01-2012/06/29</h1>
        <DataCount
          dimension={ctx => ctx.crossfilter}
          group={ctx => ctx.groupAll}
        />
        &nbsp;papers selected (<ResetFilters />)
        <BubbleChart className="row"
          dimension={ctx => ctx.yearlyDimension}
          group={ctx => ctx.yearlyPerformanceGroup}
          width={990} height={250}
          colorAccessor={d => d.value.absGain}
          keyAccessor={p => p.value.absGain}
          valueAccessor={p => p.value.percentageGain}
          radiusValueAccessor={p => p.value.fluctuationPercentage}
          x={d3.scale.linear().domain([-2500, 2500])}
          y={d3.scale.linear().domain([-100, 100])}
          r={d3.scale.linear().domain([0, 4000])}
          colorDomain={[-500, 500]}
        />
        <div className="row">
          <PieChart
            dimension={ctx => ctx.gainOrLossDimension}
            group={ctx => ctx.gainOrLossGroup}
            width={180} height={180}
            radius={80}
            label={(d) => {
              let percent = numberFormat(d.value / crossfilterContext.groupAll.value() * 100);
              return `${d.key} (${percent}%)`;
            }}
          />
          <PieChart
            dimension={ctx => ctx.quarterDimension}
            group={ctx => ctx.quarterGroup}
            width={180} height={180}
            radius={80} innerRadius={30}
          />
          <RowChart
            dimension={ctx => ctx.dayOfWeekDimension}
            group={ctx => ctx.dayOfWeekGroup}
            width={180} height={180}
            elasticX={true}
            margins={{top: 20, left: 10, right: 10, bottom: 20}}
            label={d => d.key.split('.')[1]}
            title={d => d.value}
            xAxis={axis => axis.ticks(4)}
          />
          <BarChart
            dimension={ctx => ctx.fluctuationDimension}
            group={ctx => ctx.fluctuationGroup}
            width={420}
            height={180}
            elasticY={true}
            centerBar={true}
            gap={1}
            round={dc.round.floor}
            alwaysUseRounding={true}
            x={d3.scale.linear().domain([-25, 25])}
            renderHorizontalGridLines={true}
          />
        </div>
        <LineChart
          dimension={ctx => ctx.moveMonthsDimension}
          group={ctx => [ctx.indexAvgByMonthGroup, 'Monthly Index Average']}
          renderArea={true}
          width={990}
          height={200}
          transitionDuration={1000}
          margins={{top: 30, right: 50, bottom: 25, left: 40}}
          mouseZoomable={true}
          x={d3.time.scale().domain([new Date(1985, 0, 1), new Date(2012, 11, 31)])}
          round={d3.time.month.round}
          xUnits={d3.time.months}
          elasticY={true}
          renderHorizontalGridLines={true}
          legend={dc.legend().x(800).y(10).itemHeight(13).gap(5)}
          brushOn={false}
          valueAccessor={d => d.value.avg}
          title={(d) => {
            let value = d.value.avg ? d.value.avg : d.value;
            if (isNaN(value)) {
              value = 0;
            }
            return `${dateFormat(d.key)}\n${numberFormat(value)}`;
          }}
          stack={ctx => [ctx.moveMonthsGroup, 'Monthly Index Move', (d) => { return d.value; }]}
        />
        <DataTable
          className="table table-hover"
          dimension={ctx => ctx.dateDimension}
          group={d => `${d.dd.getFullYear()}/${d.dd.getMonth()+1}`}
          columns={[
            'date', 'open', 'close', 'volume'
          ]}
        />
        <div className="clearfix" />
      </ChartContainer>
    </div>
  );
};

export default styled(withRouter(Home))`
  font-size: 20px;

  .row {
    display: block;
  }
`;
