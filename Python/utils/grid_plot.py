import tkinter as tk
import numpy as np


class GridPlot(tk.Tk):
    '''
    Based on: https://stackoverflow.com/questions/4781184/tkinter-displaying-a-square-grid
    This class will plot RGB (8 bit!) data from the textile on a greyscale grid, each square representing a measuring
    point.
    '''

    def __init__(self, devices=[], grid_size=(7, 7)):
        tk.Tk.__init__(self)
        self.devices = devices
        self.cell_width = 50
        self.cell_height = 50
        self.grid_size = grid_size
        tile_width = self.grid_size[1] * self.cell_width
        tile_height = self.grid_size[0] * self.cell_height
        self.canvas = tk.Canvas(self, width=(tile_width + self.cell_width) * len(self.devices) + self.cell_width,
                                height=tile_height * 1.5, borderwidth=0, highlightthickness=0, bg="#417fba")

        # Write MAC addresses under respective tiles.
        for i, device_name in enumerate(self.devices):
            device_name = devices[i]
            tile_width = self.grid_size[1] * self.cell_width
            self.canvas.create_text(self.cell_width + tile_width * 1 / 2 + (tile_width + self.cell_width) * i,
                                    (self.grid_size[0] + 1 + 1 / 2) * self.cell_height, fill="#ededed", font="Arial 20 bold",
                                    text=device_name)

        self.canvas.pack(side="top", fill="both", expand="true")

        self.delay = 1  # Delay between redrawing in ms

        self.square_colors = {}
        for device in self.devices:
            self.square_colors[device] = np.zeros(self.grid_size)

        # Create individual squares
        self.rect = {}
        self._create_individual_squares()

        self.redraw()

    def _create_individual_squares(self):
        for device_num, device in enumerate(self.devices):
            for row in range(self.grid_size[0]):
                for column in range(self.grid_size[1]):
                    x1 = self.cell_width + column * self.cell_width + device_num * (self.grid_size[1] + 1) * self.cell_width
                    y1 = self.cell_height + row * self.cell_height
                    x2 = x1 + self.cell_width
                    y2 = y1 + self.cell_height
                    self.rect[device_num, row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", tags="rect")

    def redraw(self):
        for device_num, device in enumerate(self.devices):
            for row in range(self.grid_size[0]):
                for column in range(self.grid_size[1]):
                    item_id = self.rect[device_num, row, column]
                    RGB = int(self.square_colors[device][row][column])
                    if RGB > 255:
                        RGB = 255
                    self.canvas.itemconfig(item_id, fill="#%02x%02x%02x" % (RGB, RGB, RGB))
        self.after(self.delay, lambda: self.redraw())

    def update_view(self):
        self.update_idletasks()
        self.update()
