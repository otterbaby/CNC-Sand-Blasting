#include "SignalDecrypt.h"
#include "MotorStateMachine.h"


/*
 * This program receives instructions over serial port to set in motion two
 * stepper motors on a TMC2130 driver.
 * @author: Wladimir Reiswich
 */

const int interval = 30;
char com_buff[64];

#define REC_ON    PORTD = PORTD | B00010000 
#define REC_OFF   PORTD = PORTD & B11101111
#define SIG_ON    PORTC = PORTC | B01000000
#define SIG_OFF   PORTC = PORTC & B10111111
/*
 * Generates the rectangle signal for the stepper motor (PIN 6 and 4) for each
 * motor independently.
 * Once done, a cleanup routine is executed and prepared for the next command.
 */
void step_machine(){

  int step_is = 0;
  while (step_is < step_to_go){
    REC_ON;
    SIG_ON;
    delay(interval);
    REC_OFF;
    SIG_OFF;
    delay(interval);
    step_is++;
  }
  
  clean_up();
}


/*
 * The FSM is reset and original command string is sent back as acknowledgement.
 * This function is called at the end of an executed command or as a reset.
 */
void clean_up() {
  current_input.run = low;
  state_handler();
  Serial.print(com_buff);
  memset(com_buff,0,64);
}

/*
 * This is an interrupt that gets called when serial buffer receives data.
 * It starts the event chain of calling the signal_handler()
 */
void serialEvent(){
  
    int i = Serial.readBytesUntil('$',com_buff, 20);
    com_buff[i] = '$';
    signal_handler(com_buff);
    state_handler();
    step_machine();
      
}

/*
 * Setup of the COM port and the output pins.
 */
void setup() {
  Serial.begin(9600);
  delay(100);
  current_input.run = 0;
  DDRD = DDRD | B00111000;
  DDRC = DDRC | B00010010;
  DDRB = DDRB | B00111000; //pin 5: SCK, pin 4: SDO, pin 3: SDI
  PORTB = PORTB | B00111000; //(SCK and SDI high for standard operation)
}

//only acts when the flag (current_input.run) is HIGH
void loop() {
  //if(current_input.run)
    
}
