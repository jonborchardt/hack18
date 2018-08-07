import 'dc/dc.css';
import 'bootstrap/dist/css/bootstrap.css';
import * as React from 'react';
import styled from 'styled-components';
import { withRouter } from 'react-router';
import {
  ChartContainer,
  PieChart,
  RowChart,
  BubbleChart,
  DataTable,
  DataCount,
  BarChart,
  LineChart
} from 'dc-react';
import * as crossfilter from 'crossfilter2';
import * as d3 from 'd3';
import * as dc from 'dc';

import { EmptyRouteAwareComponentProps } from '../util';
import ResetFilters from './ResetFilters';
import {Record} from '../types';

interface Props {
  className?: string;
}

class RecordCrossfilterContext {
  public data;
  public crossfilter;
  public groupAll;
  public bubbleYearDimension;
  public genderYearDimension;
  public femaleYearGroup;
  public maleYearGroup;
  public barYearDimension;
  public barYearGroup;
  public genderDimension;
  public genderGroup;
  public venueDimension;
  public venueGroup;
  public inCitationsDimension;
  public inCitationsGroup;
  public outCitationsDimension;
  public outCitationsGroup;

  public _yearlyPerformanceGroup;

  constructor(data: Record[]) {
    this.data = data;
    this.crossfilter = crossfilter(data);
    this.groupAll = this.crossfilter.groupAll();
    this.bubbleYearDimension = this.crossfilter.dimension(d => 
      d.year?d.year.toString(): 'unknown'
    );
    this.genderYearDimension = this.crossfilter.dimension(d => 
      d.year?d.year.toString(): 'unknown'
    );
    this.femaleYearGroup = this.genderYearDimension.group().reduceSum(d=>d.gender==='female' ? 1 : 0);
    this.maleYearGroup = this.genderYearDimension.group().reduceSum(d=>d.gender==='male' ? 1 : 0);
    this.barYearDimension = this.crossfilter.dimension(d => 
      d.year?d.year.toString(): 'unknown'
    );
    this.barYearGroup = this.barYearDimension.group();
    this.genderDimension = this.crossfilter.dimension(d => d.gender);
    this.genderGroup = this.genderDimension.group();
    this.venueDimension = this.crossfilter.dimension(d => d.venue);
    this.venueGroup = this.venueDimension.group();
    this.inCitationsDimension = this.crossfilter.dimension(d => d.inCitationsCount);
    this.inCitationsGroup = this.inCitationsDimension.group();
    this.outCitationsDimension = this.crossfilter.dimension(d => d.outCitationsCount);
    this.outCitationsGroup = this.outCitationsDimension.group();
  }

  get yearlyPerformanceGroup() {
    if (this._yearlyPerformanceGroup) {
      return this._yearlyPerformanceGroup;
    }

    this._yearlyPerformanceGroup = this.bubbleYearDimension.group().reduce(
      (p, v) => {
        ++p.count;
        p.year = v.year;
        p.inCitations += v.inCitationsCount;
        p.outCitations +=  v.outCitationsCount;
        p.genderIndex += (v.gender==='female'?1:-1);
        return p;
      },
      (p, v) => {
        --p.count;
        p.inCitations -= v.inCitationsCount;
        p.outCitations -=  v.outCitationsCount;
        p.genderIndex -= (v.gender==='female'?1:-1);
        return p;
      },
      () => {
        return {
          year: 0,
          count: 0,
          inCitations: 0,
          outCitations: 0,
          genderIndex: 0
        };
      }
    );

    return this._yearlyPerformanceGroup;
  }
}

function download(content, fileName, contentType) {
  var a = document.createElement('a');
  var file = new Blob([content], {type: contentType});
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
}

// Home Page Content
const Home: React.SFC<EmptyRouteAwareComponentProps<Props>> = props => {
  let crossfilterContext = null;
  function getCrossfilterContext(callback) {
    if (!crossfilterContext) {
      const convertData = false;
      if(convertData) {
        const ox: Record[] = [];
        const recordsx = require('../assets/data/sample-S2-records.txt');
        recordsx.split('\n').forEach(s => {
          if(s && s.year){
            const j = JSON.parse(s);
              j.authors.forEach((author, aindex) => {
              ox.push({
                id: (j.id+(aindex>0?'_aindex':'')),
                author: author.name,
                gender: (Math.random()>0.5?'female':'male'),
                year: j.year,
                title: j.title || 'Unknown',
                venue: j.venue || j.journalName || 'Unknown',
                inCitationsCount: (j.inCitations?j.inCitations.length:0),
                outCitationsCount: (j.outCitations?j.outCitations.length:0)
              });
            });
          }
        });
        download(JSON.stringify(ox), 'records.json', 'text/plain');
      }

      const vals = require('../assets/data/records.json');
      const start = Date.now();
      console.log('start');
      crossfilterContext = new RecordCrossfilterContext(vals);
      console.log('end 2 ', (Date.now()-start)/1000);
    }
    if (!callback) {
      return crossfilterContext;
    }
    callback(crossfilterContext);
  }

  return (
    <div className={props.className}>
      <ChartContainer className="container" crossfilterContext={getCrossfilterContext}>
        <Title>
          <h1>Semantic Scholar Records</h1>
          <DataCount
            dimension={ctx => ctx.crossfilter}
            group={ctx => ctx.groupAll}
          />
          &nbsp;papers selected (<ResetFilters />)
          </Title>
          <Filters>
            <LeftFilters>
              <Chart>
                <ChartTitle>Gender</ChartTitle>
                <PieChart
                  dimension={ctx => ctx.genderDimension}
                  group={ctx => ctx.genderGroup}
                  width={180} height={180}
                  radius={80} innerRadius={30}
                />
              </Chart>
              <Chart>
                <ChartTitle>Venue</ChartTitle>
                <RowChart
                  dimension={ctx => ctx.venueDimension}
                  group={ctx => ctx.venueGroup}
                  width={180} height={1800}
                  elasticX={true}
                  margins={{top: 20, left: 10, right: 10, bottom: 20}}
                  label={d => d.key}
                  title={d => d.value}
                  xAxis={axis => axis.ticks(4)}
                />
              </Chart>
            </LeftFilters>
            <RightFilters>
              <ChartTitle>Gender Difference By Year</ChartTitle>
              <BubbleChart className="row"
                dimension={ctx => ctx.bubbleYearDimension}
                group={ctx => ctx.yearlyPerformanceGroup}
                width={990} height={250}
                colorAccessor={d => d.value.outCitations}
                keyAccessor={p => p.value.year}
                valueAccessor={p => p.value.genderIndex}
                radiusValueAccessor={p => p.value.count}
                title={d => ''}
                x={d3.scale.linear().domain([1944, 2018])}
                y={d3.scale.linear().domain([-15, 15])}
                r={d3.scale.linear().domain([0, 300])}
                colorDomain={[0, 50]}
              />
              <RightRowFilters>
                <Chart>
                  <ChartTitle>Year</ChartTitle>
                  <BarChart
                    dimension={ctx => ctx.barYearDimension}
                    group={ctx => ctx.barYearGroup}
                    width={320}
                    height={180}
                    elasticY={true}
                    centerBar={true}
                    gap={1}
                    round={dc.round.floor}
                    alwaysUseRounding={true}
                    x={d3.scale.linear().domain([1944, 2018])}
                    renderHorizontalGridLines={true}
                  />
                </Chart>
                <Chart>
                  <ChartTitle>In Citations</ChartTitle>
                  <BarChart
                    dimension={ctx => ctx.inCitationsDimension}
                    group={ctx => ctx.inCitationsGroup}
                    width={320}
                    height={180}
                    elasticY={true}
                    centerBar={true}
                    gap={1}
                    round={dc.round.floor}
                    alwaysUseRounding={true}
                    x={d3.scale.linear().domain([0, 60])}
                    renderHorizontalGridLines={true}
                  />
                </Chart>
                <Chart>
                  <ChartTitle>Out Citations</ChartTitle>
                  <BarChart
                    dimension={ctx => ctx.outCitationsDimension}
                    group={ctx => ctx.outCitationsGroup}
                    width={320}
                    height={180}
                    elasticY={true}
                    centerBar={true}
                    gap={1}
                    round={dc.round.floor}
                    alwaysUseRounding={true}
                    x={d3.scale.linear().domain([0, 60])}
                    renderHorizontalGridLines={true}
                  />
                </Chart>
              </RightRowFilters>
              <Chart>
                <ChartTitle>Total Records By Year</ChartTitle>
                <LineChart
                  dimension={ctx => ctx.genderYearDimension}
                  group={ctx => [ctx.femaleYearGroup, 'Female']}
                  renderArea={true}
                  width={990}
                  height={200}
                  transitionDuration={200}
                  margins={{top: 30, right: 50, bottom: 25, left: 40}}
                  mouseZoomable={true}
                  x={d3.scale.linear().domain([1944, 2018])}
                  round={d3.time.month.round}
                  xUnits={d3.time.months}
                  elasticY={true}
                  renderHorizontalGridLines={true}
                  legend={dc.legend().x(800).y(10).itemHeight(13).gap(5)}
                  brushOn={false}
                  valueAccessor={d => d.value}
                  stack={ctx => [ctx.maleYearGroup, 'Male', (d) => { return d.value; }]}
                />
              </Chart>
            </RightFilters>
        </Filters>
    </ChartContainer>
  </div>
  );
};

const Chart = styled.div`
  margin: 10px;
  display: flex;
  flex-direction: column;
`;

const ChartTitle = styled.div`
  margin-left: 35px;
  font-weight: bold;
`;

const Title = styled.div`
  margin-bottom: 30px;
`;

const Filters = styled.div`
  display: flex;
`;

const LeftFilters = styled.div`
  flex-direction: column;
`;

const RightFilters = styled.div`
  display: flex;
  flex-direction: column;
`;

const RightRowFilters = styled.div`
  display: flex;
`;

export default styled(withRouter(Home))`
display: flex;
font-size: 20px;

.row {
  display: block;
}

.dc-chart {
  g.row text {
    fill: darkslategray;
  }
  text {
    font-family: "open sans";
  }
  .title,
  .filter {
    margin-left: 20px;
    margin-right: 6px;
  }
  .filter {
    font-size: 10px;
    display: block;
    padding-bottom: 5px;
  }
  .reset-btn {
    display: inline-block;
    padding-bottom: 6px;
  }
  a .reset {
    margin-right: 5px;
    font-size: 11px;
    font-weight: normal;
    -webkit-border-radius: 7px;
    -moz-border-radius: 7px;
    border-radius: 7px;
  }
  .axis {
    .tick {
      text {
        // make axis tick text lighter
        fill: #D2D2D2;
        font-size: 10px;
        font: 10px sans-serif;
        /* Makes it so the user can't accidentally click and select text that is meant as a label only */
        -webkit-user-select: none;
        /* Chrome/Safari */
        -moz-user-select: none;
        /* Firefox */
        -ms-user-select: none;
        /* IE10 */
        -o-user-select: none;
        user-select: none;
        pointer-events: none;
      }
      line {
        stroke: #D2D2D2;
        shape-rendering: crispEdges;
      }
      line.grid-line {
        // make grid lighter
        stroke: #ccc;
      }
    }
    path.domain {
      stroke: #D2D2D2;
      fill: none;
      shape-rendering: crispEdges;
    }
  }
}
`;
