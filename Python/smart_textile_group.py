import numpy as np
from loguru import logger
import datetime
import time as t
import asyncio

from communication.bleak_comm import BleakComm
from utils.persistence import *

try:
    from utils.grid_plot import GridPlot
except (ModuleNotFoundError, ImportError) as e:
    GridPlot = None
    logger.warning("Visualisation off (TKinter module not installed?)")


class SmartTextileGroup:
    def __init__(self, devices, grid_size=(7, 7), comm_mode="BLEAK", data_directory=None):
        self.devices = devices
        self.grid_size = grid_size
        if self.grid_size is not None:
            self.current_view = {device: np.zeros(self.grid_size) for device in devices}
            self.grid = GridPlot(devices, grid_size=self.grid_size)
        self.comm_mode = comm_mode
        if data_directory:
            self.data_handler = SensorPersistence(devices, data_directory, buffer_size=20)
        if comm_mode == "BLEAK":
            def handle_data(handle, value, device):
                """
                :param handle: integer characteristic read handle the data was received on
                :param value: data returned in the notification as bytearray
                :param device: hardware address (str, e.g. "D3:21:46:1B:B9:A0") of the device to which this callback belongs
                """
                data = list(value)
                logger.info([device] + data)
                if self.grid_size:
                    data_no_low_battery = data[1:]  # First value in length-50 list is low battery indicator
                    data_resize = np.array(data_no_low_battery).reshape(self.grid_size)
                    self.current_view[device] = data_resize
                if data_directory:
                    self.data_handler.persist([[device, datetime.now()] + data])
            callbacks = {device: lambda handle, value, device=device:
                            handle_data(handle, value, device) for device in devices}
            self.comm_handler = BleakComm(self.devices, callbacks)
        else:
            ValueError("Invalid communication mode passed")

    async def subscribe_to_textiles(self):
        """
        subscribes to notifications on the data characteristic published by each smart textile and optionally plots the data
        """
        if self.comm_mode == "BLEAK":
            await self.comm_handler.connect_devices()
            await self.comm_handler.subscribe_devices()
        else:
            ValueError("Communication mode " + self.comm_mode + " does not support this function.")

        if self.grid_size:
            while True:
                await asyncio.sleep(0.01)
                self.grid.square_colors = self.current_view
                self.grid.update_view()
        else:
            await asyncio.Event().wait()

    async def keystroke_capture(self, main_dir, states):
        """
        Sets up a data link between BLE devices and the host for this script, reads data from multiple smart
        textiles and logs them to a file in a subfolder in the data_directory whenever the ENTER key is pressed.
        The subfolder is created/determined based on the user's name, prompted at startup.
        :param states: dict (str) -> (str), keys are names of the states to log, each key should have one value, being
                        shortcut name for this state, to be entered when logging it.
        :param main_dir: main directory, where subfolder of user and different states should be made.
        """
        await self.comm_handler.connect_devices()
        t.sleep(1)  # Give logger some time to print
        folder = input(f"Enter your name (your data will appear in {main_dir}yourname) and press ENTER: ")
        directories = {}
        data_handlers = {}
        counters = {}
        for state in list(states.keys()):
            directories[state] = main_dir + folder + '/' + str(state) + '/'
            data_handlers[state] = SensorPersistence(self.devices, directory=directories[state], buffer_size=0)
            counters[state] = 0
        while True:
            t.sleep(1)  # Give logger some time to print
            print(f'In this session so far, you\'ve logged {"".join([f"{state} {counters[state]} times ; " for state in states])}')
            log_type = input(
                f'{"".join([f"To log a {state} state, enter {states[state]} ; " for state in states])} finally, press ENTER: '
            )
            for state in states:
                if log_type == states[state]:  # The state shortcut name should be entered
                    data = await self.comm_handler.read_devices()
                    data_handlers[state].persist(data)
                    counters[state] += 1
                    break
            else:
                print("Invalid option entered!")
                continue
