#pragma once
#include "mbed_config.h"
#include <stdint.h>
#include <macros.h>

#ifndef __PINS_ARDUINO__
#define __PINS_ARDUINO__

// Frequency of the board main oscillator
#define VARIANT_MAINOSC (32768ul)

// Master clock frequency
#define VARIANT_MCK     (64000000ul)

// Pins
// ----

// Number of pins defined in PinDescription array
#ifdef __cplusplus
extern "C" unsigned int PINCOUNT_fn();
#endif
#define PINS_COUNT           (PINCOUNT_fn())
#define NUM_DIGITAL_PINS     (21u)
#define NUM_ANALOG_INPUTS    (7u)
#define NUM_ANALOG_OUTPUTS   (0u)

// Analog pins
// -----------
#define PIN_A0 (7u)
#define PIN_A1 (8u)
#define PIN_A2 (9u)
#define PIN_A3 (10u)
#define PIN_A4 (11u)
#define PIN_A5 (12u)
#define PIN_A6 (13u)
static const uint8_t A0  = PIN_A0;
static const uint8_t A1  = PIN_A1;
static const uint8_t A2  = PIN_A2;
static const uint8_t A3  = PIN_A3;
static const uint8_t A4  = PIN_A4;
static const uint8_t A5  = PIN_A5;
static const uint8_t A6  = PIN_A6;
#define ADC_RESOLUTION 12

// Low battery detector readout pin
#define PIN_LB (16u)
static const uint8_t LB = PIN_LB;

// Digital pins
// -----------
#define D0   0
#define D1   1
#define D2   2
#define D3   3
#define D4   4
#define D5   5
#define D6   6

// Wire
#define PIN_WIRE_SDA        (14u)
#define PIN_WIRE_SCL        (15u)

// These serial port names are intended to allow libraries and architecture-neutral
// sketches to automatically default to the correct port name for a particular type
// of use.  For example, a GPS module would normally connect to SERIAL_PORT_HARDWARE_OPEN,
// the first hardware serial port whose RX/TX pins are not dedicated to another use.
//
// SERIAL_PORT_MONITOR        Port which normally prints to the Arduino Serial Monitor
//
// SERIAL_PORT_USBVIRTUAL     Port which is USB virtual serial
//
// SERIAL_PORT_LINUXBRIDGE    Port which connects to a Linux system via Bridge library
//
// SERIAL_PORT_HARDWARE       Hardware serial port, physical RX & TX pins.
//
// SERIAL_PORT_HARDWARE_OPEN  Hardware serial ports which are open for use.  Their RX & TX
//                            pins are NOT connected to anything by default.

// Mbed specific defines
#define SERIAL_HOWMANY		0

#define SERIAL_CDC			1
#define HAS_UNIQUE_ISERIAL_DESCRIPTOR
#define BOARD_VENDORID		0x2342
#define BOARD_PRODUCTID		0x805b
#define BOARD_NAME			"SMART_TEXTILE_PCB"

#define DFU_MAGIC_SERIAL_ONLY_RESET   0xb0

#define I2C_SDA				(digitalPinToPinName(PIN_WIRE_SDA))
#define I2C_SCL				(digitalPinToPinName(PIN_WIRE_SCL))

#define digitalPinToPort(P)		(digitalPinToPinName(P)/32)

#ifdef SERIAL_CDC
	uint8_t getUniqueSerialNumber(uint8_t* name);
#endif
void _ontouch1200bps_();

#endif //__PINS_ARDUINO__
