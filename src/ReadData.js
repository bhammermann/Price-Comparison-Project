const { MongoClient } = require('mongodb');


module.exports.run = async function run(url) {
    const dbName = 'Prices'; // Ändern Sie den Namen Ihrer Datenbank entsprechend
    const client = new MongoClient(url);
    await client.connect();

    const db = client.db(dbName);

    // Überwachen von Änderungen in allen Sammlungen der Datenbank mit einem Change Stream
    const changeStream = db.watch();
    console.log("Changestream started")

    // Event-Handler für Änderungen in allen Sammlungen
    changeStream.on('change', function(change) {
        //console.log('Änderung in der Datenbank erkannt:');
        //console.log('  Collection:', change.ns.coll); // Ausgabe des Namens der Sammlung, in der die Änderungen aufgetreten sind
        //console.log('  Änderung:', change);

        // Je nach Collection-Aktualisierung können Sie unterschiedliche Logik implementieren
        switch(change.operationType) {
            case 'insert':
                handleInsert(change.ns.coll, change.fullDocument);
                break;
            // Weitere Fälle (update, delete) können ebenfalls behandelt werden
            default:
                console.log('Änderungstyp nicht unterstützt:', change.operationType);
        }
    });

    // Sie können auch auf Fehler im Change Stream reagieren
    changeStream.on('error', function(err) {
        console.error('Fehler im Change Stream:', err);
    });

}

// Funktion zum Behandeln von Einfügungen in verschiedenen Sammlungen
function handleInsert(collectionName, document) {
    console.log(`Neue Einträge in Sammlung "${collectionName}":`);
    const name = document.name;
    const preis = document.preis;
        
    // Hier können Sie mit den Variablen `name` und `preis` arbeiten
    console.log('  Name:', name);
    console.log('  Preis:', preis);
}
