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
import { Record, Gender, Author, GenderCount } from '../types';
import Chart from './Chart';

interface Props {
  className?: string;
}

class RecordCrossfilterContext {
  All = 'All';

  public data;
  public crossfilter;
  public groupAll;

  public bubbleYearDimension;
  public genderYearDimension;
  public uniqueNameYearDimension;
  public percentFemaleDimension;
  public venueDimension;
  public bubbleVenueDimension;
  public inCitationsDimensions;
  public outCitationsDimensions;
  public firstFemaleAuthorPositionDimension;

  public femalePercentYearGroup;
  public malePercentYearGroup;
  public percentFemaleGroup;
  public venueGroup;
  public inCitationsGroups;
  public outCitationsGroups;
  public firstFemaleAuthorPositionGroup;

  public _citationsGroup;
  public _bubbleYearGroup;
  public _bubbleVenueGroup;
  public _yearUniqueNameGroup;

  constructor(data: Record[]) {
    this.data = data;
    this.crossfilter = crossfilter(data);
    this.groupAll = this.crossfilter.groupAll();

    this.bubbleYearDimension = this.crossfilter.dimension((d: Record) => d.year || 0);
    this.genderYearDimension = this.crossfilter.dimension((d: Record) => d.year || 0);
    this.uniqueNameYearDimension = this.crossfilter.dimension((d: Record) => d.year || 0);
    this.percentFemaleDimension = this.crossfilter.dimension((d: Record) => d.percentFemaleAuthor || 0);
    this.venueDimension = this.crossfilter.dimension((d: Record) => d.venue);
    this.bubbleVenueDimension = this.crossfilter.dimension((d: Record) => d.venue);
    this.inCitationsDimensions = [];
    this.inCitationsDimensions[Gender.female] = this.crossfilter.dimension((d: Record) => Math.min(30, d.inCitationsCounts[Gender.female] || 0));
    this.inCitationsDimensions[Gender.male] = this.crossfilter.dimension((d: Record) => Math.min(30, d.inCitationsCounts[Gender.male] || 0));
    this.outCitationsDimensions = [];
    this.outCitationsDimensions[Gender.female] = this.crossfilter.dimension((d: Record) => Math.min(30, d.outCitationsCounts[Gender.female] || 0));
    this.outCitationsDimensions[Gender.male] = this.crossfilter.dimension((d: Record) => Math.min(30, d.outCitationsCounts[Gender.male] || 0));
    this.firstFemaleAuthorPositionDimension = this.crossfilter.dimension((d: Record) => d.firstFemalePosition);

    this.femalePercentYearGroup = this.genderYearDimension.group().reduceSum((d: Record) => d.percentFemaleAuthor || 0);
    this.malePercentYearGroup = this.genderYearDimension.group().reduceSum((d: Record) => 1 - d.percentFemaleAuthor || 0);
    this.percentFemaleGroup = this.percentFemaleDimension.group((val) => { return Math.round((val * 6)) / 6; });
    this.venueGroup = this.venueDimension.group();
    this.inCitationsGroups = [];
    this.inCitationsGroups[Gender.female] = this.inCitationsDimensions[Gender.female].group();
    this.inCitationsGroups[Gender.male] = this.inCitationsDimensions[Gender.male].group();
    this.outCitationsGroups = [];
    this.outCitationsGroups[Gender.female] = this.outCitationsDimensions[Gender.female].group();
    this.outCitationsGroups[Gender.male] = this.outCitationsDimensions[Gender.male].group();
    this.firstFemaleAuthorPositionGroup = this.firstFemaleAuthorPositionDimension.group();
  }

  get bubbleYearGroup() {
    if (this._bubbleYearGroup) {
      return this._bubbleYearGroup;
    }
    this._bubbleYearGroup = this.bubbleYearDimension.group().reduce(
      (p, v: Record) => {
        ++p.count;
        p.year = v.year;
        p.citationIndex += (v.percentOutCiteFemale || 0);
        p.genderIndex += (v.percentFemaleAuthor || 0);
        return p;
      },
      (p, v) => {
        --p.count;
        p.citationIndex -= (v.percentOutCiteFemale || 0);
        p.genderIndex -= (v.percentFemaleAuthor || 0);
        return p;
      },
      () => {
        return {
          year: '',
          count: 0,
          citationIndex: 0,
          genderIndex: 0
        };
      }
    );
    return this._bubbleYearGroup;
  }

  get bubbleVenueGroup() {
    if (this._bubbleVenueGroup) {
      return this._bubbleVenueGroup;
    }
    this._bubbleVenueGroup = this.bubbleVenueDimension.group().reduce(
      (p, v: Record) => {
        ++p.count;
        p.year = v.year;
        p.venue = v.venue;
        p.citationIndex += (v.percentOutCiteFemale || 0);
        p.genderIndex += (v.percentFemaleAuthor || 0);
        return p;
      },
      (p, v) => {
        --p.count;
        p.citationIndex -= (v.percentOutCiteFemale || 0);
        p.genderIndex -= (v.percentFemaleAuthor || 0);
        return p;
      },
      () => {
        return {
          venue: '',
          year: '',
          count: 0,
          citationIndex: 0,
          genderIndex: 0
        };
      }
    );
    return this._bubbleVenueGroup;
  }

  get yearUniqueNameGroup() {
    if (this._yearUniqueNameGroup) {
      return this._yearUniqueNameGroup;
    }
    this._yearUniqueNameGroup = this.uniqueNameYearDimension.group().reduce(
      (p, v: Record) => {
        v.authors.forEach(a => {
          if (!p.uniqueNamesByGender[a.gender][a.name]) {
            p.uniqueNamesByGender[a.gender][a.name] = 1;
          } else {
            p.uniqueNamesByGender[a.gender][a.name]++;
          }
        })

        return p;
      },
      (p, v: Record) => {
        v.authors.forEach(a => {
          p.uniqueNamesByGender[a.gender][a.name]--;
        })
        return p;
      },
      () => {
        return {
          uniqueNamesByGender: { 'male': {}, 'female': {} }
        };
      }
    );
    return this._yearUniqueNameGroup;
  }
}

interface State {
  loadedData: Record[];
  getCrossfilterContextFunc: any;
  key: string;
}

// Home Page Content
class Home extends React.Component<EmptyRouteAwareComponentProps<Props>, State> {
  constructor(props: EmptyRouteAwareComponentProps<Props>) {
    super(props);

    const vals = require('../assets/data/records.json');
    this.state = {
      loadedData: [],
      getCrossfilterContextFunc: undefined,
      key: "unloaded"
    }

    this.saveData = this.saveData.bind(this);
    this.parseFile = this.parseFile.bind(this);
    this.loadLines = this.loadLines.bind(this);
    this.loadCrossfilter = this.loadCrossfilter.bind(this);
  }

  download(content, fileName, contentType) {
    var a = document.createElement('a');
    var file = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
  }

  saveData() {
    this.download(JSON.stringify(this.state.loadedData), 'records.json', 'text/plain');
  }

  parseFile(file) {
    var fileSize = file.size;
    var chunkSize = 1024 * 1024 * 8;
    var offset = 0;
    var readBlock = null;
    var _this = this;

    let count = 10000000;

    var onLoadHandler = function (evt) {
      if (evt.currentTarget.error == null) {
        const lines = (event.currentTarget as any).result;
        //const start = lines.indexOf("{\"entities"); // todo: this is a huge hack
        const start = lines.indexOf("{\"outCitati"); // todo: this is a huge hack
        const lastReturn = lines.lastIndexOf('\n');
        offset += lastReturn;

        if (start > -1 && lastReturn > -1 && count-- > 0) {
          _this.loadLines(lines.substring(start, lastReturn));
        } else {
          //_this.saveData();
          _this.loadCrossfilter(_this.state.loadedData);
          return;
        }
      } else {
        console.log(evt.currentTarget.error);
        return;
      }
      if (offset >= fileSize) {
        //_this.saveData();
        _this.loadCrossfilter(_this.state.loadedData);
        return;
      }

      readBlock(offset, chunkSize, file);
    }

    readBlock = function (_offset, length, _file) {
      var r = new FileReader();
      var blob = _file.slice(_offset, length + _offset);
      r.onload = onLoadHandler;
      r.readAsText(blob);
    }

    readBlock(offset, chunkSize, file);
  }

  loadCrossfilter(v) {
    this.setState({
      key: "loaded",
      getCrossfilterContextFunc: (callback?) => { callback(new RecordCrossfilterContext(v)); }
    })
  }

  venues = ['ArXiv',
    'IEICE Transactions',
    'Applied Mathematics and Computation',
    'HCI',
    'INTERSPEECH',
    'Discrete Mathematics',
    'European Journal of Operational Research',
    'ICASSP',
    'Neurocomputing',
    'Expert Syst. Appl.',
    'Commun. ACM',
    'Theor. Comput. Sci.',
    'Automatica',
    'Inf. Sci.',
    'ICRA',
    'IEEE Trans. Information Theory',
    'IJCAI',
    'AMCIS',
    'RFC',
    'Pattern Recognition',
    'IEEE Communications Letters',
    'ISCAS',
    'NIPS',
    'AAAI',
    'Inf. Process. Lett.',
    'IEEE Transactions on Industrial Electronics',
    'IEEE Transactions on Wireless Communications',
    'ICIP',
    'CHI Extended Abstracts',
    'SAC'];

  loadLines(lines: string) {
    let { loadedData } = this.state;

    lines.split('\n').forEach((s, i) => {
      if (s) { //} && ((i % 10) === 0)) {
        const j = JSON.parse(s);
        if (j.year && j.authors && j.venue && this.venues.indexOf(j.venue) > -1) {
          let percentOutCiteFemale = j.outCitationsCount.female / (j.outCitationsCount.female + j.outCitationsCount.male + j.outCitationsCount.unknown);
          loadedData.push({
            authors: j.authors,
            year: j.year,
            venue: j.venue,
            inCitationsCounts: j.inCitationsCount,
            outCitationsCounts: j.outCitationsCount,
            // augmented
            percentFemaleAuthor: j.authors.filter(a => a.gender === Gender.female).length / j.authors.length,
            firstFemalePosition: j.authors.findIndex(a => a.gender === Gender.female) + 1,
            percentOutCiteFemale: percentOutCiteFemale
          });
        }
      }
    });

    this.setState({ loadedData }, () => console.log(this.state.loadedData.length));
  }

  yearScale = d3.scale.linear().domain([1944, 2018]);

  render() {
    return (
      <div className={this.props.className} >
        {this.state.key !== "loaded" ? <input type="file" onChange={(e) => this.parseFile(e.target.files[0])} /> : null}
        {this.state.key === "loaded" ? (<ChartContainer className="container" crossfilterContext={this.state.getCrossfilterContextFunc}>
          <Title>
            <h1>Top 30 CS Venues from Semantic Scholar Records</h1>
            <DataCount
              dimension={ctx => ctx.crossfilter}
              group={ctx => ctx.groupAll}
            />
            &nbsp;papers selected (<ResetFilters />)
          </Title>
          <Filters>
            <LeftFilters>
              <Chart title="Percent Female Author">
                <PieChart
                  dimension={ctx => ctx.percentFemaleDimension}
                  group={ctx => ctx.percentFemaleGroup}
                  width={180} height={180}
                  radius={80} innerRadius={30}
                  label={d => `%${Math.round(d.key * 100)}`}
                />
              </Chart>
              <Chart title="First Female Author Position">
                <PieChart
                  dimension={ctx => ctx.firstFemaleAuthorPositionDimension}
                  group={ctx => ctx.firstFemaleAuthorPositionGroup}
                  width={180} height={180}
                  radius={80} innerRadius={30}
                />
              </Chart>
              <Chart title="Venue">
                <RowChart
                  dimension={ctx => ctx.venueDimension}
                  group={ctx => ctx.venueGroup}
                  width={180} height={700}
                  elasticX={true}
                  margins={{ top: 20, left: 10, right: 10, bottom: 20 }}
                  label={d => d.key}
                  title={d => d.value}
                  xAxis={axis => axis.ticks(4)}
                />
              </Chart>
            </LeftFilters>
            <RightFilters>
              <RightRowFilters2>
                <Chart
                  title="Gender And Citations By Year"
                  subTitle="Color: year, Size: count, x: Percent of women in authors, y: Percent of out citations to other women authors">
                  <BubbleChart className="row"
                    dimension={ctx => ctx.bubbleYearDimension}
                    group={ctx => ctx.bubbleYearGroup}
                    width={460} height={350}
                    colorAccessor={p => p.value.year}
                    keyAccessor={p => p.value.citationIndex / (p.value.count || 1)}
                    valueAccessor={p => p.value.genderIndex / (p.value.count || 1)}
                    radiusValueAccessor={p => p.value.count}
                    title={d => ''}
                    x={d3.scale.linear().domain([0, 1])}
                    y={d3.scale.linear().domain([0, 1])}
                    r={d3.scale.linear().domain([0, 200000])}
                  />
                </Chart>
                <Chart
                  title="Gender And Citations By Venue"
                  subTitle="Color: venue, Size: count, x: Percent of women in authors, y: Percent of out citations to other women authors">
                  <BubbleChart className="row"
                    dimension={ctx => ctx.bubbleVenueDimension}
                    group={ctx => ctx.bubbleVenueGroup}
                    width={460} height={350}
                    colorAccessor={p => this.venues.indexOf(p.value.venue)}
                    keyAccessor={p => p.value.citationIndex / (p.value.count || 1)}
                    valueAccessor={p => p.value.genderIndex / (p.value.count || 1)}
                    radiusValueAccessor={p => p.value.count}
                    title={d => ''}
                    x={d3.scale.linear().domain([0, 1])}
                    y={d3.scale.linear().domain([0, 1])}
                    r={d3.scale.linear().domain([0, 200000])}
                  />
                </Chart>
              </RightRowFilters2>
              <Chart
                title="Unique Names per Year"
                subTitle="Are the number of female authors increasing?">
                <LineChart
                  dimension={ctx => ctx.uniqueNameYearDimension}
                  group={ctx => [ctx.yearUniqueNameGroup, 'Female']}
                  renderArea={true}
                  width={990}
                  height={220}
                  transitionDuration={200}
                  margins={{ top: 30, right: 50, bottom: 25, left: 40 }}
                  mouseZoomable={false}
                  x={this.yearScale}
                  elasticY={true}
                  renderHorizontalGridLines={true}
                  legend={dc.legend().x(800).y(10).itemHeight(13).gap(5)}
                  brushOn={true}
                  valueAccessor={d => {
                    const obj = d.value.uniqueNamesByGender[Gender.female];
                    const set = obj ? Object.keys(obj).map(key => obj[key]).filter(v => v > 0) : [];
                    return set.length;
                  }}
                  stack={ctx => [ctx.yearUniqueNameGroup, 'Male', (d) => {
                    const obj = d.value.uniqueNamesByGender[Gender.male];
                    const set = obj ? Object.keys(obj).map(key => obj[key]).filter(v => v > 0) : [];
                    return set.length;
                  }]}
                />
              </Chart>
              <Chart
                title="Papers per Year"
                subTitle="How many papers are partially or fully authored by women?">
                <LineChart
                  dimension={ctx => ctx.genderYearDimension}
                  group={ctx => [ctx.femalePercentYearGroup, 'Female Contribution']}
                  renderArea={true}
                  width={990}
                  height={220}
                  transitionDuration={200}
                  margins={{ top: 30, right: 50, bottom: 25, left: 40 }}
                  mouseZoomable={false}
                  x={this.yearScale}
                  elasticY={true}
                  renderHorizontalGridLines={true}
                  legend={dc.legend().x(800).y(10).itemHeight(13).gap(5)}
                  brushOn={true}
                  valueAccessor={d => d.value}
                  stack={ctx => [ctx.malePercentYearGroup, 'Male Contribution', (d) => { return d.value; }]}
                />
              </Chart>
              <RightRowFilters>
                <Chart title="In Female Citations">
                  <BarChart
                    dimension={ctx => ctx.inCitationsDimensions[Gender.female]}
                    group={ctx => ctx.inCitationsGroups[Gender.female]}
                    width={230}
                    height={160}
                    elasticY={true}
                    centerBar={true}
                    gap={1}
                    round={dc.round.floor}
                    alwaysUseRounding={true}
                    x={d3.scale.linear().domain([1, 30])}
                    renderHorizontalGridLines={true}
                  />
                </Chart>
                <Chart title="In Male Citations">
                  <BarChart
                    dimension={ctx => ctx.inCitationsDimensions[Gender.male]}
                    group={ctx => ctx.inCitationsGroups[Gender.male]}
                    width={230}
                    height={160}
                    elasticY={true}
                    centerBar={true}
                    gap={1}
                    round={dc.round.floor}
                    alwaysUseRounding={true}
                    x={d3.scale.linear().domain([1, 30])}
                    renderHorizontalGridLines={true}
                  />
                </Chart>
                <Chart title="Out Female Citations">
                  <BarChart
                    dimension={ctx => ctx.outCitationsDimensions[Gender.female]}
                    group={ctx => ctx.outCitationsGroups[Gender.female]}
                    width={230}
                    height={160}
                    elasticY={true}
                    centerBar={true}
                    gap={1}
                    round={dc.round.floor}
                    alwaysUseRounding={true}
                    x={d3.scale.linear().domain([1, 30])}
                    renderHorizontalGridLines={true}
                  />
                </Chart>
                <Chart title="Out Male Citations">
                  <BarChart
                    dimension={ctx => ctx.outCitationsDimensions[Gender.male]}
                    group={ctx => ctx.outCitationsGroups[Gender.male]}
                    width={230}
                    height={160}
                    elasticY={true}
                    centerBar={true}
                    gap={1}
                    round={dc.round.floor}
                    alwaysUseRounding={true}
                    x={d3.scale.linear().domain([1, 30])}
                    renderHorizontalGridLines={true}
                  />
                </Chart>
              </RightRowFilters>
            </RightFilters>
          </Filters>
        </ChartContainer>) : null}
      </div>
    );
  }
};

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

const RightRowFilters2 = styled(RightRowFilters)`
  margin-left: 20px;
`;

export default styled(withRouter(Home))`
display: flex;
flex-direction: column;
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
