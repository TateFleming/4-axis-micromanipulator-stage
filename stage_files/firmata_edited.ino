#include <Firmata.h>
/* has the command arrived? */
boolean firstCommand = false;
int dataOnSerial = 0;
boolean statusLed = false;

/* analog inputs */
int analogInputsToReport = 0; // bitwise array to store pin reporting

/* digital input ports */
byte reportPINs[TOTAL_PORTS];       // 1 = report this port, 0 = silence
byte previousPINs[TOTAL_PORTS];     // previous 8 bits sent

/* pins configuration */
byte pinConfig[TOTAL_PINS];         // configuration of every pin
byte portConfigInputs[TOTAL_PORTS]; // each bit: 1 = pin in INPUT, 0 = anything else
int pinState[TOTAL_PINS];           // any value that has been written

/* timer variables */
unsigned long currentMillis;        // store the current value from millis()
unsigned long previousMillis;       // for comparison with currentMillis
int samplingInterval = 19;          // how often to run the main loop (in ms)
unsigned long toggleMillis;

void toggleLed()
{
 if (millis() - toggleMillis > 500) {
   statusLed = !statusLed;
   digitalWrite(13, statusLed);
   toggleMillis = millis();
 }
}

void outputPort(byte portNumber, byte portValue, byte forceSend)
{
 // pins not configured as INPUT are cleared to zeros
 portValue = portValue & portConfigInputs[portNumber];
 // only send if the value is different than previously sent
 if(forceSend || previousPINs[portNumber] != portValue) {
   Firmata.sendDigitalPort(portNumber, portValue);
   previousPINs[portNumber] = portValue;
 }
}

void checkDigitalInputs(void)
{
 if (TOTAL_PORTS > 2 && reportPINs[2]) outputPort(2, readPort(2, portConfigInputs[2]), false);
 if (TOTAL_PORTS > 13 && reportPINs[13]) outputPort(13, readPort(13, portConfigInputs[13]), false);
 if (TOTAL_PORTS > 14 && reportPINs[14]) outputPort(14, readPort(14, portConfigInputs[14]), false);
 if (TOTAL_PORTS > 15 && reportPINs[15]) outputPort(15, readPort(15, portConfigInputs[15]), false);
}

// -----------------------------------------------------------------------------
/* sets the pin mode to the correct state and sets the relevant bits in the
* two bit-arrays that track Digital I/O and PWM status
*/
void setPinModeCallback(byte pin, int mode)
{
 switch(mode) {
   case INPUT:
     if (IS_PIN_DIGITAL(pin)) {
       pinMode(PIN_TO_DIGITAL(pin), INPUT); // disable output driver
       digitalWrite(PIN_TO_DIGITAL(pin), LOW); // disable internal pull-ups
       pinConfig[pin] = INPUT;
     }
     break;
   case OUTPUT:
     if (IS_PIN_DIGITAL(pin)) {
       digitalWrite(PIN_TO_DIGITAL(pin), LOW); // disable PWM
       pinMode(PIN_TO_DIGITAL(pin), OUTPUT);
       pinConfig[pin] = OUTPUT;
     }
     break;
   default:
     Firmata.sendString("Unknown pin mode"); // TODO: put error msgs in EEPROM
 }
 // TODO: save status to EEPROM here, if changed
}

void digitalWriteCallback(byte port, int value)
{
 byte pin, lastPin, mask=1, pinWriteMask=0;

 if (port < TOTAL_PORTS) {
   // create a mask of the pins on this port that are writable.
   lastPin = port*8+8;
   if (lastPin > TOTAL_PINS) lastPin = TOTAL_PINS;
   for (pin=port*8; pin < lastPin; pin++) {
     // do not disturb non-digital pins (eg, Rx & Tx)
     if (IS_PIN_DIGITAL(pin)) {
       // only write to OUTPUT and INPUT (enables pullup)
       // do not touch pins in PWM, ANALOG, SERVO or other modes
       if (pinConfig[pin] == OUTPUT || pinConfig[pin] == INPUT) {
         pinWriteMask |= mask;
         pinState[pin] = ((byte)value & mask) ? 1 : 0;
       }
     }
     mask = mask << 1;
   }
   writePort(port, (byte)value, pinWriteMask);
 }
}


void reportDigitalCallback(byte port, int value)
{
 if (port < TOTAL_PORTS) {
   reportPINs[port] = (byte)value;
 }
 // do not disable analog reporting on these 8 pins, to allow some
 // pins used for digital, others analog.  Instead, allow both types
 // of reporting to be enabled, but check if the pin is configured
 // as analog when sampling the analog inputs.  Likewise, while
 // scanning digital pins, portConfigInputs will mask off values from any
 // pins configured as analog
}

void sysexCallback(byte command, byte argc, byte *argv)
{
 switch(command) {

   break;
 case CAPABILITY_QUERY:
   Serial.write(START_SYSEX);
   Serial.write(CAPABILITY_RESPONSE);
   for (byte pin=0; pin < TOTAL_PINS; pin++) {
     if (IS_PIN_DIGITAL(pin)) {
       Serial.write((byte)INPUT);
       Serial.write(1);
       Serial.write((byte)OUTPUT);
       Serial.write(1);
     }
     Serial.write(127);
   }
   Serial.write(END_SYSEX);
   break;
 case PIN_STATE_QUERY:
   if (argc > 0) {
     byte pin=argv[0];
     Serial.write(START_SYSEX);
     Serial.write(PIN_STATE_RESPONSE);
     Serial.write(pin);
     if (pin < TOTAL_PINS) {
       Serial.write((byte)pinConfig[pin]);
  Serial.write((byte)pinState[pin] & 0x7F);
  if (pinState[pin] & 0xFF80) Serial.write((byte)(pinState[pin] >> 7) & 0x7F);
  if (pinState[pin] & 0xC000) Serial.write((byte)(pinState[pin] >> 14) & 0x7F);
     }
     Serial.write(END_SYSEX);
   }
   break;
 }
}

void setup()
{
 byte i;

 Firmata.setFirmwareVersion(2, 2);

// Firmata.attach(ANALOG_MESSAGE, analogWriteCallback);
 Firmata.attach(DIGITAL_MESSAGE, digitalWriteCallback);
// Firmata.attach(REPORT_ANALOG, reportAnalogCallback);
 Firmata.attach(REPORT_DIGITAL, reportDigitalCallback);
 Firmata.attach(SET_PIN_MODE, setPinModeCallback);
 Firmata.attach(START_SYSEX, sysexCallback);

 // TODO: load state from EEPROM here

 /* these are initialized to zero by the compiler startup code
 for (i=0; i < TOTAL_PORTS; i++) {
   reportPINs[i] = false;
   portConfigInputs[i] = 0;
   previousPINs[i] = 0;
 }
 */
 for (i=0; i < TOTAL_PINS; i++) {
   if (IS_PIN_ANALOG(i)) {
     // turns off pullup, configures everything
     setPinModeCallback(i, ANALOG);
   } else {
     // sets the output to 0, configures portConfigInputs
     setPinModeCallback(i, OUTPUT);
   }
 }
 // by defult, do not report any analog inputs
 analogInputsToReport = 0;

 Firmata.begin(57600);

 /* send digital inputs to set the initial state on the host computer,
  * since once in the loop(), this firmware will only send on change */
 for (i=0; i < TOTAL_PORTS; i++) {
   outputPort(i, readPort(i, portConfigInputs[i]), true);
 }
 
 /* init the toggleLed counter */
 toggleMillis = millis();
 pinMode(13, OUTPUT);
}

void loop()
{
 byte pin, analogPin;

 /* DIGITALREAD - as fast as possible, check for changes and output them to the
  * FTDI buffer using Serial.print()  */
 checkDigitalInputs();  

 //XXX: hack Firmata to blink until serial command arrives
 dataOnSerial = Firmata.available();
 if (dataOnSerial > 0 && !firstCommand) {
   firstCommand = true;
 }
 //XXX: do the blink if the first command hasn't arrived yet
 //     configures pin 13 as output and then back as input
 if (!firstCommand) {
   toggleLed();
 }
 
 /* SERIALREAD - processing incoming messagse as soon as possible, while still
  * checking digital inputs.  */
 while(dataOnSerial) {
   Firmata.processInput();
   dataOnSerial = Firmata.available();
 }
 
 /* SEND FTDI WRITE BUFFER - make sure that the FTDI buffer doesn't go over
  * 60 bytes. use a timer to sending an event character every 4 ms to
  * trigger the buffer to dump. */
}
