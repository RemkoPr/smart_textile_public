import asyncio
import atexit
import datetime
from bleak import BleakClient
from loguru import logger


class BleakComm:

    def __init__(self, devices, callbacks):
        """
        Upon initialisation, all devices denoted by the argument "devices" are connected to.

        :param devices: list of MAC addresses (string, e.g. D3:21:46:1B:B9:A0), one per device
        :param callbacks: list of callback functions, one per device
        """

        #  Base 00000000-0000-1000-8000-00805f9b34fb with c130 short UUID as fixed in Arduino firmware
        self.DATA_CHAR_UUID = "0000C130-0000-1000-8000-00805F9b34fb"
        assert(len(devices) == len(callbacks))
        self.devices = devices
        self.callbacks = callbacks
        self.connections = {}

        @atexit.register
        def _cleanup():
            # This function cannot have "self" as an argument and is hence defined here in __init__
            loop = asyncio.get_event_loop()
            loop.run_until_complete(__cleanup())

        async def __cleanup():
            logger.warning("Interrupted, disconnecting devices")
            await self.disconnect_devices()

    async def connect_device(self, device):
        self.connections[device] = BleakClient(device, timeout=5.0)
        await self.connections[device].connect()
        logger.debug("Connected to " + device)

    async def connect_devices(self):
        for device in self.devices:
            await self.connect_device(device)

    async def disconnect_device(self, device):
        try:
            await self.connections[device].disconnect()
            logger.debug("Disconnected from " + device)
        except KeyError:
            logger.warning(f"Tried to disconnect from {device}, but no connection to this device was stored.")

    async def disconnect_devices(self):
        """
        Sequentially disconnect from all devices
        """
        for device in self.devices:
            await self.disconnect_device(device)

    async def subscribe_device(self, device, callback, w):
        logger.debug("Starting " + device + " loop")
        client = self.connections[device]
        await client.start_notify(self.DATA_CHAR_UUID, callback)
        w.set()

        while True:
            await asyncio.sleep(5)

    async def subscribe_devices(self):
        """
        Subscribes to notifications on the data characteristic published by each device
        """
        w = asyncio.Event()
        for device in self.devices:
            asyncio.create_task(self.subscribe_device(device, self.callbacks[device], w))
            await w.wait()
            w.clear()

    async def unsubscribe_device(self, device):
        try:
            await self.connections[device].stop_notify(self.DATA_CHAR_UUID)
            logger.debug("Unsubscribed from " + device)
        except KeyError:
            logger.warning(f"Tried to unsubscribe from {device}, but no connection to this device was stored.")

    async def unsubscribe_devices(self):
        for device in self.devices:
            await self.unsubscribe_device(device)

    async def read_device(self, device):
        logger.debug("Attempting read from " + device)
        client = self.connections[device]
        data = await client.read_gatt_char(self.DATA_CHAR_UUID)
        return list(data)

    async def read_devices(self):
        """
        Sequential single read of BLE peripherals.
        """
        data = []
        for device in self.devices:
            data.append([device] + [datetime.datetime.now()] + await self.read_device(device))
        return data
