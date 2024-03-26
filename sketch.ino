#include <WiFiNINA.h>              // Include the WiFi library
#include <SPI.h>                   // Include the SPI library
#include <Arduino_MKRIoTCarrier.h> // Include the MKRIoTCarrier library

char ssid[] = "wifi";          // Your WiFi SSID
char pass[] = "pass";       // Your WiFi password
unsigned int localPort = 12345;    // Local port to listen on

MKRIoTCarrier carrier;
WiFiUDP udp;                       // Create a UDP instance

void setup() {
  carrier.begin();
  Serial.begin(9600);              // Initialize serial communication

  // Attempt to connect to WiFi network
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    Serial.println("Attempting to connect to WiFi...");
    delay(5000);                   // Retry every 5 seconds if connection fails
  }

  Serial.println("Connected to WiFi");

  // Begin UDP communication
  udp.begin(localPort);
  Serial.println("UDP server started");
}

void loop() {
  // Read temperature from sensor on the MKR IoT Carrier board
  float temperature = carrier.Env.readTemperature();

  // Print temperature to serial monitor
  Serial.print("Temperature: ");
  Serial.println(temperature);

  // Broadcast temperature data using UDP
  sendDataOverUDP(temperature);

  delay(5000); // Delay for 5 seconds before next reading
}

void sendDataOverUDP(float temp) {
  // Broadcast temperature data over UDP
  Serial.println("Sending data over UDP...");

  IPAddress broadcastIP(255, 255, 255, 255); // Broadcast address for all devices on the network
  udp.beginPacket(broadcastIP, localPort);
  udp.print(temp);
  udp.endPacket();

  Serial.println("Data sent over UDP");
}
