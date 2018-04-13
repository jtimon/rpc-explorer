import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';

import createStore from './store';

import App from './components/app';

const Immutable = require('seamless-immutable').static;

const store = createStore();

function Body() {
  return (
    <Provider store={store}>
      <App />
    </Provider>
  );
}

function initLibraries() {
  window.store = store;
  window.Immutable = Immutable;
}

function initStateValues() {
  store.dispatchMerge({
    chain: 'elementsregtest',
    chainInfo: Immutable({}),
    blocks: Immutable.from({
      hashes: {},
      heights: {},
      stats: {},
    }),
    transactions: Immutable({}),
    searchRedirect: '',
  });
}

initLibraries();
initStateValues();
render(<Body />, document.getElementById('liquid-explorer'));
