import fs from "fs";
import process from "process";

fs.readFile("input.txt", "utf8", function (err, contents) {


  const resetMemory = () => contents.split(",").map(value => parseInt(value, 10));

  let memory = resetMemory();

  let pos = 0

  const getOpcode = () => {
    return memory[pos];
  }

  const getValues = () => {
    return [memory[pos + 1], memory[pos + 2]]
  }

  const getResultPosition = () => {
    return memory[pos + 3];
  }

  const nextPosition = () => {
    pos = pos + 4;
  }

  const process = () => {
    let result = undefined;

    while (result == undefined) {
      if (getOpcode() == 1) {
        const resultPosition = getResultPosition();
        const values = getValues();
        // console.log("opcode 1, values " + values + ", resultposition " + resultPosition)
        memory[resultPosition] = memory[values[0]] + memory[values[1]];
        nextPosition();
      } else if (getOpcode() == 2) {
        const resultPosition = getResultPosition();
        const values = getValues();
        // console.log("opcode 2, values " + values + ", resultposition " + resultPosition)
        memory[resultPosition] = memory[values[0]] * memory[values[1]];
        nextPosition();
      } else if (getOpcode() == 99) {
        console.log("opcode 99, exiting");

        console.log("Result: " + memory[0]);

        result = memory[0];
      }
    }

    return result;

  }

  for (let noun = 0; noun < 100; noun++) {
    for (let verb = 0; verb < 100; verb++) {
      memory = resetMemory();
      pos = 0;

      memory[1] = noun;
      memory[2] = verb;

      const result = process();

      if (result == 19690720) {
        console.log(100 * noun + verb);
        throw "Done"
      }
    };
  }
});
