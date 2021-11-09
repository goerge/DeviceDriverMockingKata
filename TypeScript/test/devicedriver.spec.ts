import { expect } from "chai";
import "mocha";
import { DeviceDriver } from "../src/devicedriver";
import { FlashMemoryDevice } from "../src/flashmemorydevice";

describe("Device Driver", () => {

  it("should foo", () => {
    // TODO: replace hardware with a Test Double
    const hardware = new FlashMemoryDevice();
    const driver = new DeviceDriver(hardware);

    const data = driver.read(0xFF);

    expect(data).to.equal(0);
  });

});
