require('dotenv').config()
const app = require('./app');

const port = '8888';

const db = require('./mongodb')

// app.listen(port, () => {
//   console.log(`Server is listening on port ${port}...`);
// });