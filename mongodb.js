const { MongoClient } = require("mongodb");

const username = encodeURIComponent("Björn Hammermann");
const password = encodeURIComponent("FOM-MongoDB");
const cluster = "Project 0";
const authSource = "admin";
const authMechanism = "SCRAM-SHA-256";

let uri =
  `mongodb+srv://${username}:${password}@${cluster}/?authSource=${authSource}&authMechanism=${authMechanism}`;

const client = new MongoClient(uri);

async function run() {
  try {
    await client.connect();

    const database = client.db("<dbName>");
    const ratings = database.collection("<collName>");

    const cursor = ratings.find();

    await cursor.forEach(doc => console.dir(doc));
  } finally {
    await client.close();
  }
}
run().catch(console.dir);
