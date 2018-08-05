import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {injectGlobal} from 'styled-components';
import {Provider} from 'react-redux';
import {BrowserRouter, Route, Switch, Redirect} from 'react-router-dom';
import {createStore, applyMiddleware, compose} from 'redux';
import thunk from 'redux-thunk';
import {ThemeProvider} from 'styled-components';

import {reducers} from './redux';
import HomeContainer from './components/HomeContainer';
import {MainTheme} from './themes';

const composeEnhancers = (window as any).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(reducers, {}, composeEnhancers(applyMiddleware(thunk)));

ReactDOM.render(
    <Provider store={store}>
    <BrowserRouter>
        <ThemeProvider theme={MainTheme}>
            <Switch>
                <Route exact path="/" component={HomeContainer}/>
            </Switch>
        </ThemeProvider>
    </BrowserRouter>
</Provider>, document.getElementById('root'));

// tslint:disable-next-line:no-unused-expression
injectGlobal `
  body {
    font-family: 'Source Sans Pro', sans-serif;
    font-size: 15px;
    background: rgb(68,169,205) url('/assets/images/background.jpg') repeat-x top left;
    -moz-osx-font-smoothing: grayscale;
    -webkit-font-smoothing: antialiased;
  }
`;