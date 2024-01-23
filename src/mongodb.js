const { MongoClient } = require("mongodb");

let uri = process.env.MONGO_URI;

const client = new MongoClient(uri);

async function run() {
  try {
    await client.connect();
    console.log("Connected")
  } finally {
    await client.close();
  }
}
run().catch(console.dir);
