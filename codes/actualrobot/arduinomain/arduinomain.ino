
//zoomkat 11-12-13 String capture and parsing
//from serial port input (via serial monitor)
//and print result out serial port
//copy test strings and use ctrl/v to paste in
//serial monitor if desired
// * is used as the data string delimiter
// , is used to delimit individual data
#include<Servo.h>

Servo m1;  // create servo object to control a servo
Servo m2;// twelve servo objects can be created on most boards
Servo m3;
Servo m4;  // create servo object to control a servo
Servo m5;// twelve servo objects can be created on most boards
Servo m6;
Servo m7;  // create servo object to control a servo
Servo m8;// twelve servo objects can be created on most boards
Servo m9;
Servo m10;  // create servo object to control a servo
Servo m11;// twelve servo objects can be created on most boards
Servo m12;
String readString; //main captured String
// 90,90,180,90,90,180,90,90,0,90,10,180;
int angle1 = 90; //data String
int angle2 = 90; //data String
int angle3 = 180; //data String
int angle4 = 90; //data String
int angle5 = 90; //data String
int angle6 = 180; //data String
int angle7 = 90; //data String
int angle8 = 90; //data String
int angle9 = 0; //data String
int angle10 = 90; //data String
int angle11 = 10; //data String
int angle12 = 180; //data String
int ind1; // , locations
int ind2;
int ind3;
int ind4;
int ind5;
int ind6; // , locations
int ind7;
int ind8;
int ind9;
int ind10; // , locations
int ind11;
int ind12;
void setup() {
  m1.attach(51);
  m2.attach(53);// attaches the servo on pin 9 to the servo object
  m3.attach(52);
  m4.attach(32);
  m5.attach(31);// attaches the servo on pin 9 to the servo object
  m6.attach(33);
  m7.attach(26);
  m8.attach(27);// attaches the servo on pin 9 to the servo object
  m9.attach(25);
  m10.attach(45);
  m11.attach(47);// attaches the servo on pin 9 to the servo object
  m12.attach(46);
  Serial.begin(115200);

  Serial.println("ok");
}

void loop() {

  //expect a string like 90,low,15.6,125*
  //or 130,hi,7.2,389*

  if (Serial.available())  {
    char c = Serial.read();  //gets one byte from serial buffer
    if (c == ';') {
      //do stuff
      //      Serial.print("<");
      //      Serial.println(readString); //prints string to serial port out

      ind1 = readString.indexOf(',');  //finds location of first ,
      angle1 = (readString.substring(0, ind1)).toInt();   //captures first data String
      ind2 = readString.indexOf(',', ind1 + 1 ); //finds location of second ,
      angle2 = (readString.substring(ind1 + 1, ind2)).toInt(); //captures second data String
      ind3 = readString.indexOf(',', ind2 + 1 );
      angle3 = (readString.substring(ind2 + 1, ind3)).toInt();
      ind4 = readString.indexOf(',', ind3 + 1 );
      angle4 = (readString.substring(ind3 + 1, ind4)).toInt(); //captures remain part of data after last ,
      ind5 = readString.indexOf(',', ind4 + 1 );
      angle5 = (readString.substring(ind4 + 1, ind5)).toInt();
      ind6 = readString.indexOf(',', ind5 + 1 );
      angle6 = (readString.substring(ind5 + 1, ind6)).toInt();
      ind7 = readString.indexOf(',', ind6 + 1 );
      angle7 = (readString.substring(ind6 + 1, ind7)).toInt();
      ind8 = readString.indexOf(',', ind7 + 1 );
      angle8 = (readString.substring(ind7 + 1, ind8)).toInt();
      ind9 = readString.indexOf(',', ind8 + 1 );
      angle9 = (readString.substring(ind8 + 1, ind9)).toInt();
      ind10 = readString.indexOf(',', ind9 + 1 );
      angle10 = (readString.substring(ind9 + 1, ind10)).toInt();
      ind11 = readString.indexOf(',', ind10 + 1 );
      angle11 = (readString.substring(ind10 + 1, ind11)).toInt();
      ind12 = readString.indexOf(',', ind11 + 1 );
      angle12 = (readString.substring(ind11 + 1, ind12)).toInt();
      //      Serial.print("angle = ");
      //      int x = angle.toInt()%180;
//      Serial.println(angle1);
//      Serial.println(angle2);
//      Serial.println(angle3);
//      Serial.println(angle4);
//      Serial.println(angle5);
//      Serial.println(angle6);
//      Serial.println(angle7);
//      Serial.println(angle8);
//      Serial.println(angle9);
//      Serial.println(angle10);
//      Serial.println(angle11);
//      Serial.println(angle12);
      m1.write(angle1);
      m2.write(angle2);
      m3.write(angle3);
      m4.write(angle4);
      m5.write(angle5);
      m6.write(angle6);
      m7.write(angle7);
      m8.write(angle8);
      m9.write(angle9);
      m10.write(angle10);
      m11.write(angle11);
      m12.write(angle12);
      delay(10);
      Serial.println("ok");
      readString = ""; //clears variable for new input
      //      angle="";
      //      fuel="";
      //      speed1="";
      //      altidude="";
    }
    else {
      readString += c; //makes the string readString
    }
  }
}
