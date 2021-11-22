import itertools
import os
import csv
from loguru import logger

from datetime import *


class Persistence:
    def __init__(self, directory):
        self.directory = directory
        self.init_directory(self.directory)
        self.file_name = self.create_unique_file_name(directory)

    def init_directory(self, directory):
        """
        Checks if directory exists, if not, creates it
        :param directory: directory to check
        """
        if not os.path.exists(directory):
            ans = input("Make new directory (" + directory + ")? [Y/N] ")
            if ans.lower() == "y":
                os.makedirs(directory)
            elif ans.lower() == "n":
                raise NotADirectoryError("Data directory doesn't exist, creation cancelled by user.")
            else:
                raise ValueError("Invalid answer given, enter [Y] or [N].")

    def create_unique_file_name(self, directory):
        # Build the file name so that each experiment (a.k.a. each run of the code) saves data to a different file

        file_name = str(date.today())
        file_number = 0
        for file_in_dir in os.listdir(directory):
            if file_in_dir.startswith(file_name):
                val = int(file_in_dir[file_in_dir.find("[") + 1:file_in_dir.find("]")])
                if val > file_number:
                    file_number = val
        file_name = file_name + "[" + str(file_number + 1) + "].csv"

        return file_name


class SensorPersistence(Persistence):
    """
        Writes sensor data to a buffer and periodically flushes to file system.
    """

    def __init__(self, devices, directory="./data/", buffer_size=10):
        super().__init__(directory)
        self.devices = devices
        self.buffer = []
        self.max_buffer_size = buffer_size
        self.init_csv_file(self.directory, self.file_name)

    def init_csv_file(self, directory, file_name):
        # TODO: haal grid size van smart textile
        grid_width = grid_height = 7
        header = ['PCB addr', 'timestamp', 'LowBattery'] + \
                 [f'sensor_value_{digital_pin}_{analog_pin}'
                  for digital_pin, analog_pin in itertools.product(range(grid_width), range(grid_height))]
        with open(os.path.join(directory, file_name), 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            csv_writer.writerow(header)

    def persist(self, data):
        self.buffer.append(data)

        if len(self.buffer) > self.max_buffer_size:
            self._persist_to_file()
            self.buffer = []

    def _persist_to_file(self):
        with open(os.path.join(self.directory, self.file_name), 'a+', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')

            for all_pcb_sensor_values in self.buffer:
                for row in all_pcb_sensor_values:
                    csv_writer.writerow(row)
        logger.info("Wrote to file")
