//INCLUDE STATEMENTS
// Including the libraries with the functions we need for this program
#include <Wire.h>
#include <seeed-kit.h>
#include <Servo.h>

//FUNCTION DECLARATIONS - Declarations for functions defined in this file
/*TODO - Declare the function you plan to write here */

//MAIN - Every C++ program beings with main() function
int main() {

  //Required at beginning of each lab file - initialize Arduino and other hardware.
  init();
  
  //Initialize components
  /*TODO - Insert function calls to any components you are using that require initialization
  eg. LCD screen, RGBA LED, LED Bar, Servo Motor
  Consult 1020 Arduino reference for further details */
  lcdInit();
  rgbLedInit(3, 1);
  servoInit(7);
  randomSeed(A4);

  
  //Call function containing implemented code
  /*TODO - Implement function call here */
  //adjustLight(500, A0);
  adjustSteering(A2);
 
  //Every main() needs to return a value because its type is not void
  return 0;
}


//OTHER FUNCTION DEFINITIONS - Defining functions declared above (and possibly called from main())

/**
 * This function continuously adjusts the brightness of an RGBA LED based on the sensed 
 * brightness level, in an attempt to keep the overall brightness constant
 *
 * @param     b     the desired brightness level 
 *                  @pre 0 <= b <= 800
 * @param     a     the analog port into which the light sensor is connected 
 *                  @pre must be in [A0, A1, A2, A3]
 *                  
 * @returns         nothing
 * 
 * @modifies        adjusts brightness of RGBA LED
 * @modifies        output sensed brightness level AND RGBA LED brightness
 *                  setting, as text to LCD screen
 */
/*TODO - Implement adjustLight() based on contract specification */
void adjustLight(int b, int a)
{
  int b_sense = analogRead(a);
  int b_diff = b - b_sense;
  int b_set = b_diff/2;
  if (b_diff < 0) //Too bright out, dim light
    b_set = 0;
  rgbLedHSB(0, 0, 0, b_set/800.0);

  while (true)
  {
    //Change brightness of RGBA LED to compensate for b_diff
    lcdClear();
    lcdPrint(b_sense);
    lcdPrint(",");
    lcdPrint(b_diff);
    lcdPrint(",");
    b_set = b_set + b_diff/2;
    lcdPrint(b_set);
    lcdPrint(",");
    if (b_set > 800)
      b_set = 800;
    else if (b_set < 0)
      b_set = 0;
    rgbLedHSB(0, 0, 0, b_set/800.0);
    lcdPrint(b_set);
    delay(1000);
    
    //Get new brightness level and do math
    b_sense = analogRead(a);
    b_diff = b - b_sense;
  }
}

/**
 * This function continuously adjusts the calculated steering direction of our vessel
 * in an attempt to continue on a specified heading of d degrees. The direction of the
 * current is simulated/changed by the input of the rotary dial.
 *
 * @param     a     the analog port into which the light sensor is connected 
 *                  @pre must be in [A0, A1, A2, A3]
 *                  
 * @returns         nothing
 * 
 * @modifies        adjusts the direction of the servo motor position to show vessel steering
 * @modifies        outputs direction set to servo motor AND calculated overall
 *                  vessel direction, as text to LCD screen
 */
/*TODO - Implement adjustSteering() based on contract specification */
void adjustSteering(int a)
{
  const int DIR = 0;
  int current_dir = currentRead(a);

  int steering_dir = -current_dir;

  while (true) {
    lcdClear();
    lcdPrint(((steering_dir + 90)/5)*5);
    lcdPrint(",");
    servoMove(((steering_dir + 90)/5)*5);
    current_dir = currentRead(a);
    lcdPrint(current_dir);
    steering_dir = -current_dir;
    delay(1000);
  }

}

int currentRead(int a)
{
  int r = analogRead(a);

  //Convert r [0, 1023] to direction [-90, 90]
  int d = r*(180/1023.0) - 90; // + random(-5, 6);

  return d;
}

