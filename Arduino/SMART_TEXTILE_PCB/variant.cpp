#include "Arduino.h"

PinDescription g_APinDescription[] = {

  // D0 - D6
  P0_23, NULL, NULL,     // D0
  P0_21, NULL, NULL,     // D1
  P0_22,  NULL, NULL,     // D2
  P0_19,  NULL, NULL,     // D3
  P0_13,  NULL, NULL,     // D4
  P0_14, NULL, NULL,     // D5
  P0_15, NULL, NULL,     // D6

  // A0 - A6
  P0_3,  NULL, NULL,     // A0
  P0_28,  NULL, NULL,     // A1
  P0_2, NULL, NULL,     // A2
  P0_31, NULL, NULL,     // A3
  P0_29, NULL, NULL,     // A4
  P0_30,  NULL, NULL,     // A5
  P0_4, NULL, NULL,     // A6

  // I2C
  P0_20, NULL, NULL,     // SDA
  P0_17, NULL, NULL,     // SCL

  // Low battery detector pin
  P0_5, NULL, NULL,		// LB
};

extern "C" {
  unsigned int PINCOUNT_fn() {
    return (sizeof(g_APinDescription) / sizeof(g_APinDescription[0]));
  }
}

#include "nrf_rtc.h"

void initVariant() {

  // Errata Nano33BLE - I2C pullup is on SWO line, need to disable TRACE
  // was being enabled by nrfx_clock_anomaly_132
 // CoreDebug->DEMCR = 0;
 // NRF_CLOCK->TRACECONFIG = 0;

  // FIXME: bootloader enables interrupt on COMPARE[0], which we don't handle
  // Disable it here to avoid getting stuck when OVERFLOW irq is triggered
  nrf_rtc_event_disable(NRF_RTC1, NRF_RTC_INT_COMPARE0_MASK);
  nrf_rtc_int_disable(NRF_RTC1, NRF_RTC_INT_COMPARE0_MASK);
 
  NRF_PWM_Type* PWM[] = {
    NRF_PWM0, NRF_PWM1, NRF_PWM2
#ifdef NRF_PWM3
    ,NRF_PWM3
#endif
  };

  for (unsigned int i = 0; i < (sizeof(PWM)/sizeof(PWM[0])); i++) {
    PWM[i]->ENABLE = 0;
    PWM[i]->PSEL.OUT[0] = 0xFFFFFFFFUL;
  } 
}

#ifdef SERIAL_CDC

static void utox8(uint32_t val, uint8_t* s) {
  for (int i = 0; i < 16; i=i+2) {
    int d = val & 0XF;
    val = (val >> 4);

    s[15 - i -1] = d > 9 ? 'A' + d - 10 : '0' + d;
    s[15 - i] = '\0';
  }
}

uint8_t getUniqueSerialNumber(uint8_t* name) {
  #define SERIAL_NUMBER_WORD_0  NRF_FICR->DEVICEADDR[1]
  #define SERIAL_NUMBER_WORD_1  NRF_FICR->DEVICEADDR[0]

  utox8(SERIAL_NUMBER_WORD_0, &name[0]);
  utox8(SERIAL_NUMBER_WORD_1, &name[16]);

  return 32;
}

void _ontouch1200bps_() {
  __disable_irq();
  NRF_POWER->GPREGRET = DFU_MAGIC_SERIAL_ONLY_RESET;
  NVIC_SystemReset();
}

#endif
