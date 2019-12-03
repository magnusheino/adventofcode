import fs from "fs";

fs.readFile("input.txt", "utf8", function(err, contents) {
  const masses = contents.split("\n").map(mass => parseInt(mass, 10));

  const getFuelFromMass = mass => {
    let fuel = parseInt(mass / 3, 10) - 2;

    return fuel > 0 ? fuel : 0;
  };

  let fuels = masses.map(mass => {
    const fuel = getFuelFromMass(mass);

    let totalFuel = fuel;

    let extraFuel = getFuelFromMass(fuel);
    totalFuel += extraFuel;

    while (extraFuel > 0) {
      extraFuel = getFuelFromMass(extraFuel);
      totalFuel += extraFuel;
    }

    return totalFuel;
  });

  let fuel = fuels.reduce((total, fuel) => total + fuel, 0);

  console.log(fuel);
});
