import fs from 'fs';

function Counter(s) {
    var count = {};
    Array.from(s).forEach(val => count[val] = (count[val] || 0) + 1);
    return count;
}

fs.readFile('02_input.txt', 'utf8', function (err, contents) {
    const boxes = contents.split('\n').map(box => box.trim());

    const counts = boxes.map(box => Counter(box)).map(count => {
        return Object.values(count);
    })

    let has2 = 0
    let has3 = 0

    counts.forEach(count => {
        if (count.includes(2)) {
            has2++;
        }

        if (count.includes(3)) {
            has3++;
        }
    });

    const checksum = has2 * has3;

    console.log(checksum)
});