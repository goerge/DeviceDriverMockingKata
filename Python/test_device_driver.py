import unittest
from unittest.mock import Mock
from device_driver import DeviceDriver, FlashMemoryDevice


class DeviceDriverTest(unittest.TestCase):
    def test_read_from_hardware(self):
        # TODO: replace hardware with a Test Double
        hardware = FlashMemoryDevice()
        driver = DeviceDriver(hardware)
        
        data = driver.read(0xFF)

        self.assertEqual(data, 0)


if __name__ == "__main__":
    unittest.main()
