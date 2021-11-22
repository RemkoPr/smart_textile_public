import os
import sys
from smart_textile_group import SmartTextileGroup

from absl import app
from absl import flags
from loguru import logger
import asyncio

from utils.run import *

FLAGS = flags.FLAGS


def main(_):
    PCB_BLACK = "D3:21:46:1B:B9:A0"
    PCB_RED = "FA:3D:10:33:9A:0F"
    PCB_GREEN = "E4:33:DA:53:42:57"

    # only log at INFO level to console
    logger.configure(handlers=[{"sink": sys.stderr, "level": "DEBUG"}])
    logger.add(os.path.join('./data', "smart_textile.log"), rotation="500 MB", level="DEBUG")

    smart_textiles = SmartTextileGroup([PCB_GREEN, PCB_BLACK], grid_size=(7, 7), comm_mode="BLEAK", data_directory=None)
    asyncio.get_event_loop().run_until_complete(smart_textiles.subscribe_to_textiles())
    #asyncio.get_event_loop().run_until_complete(smart_textiles.keystroke_capture('./data/classifier/',{"open": "o","folded": "f","random": "r"}))


if __name__ == '__main__':
    app.run(main)
