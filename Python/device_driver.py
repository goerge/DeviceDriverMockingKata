import time


class VppException(Exception):
    pass


class InternalErrorException(Exception):
    pass


class ProtectedBlockException(Exception):
    pass


class ReadFailureException(Exception):
    def __init__(self, message):
        super().__init__(message)


class TimeoutException(Exception):
    def __init__(self, message):
        super().__init__(message)

class FlashMemoryDevice:
    """
    This class represents the interface to a Flash Memory Device. The hardware has only two methods - 'read' and 'write'
    However, the interface for using the device is a lot more complex than that. It is outlined in the top-level README file.
    """
    def read(self, address: int) -> int:
        raise NotImplementedError("unsupported operation")

    def write(self, address: int, data: int):
        raise NotImplementedError("unsupported operation")

class DeviceDriver:
    """
    This class is used by the operating system to interact with the hardware 'FlashMemoryDevice'.
    """

    INIT_ADDRESS = 0x00

    PROGRAM_COMMAND = 0x40
    READY_MASK = 0x02
    READY_NO_ERROR = 0x00

    TIMEOUT_THRESHOLD = 100_000_000  # nanoseconds

    RESET_COMMAND = 0xFF
    VPP_MASK = 0x20
    INTERNAL_ERROR_MASK = 0x10
    PROTECTED_BLOCK_ERROR_MASK = 0x08

    def __init__(self, hardware: FlashMemoryDevice):
        self.hardware = hardware

    def read(self, address: int) -> int:
        return self.hardware.read(address)

    def write(self, address: int, data: int):
        start = time.perf_counter_ns()
        self.hardware.write(self.INIT_ADDRESS, self.PROGRAM_COMMAND)
        self.hardware.write(address, data)

        while True:
            ready_byte = self.read(self.INIT_ADDRESS)
            if ready_byte & self.READY_MASK:
                break

            if ready_byte != self.READY_NO_ERROR:
                self.hardware.write(self.INIT_ADDRESS, self.RESET_COMMAND)

                if ready_byte & self.VPP_MASK:
                    raise VppException()

                if ready_byte & self.INTERNAL_ERROR_MASK:
                    raise InternalErrorException()

                if ready_byte & self.PROTECTED_BLOCK_ERROR_MASK:
                    raise ProtectedBlockException()

            if time.perf_counter_ns() - start > self.TIMEOUT_THRESHOLD:
                raise TimeoutException("Timeout when trying to read data from memory")

        actual = self.read(address)
        if data != actual:
            raise ReadFailureException("Failed to read data from memory")
