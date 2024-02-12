require('dotenv').config()
const app = require('./app');

const port = '8888';
const mongo_uri = process.env.MONGO_URI;

if (!mongo_uri) {
    console.log("Bitte MONGO_URI setzen.");
    process.exit(1);
}

console.log(mongo_uri)

const read = require('./ReadData')
read.run(mongo_uri);

// CommonJs
const fastify = require('fastify')({
  logger: true
});

fastify.register(require('@fastify/mongodb'), {
    forceClose: true,    
    url: mongo_uri
})

fastify.register(require("@fastify/view"), {
  engine: {
    ejs: require("ejs"),
  },
});

fastify.get("/", async (req, reply) => {
    const categories = [
        "GPU", "CPU", "Case", "Mainboard", "PSU", "RAM" 
    ]
    const data = {};

    for (const cat of categories) {
        const collection = fastify.mongo.client.db('Prices').collection(cat);
        const results = await collection.find({}).sort({_id: -1}).limit(5);
        data[cat] = await results.toArray();
    }

    console.log(data);
       
    return reply.view("/templates/index.ejs", data);
});

fastify.listen({ host: "0.0.0.0", port: process.env.PORT ?? 3000 }, (err, address) => {
    if (err) {
        console.log("Failed to start web server.");
        console.log(err)
        process.exit(1);
    }
    console.log("Started webserver at", address);
})

// app.listen(port, () => {
//   console.log(`Server is listening on port ${port}...`);
// });
