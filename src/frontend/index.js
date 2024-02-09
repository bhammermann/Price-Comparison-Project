import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

ReactDOM.render(<App />, document.getElementById('root'));

require('dotenv').config()
const app = require('./app');

const port = '8888';

const db = require('./mongodb')

// app.listen(port, () => {
//   console.log(`Server is listening on port ${port}...`);
// });