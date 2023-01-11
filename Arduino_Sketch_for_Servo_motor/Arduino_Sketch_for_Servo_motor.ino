#include <cvzone.h>

SerialData serialData(1,3);

int val[1];

void setup() {

  serialData.begin(9600);
  pinMode(11,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
 serialData.Get(val);
 analogWrite(11,val[0]);
}
