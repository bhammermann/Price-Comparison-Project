// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles
parcelRequire = (function (modules, cache, entry, globalName) {
  // Save the require from previous bundle to this closure if any
  var previousRequire = typeof parcelRequire === 'function' && parcelRequire;
  var nodeRequire = typeof require === 'function' && require;

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire = typeof parcelRequire === 'function' && parcelRequire;
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error('Cannot find module \'' + name + '\'');
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = cache[name] = new newRequire.Module(name);

      modules[name][0].call(module.exports, localRequire, module, module.exports, this);
    }

    return cache[name].exports;

    function localRequire(x){
      return newRequire(localRequire.resolve(x));
    }

    function resolve(x){
      return modules[name][1][x] || x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [function (require, module) {
      module.exports = exports;
    }, {}];
  };

  var error;
  for (var i = 0; i < entry.length; i++) {
    try {
      newRequire(entry[i]);
    } catch (e) {
      // Save first error but execute all entries
      if (!error) {
        error = e;
      }
    }
  }

  if (entry.length) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(entry[entry.length - 1]);

    // CommonJS
    if (typeof exports === "object" && typeof module !== "undefined") {
      module.exports = mainExports;

    // RequireJS
    } else if (typeof define === "function" && define.amd) {
     define(function () {
       return mainExports;
     });

    // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }

  // Override the current require with this new one
  parcelRequire = newRequire;

  if (error) {
    // throw error from earlier, _after updating parcelRequire_
    throw error;
  }

  return newRequire;
})({"app.js":[function(require,module,exports) {
const http = require('http');
const fs = require('fs');
const path = require('path');
const mimeTypes = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpg',
  '.gif': 'image/gif',
  '.wav': 'audio/wav',
  '.mp4': 'video/mp4',
  '.woff': 'application/font-woff',
  '.ttf': 'application/font-ttf',
  '.eot': 'application/vnd.ms-fontobject',
  '.otf': 'application/font-otf',
  '.svg': 'application/image/svg+xml'
};
const app = http.createServer((request, response) => {
  let filePath = path.join(__dirname, 'public', request.url);
  if (filePath === path.join(__dirname, 'public', '/')) filePath = path.join(__dirname, 'public', 'index.html');
  const extname = String(path.extname(filePath)).toLowerCase();
  const contentType = mimeTypes[extname] || 'application/octet-stream';
  fs.readFile(filePath, (error, content) => {
    if (error) {
      response.writeHead(500);
      response.end(`Sorry, check with the site admin for error: ${error.code} ..\n`);
      response.end();
    } else {
      response.writeHead(200, {
        'Content-Type': contentType
      });
      response.end(content, 'utf-8');
    }
  });
});
module.exports = app;
},{}],"ReadData.js":[function(require,module,exports) {
const {
  MongoClient
} = require('mongodb');
module.exports.run = async function run(uri) {
  const dbName = 'Prices';
  const client = new MongoClient(uri);
  await client.connect();
  const db = client.db(dbName);

  // hier werden auf Änderungen in der db geschaut
  const changeStream = db.watch();
  console.log("Changestream started");

  // Event-Handler für Änderungen in allen Sammlungen
  changeStream.on('change', function (change) {
    //console.log('Änderung in der Datenbank erkannt:');
    //console.log('  Collection:', change.ns.coll); // Ausgabe des Namens der Sammlung, in der die Änderungen aufgetreten sind
    //console.log('  Änderung:', change);

    switch (change.operationType) {
      case 'insert':
        handleInsert(change.ns.coll, change.fullDocument);
        break;
      default:
        console.log('Änderungstyp nicht unterstützt:', change.operationType);
    }
  });
  changeStream.on('error', function (err) {
    console.error('Fehler im Change Stream:', err);
  });
};

// Funktion zum Behandeln von Einfügungen in verschiedenen Sammlungen
function handleInsert(collectionName, document) {
  console.log(`Neue Einträge in Sammlung "${collectionName}":`);
  const name = document.name;
  const preis = document.preis;

  // logging
  console.log('  Name:', name);
  console.log('  Preis:', preis);
}
},{}],"index.js":[function(require,module,exports) {
var _process$env$PORT;
require('dotenv').config();
const app = require('./app');
const port = '8888';
const mongo_uri = process.env.MONGO_URI;
if (!mongo_uri) {
  console.log("Bitte MONGO_URI setzen.");
  process.exit(1);
}
console.log(mongo_uri);
const read = require('./ReadData');
read.run(mongo_uri);

// CommonJs
const fastify = require('fastify')({
  logger: true
});
fastify.register(require('@fastify/mongodb'), {
  forceClose: true,
  url: mongo_uri
});
fastify.register(require("@fastify/view"), {
  engine: {
    ejs: require("ejs")
  }
});
fastify.get("/", async (req, reply) => {
  const categories = ["GPU", "CPU", "Case", "Mainboard", "PSU", "RAM"];
  const data = {};
  for (const cat of categories) {
    const collection = fastify.mongo.client.db('Prices').collection(cat);
    const results = await collection.find({}).sort({
      _id: -1
    }).limit(5);
    data[cat] = await results.toArray();
  }
  console.log(data);
  return reply.view("/templates/index.ejs", data);
});
fastify.listen({
  host: "0.0.0.0",
  port: (_process$env$PORT = process.env.PORT) !== null && _process$env$PORT !== void 0 ? _process$env$PORT : 3000
}, (err, address) => {
  if (err) {
    console.log("Failed to start web server.");
    console.log(err);
    process.exit(1);
  }
  console.log("Started webserver at", address);
});

// app.listen(port, () => {
//   console.log(`Server is listening on port ${port}...`);
// });
},{"./app":"app.js","./ReadData":"ReadData.js"}]},{},["index.js"], null)
//# sourceMappingURL=/index.js.map