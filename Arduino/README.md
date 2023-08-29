# Flashing the firmware

First, the smart textile PCB board must be installed to the Arduino IDE. Do this by installing the [IDLab-AIRO Boards package](https://github.com/RemkoPr/airo-nrf52840-boards/tree/main).

Once the Arduino IDE can compile sketches for the smart textile PCB, open pcb_firmware.ino and export a compiled binary.
Flashing of the PCB is done through the serial wire debug (SWD) protocol using a [JLink EDU Mini](https://www.segger.com/products/debug-probes/j-link/models/j-link-edu-mini/).
When reflashing the [bootloader](https://github.com/arduino/ArduinoCore-mbed/tree/master/bootloaders/nano33ble), do this at address 0x00000000.
When just flashing a new sketch using a .bin file, do this at address 0x00010000.
