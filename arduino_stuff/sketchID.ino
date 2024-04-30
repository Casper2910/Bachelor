#include <ArduinoUniqueID.h>

String ID = ""; // Declare ID variable outside of any function and initialize it

void setup() {
  Serial.begin(9600);
  UniqueIDdump(Serial);
  for (size_t i = 0; i < UniqueIDsize; i++) {
    ID += String(UniqueID[i]);
  }
  
  Serial.println(ID);
}
void loop() {
  Serial.println(ID); // Print ID in the loop
  delay(5000);
}
