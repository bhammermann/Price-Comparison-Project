const { MongoClient } = require('mongodb');


module.exports.run = async function run(uri) {
    const dbName = 'Prices'; 
    const client = new MongoClient(uri);
    await client.connect();

    const db = client.db(dbName);

    // hier werden auf Änderungen in der db geschaut
    const changeStream = db.watch();
    console.log("Changestream started")

    // Event-Handler für Änderungen in allen Sammlungen
    changeStream.on('change', function(change) {
        //console.log('Änderung in der Datenbank erkannt:');
        //console.log('  Collection:', change.ns.coll); // Ausgabe des Namens der Sammlung, in der die Änderungen aufgetreten sind
        //console.log('  Änderung:', change);

        switch(change.operationType) {
            case 'insert':
                handleInsert(change.ns.coll, change.fullDocument);
                break;
            default:
                console.log('Änderungstyp nicht unterstützt:', change.operationType);
        }
    });

    changeStream.on('error', function(err) {
        console.error('Fehler im Change Stream:', err);
    });

}

// Funktion zum Behandeln von Einfügungen in verschiedenen Sammlungen
function handleInsert(collectionName, document) {
    console.log(`Neue Einträge in Sammlung "${collectionName}":`);
    const name = document.name;
    const preis = document.preis;
        
    // logging
    console.log('  Name:', name);
    console.log('  Preis:', preis);
}
