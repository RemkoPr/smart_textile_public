
/*  
 *  BEFORE FLASHING A PCB: 
 *  Make sure PCB_NAME is correct,
 *  the name is supposed to reflect the mark with which the physical PCB is distinguished. 
 */

#include <ArduinoBLE.h>

#define PCB_NAME "Smart Textile PCB [green]"
#define BLE_UUID_DATA_SERV      "ECBA" //16b UUIDs needed for compatibility with Blatann lib (python)
#define BLE_UUID_DATA_CHAR      "C130"
#define num_cols                7
#define num_rows                7
#define SERIAL                  false
#define num_data_values         num_cols * num_rows + 1 // All measuring points + a low battery indicator

using namespace std;

int D_pins[] = {0, 1, 2, 3, 4, 5, 6};
byte A_pins[] = {A0, A1, A2, A3, A4, A5, A6};
BLEService dataService( BLE_UUID_DATA_SERV );
BLECharacteristic dataCharacteristic( BLE_UUID_DATA_CHAR, BLERead | BLENotify, num_data_values, true );

uint8_t data[num_data_values];

void setup()
{
  if( SERIAL ) { Serial.begin(9600); }
  setupBleMode();

  for(int D_index=0 ; D_index < num_rows ; D_index++) {
    pinMode(D_pins[D_index], INPUT);
  }
  for(int A_index=0 ; A_index < num_cols ; A_index++) {
    pinMode(A_pins[A_index], INPUT);
  }
}


void loop()
{
  static unsigned long counter = 0;
  
  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();

  if( SERIAL ) {
    for( int i = 0 ; i < num_data_values ; i++) { 
      Serial.print(data[i]);
      Serial.print(" ");
    }
    Serial.print("\n");
  }

  if ( central )
  {
    while ( central.connected() )
    {
      if( central.rssi() != 0 )
      {          
        readData();
        CheckBattery();
        dataCharacteristic.writeValue(data, num_data_values);
      }
    } // while connected
  } // if central
} // loop


//=================== FUNCTIONS =====================\\

void readData()
{
  int A_index, D_index;
  for(D_index=0 ; D_index < num_rows ; D_index++) {
    pinMode(D_pins[D_index], OUTPUT);
    digitalWrite(D_pins[D_index], HIGH);
    for(A_index=0 ; A_index < num_cols ; A_index++) {
      data[1 + A_index + D_index * num_rows] = analogRead(A_pins[A_index])/4.0; // Normalisation to go from 10 bit to 8 bit.
    }    
    pinMode(D_pins[D_index], INPUT);
  }
}

bool CheckBattery() 
{ 
  if( analogRead(LB)/1024.0 > 0.39 ){ // Battery is charged
    data[0] = 0;
    return false;
  }
  else { // Battery is low
    data[0] = 1;
    return true;
  }
}

bool setupBleMode() 
{  
  uint8_t i=0;
  if ( !BLE.begin() )
  {
    return false;
  }

  // set advertised local name and service UUID:
  BLE.setDeviceName( PCB_NAME );
  BLE.setLocalName( PCB_NAME );
  BLE.setAdvertisedService( dataService );

  // BLE add characteristics
  dataService.addCharacteristic( dataCharacteristic );

  // add service
  BLE.addService( dataService );
  // set the initial value for the characeristic:
  //dataCharacteristic.writeValue( 0 );
  // start advertising
  BLE.advertise();

  return true;
}
