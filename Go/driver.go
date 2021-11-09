package codekata

import (
	"errors"
	"time"
)

const init_address = 0x0

const program_command byte = 0x40
const ready_mask byte = 0x02
const ready_no_error byte = 0x00

const timeout_threshold int64 = 100000000

const reset_command byte = 0xff
const vpp_mask byte = 0x20
const internal_error_mask byte = 0x10
const protected_block_error_mask byte = 0x08

// DeviceDriver is used by the operating system to interact with the hardware 'FlashMemoryDevice'.
type DeviceDriver struct {
	device FlashMemoryDevice
}

func (driver DeviceDriver) Read(address uint32) byte {
	return driver.device.Read(address)
}

func (driver DeviceDriver) Write(address uint32, data byte) error {
	start := time.Now().UnixNano()
	driver.device.Write(init_address, program_command)
	driver.device.Write(address, data)
	var readyByte byte
	for {
		readyByte = driver.device.Read(init_address)
		if (readyByte & ready_mask) != 0 {
			break
		}
		if readyByte != ready_no_error {
			driver.device.Write(init_address, reset_command)
			if (readyByte & vpp_mask) > 0 {
				return errors.New("ErrorWriteVpp")
			}
			if (readyByte & internal_error_mask) > 0 {
				return errors.New("ErrorWriteInternal")
			}
			if (readyByte & protected_block_error_mask) > 0 {
				return errors.New("ErrorWriteProtectedBlock")
			}
		}
		if time.Now().UnixNano()-start > timeout_threshold {
			return errors.New("ErrorWriteTimeout")
		}
	}
	actual := driver.device.Read(address)
	if data != actual {
		return errors.New("ErrorReadFailure")
	}

	return nil
}
