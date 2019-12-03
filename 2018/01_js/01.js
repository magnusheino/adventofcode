import fs from 'fs';

fs.readFile('01_input.txt', 'utf8', function (err, contents) {
    const changes = contents.split('\n').map(change => parseInt(change, 10));

    let result = changes.reduce((total, change) => total + change, 0);
    console.log(result);
});