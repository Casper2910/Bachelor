#include <WiFiNINA.h>
#include <ArduinoJson.h>
#include <Adafruit_ESP8266.h>
#include <Arduino_MKRIoTCarrier.h>
#include <ArduinoUniqueID.h>

char ssid[] = "Persille";      // your network SSID (name)
char pass[] = "ScottsTots5";   // your network password
int status = WL_IDLE_STATUS;          // the WiFi status

IPAddress server(192, 168, 0, 133);   // IP address of the target device
int port = 8080;                        // port of the target device

WiFiClient client;
MKRIoTCarrier carrier;

String DID;                 // Variable for DID
String DID_Document_String; // Variable for DID document as string
String DeviceID;            // Variable for unique identifier for device

void setup() {
  Serial.begin(9600);

  // attempt to connect to WiFi network
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(5000);  // wait 5 seconds for connection
  }
  Serial.println("Connected to WiFi");

  // Connect to server
  Serial.print("Attempting to connect to server: ");
  Serial.println(server);
  if (client.connect(server, port)) {
    Serial.println("Connected to server");
  } else {
    Serial.println("Connection failed");
  }

  // Get unique identifier
  UniqueIDdump(Serial);
  for (size_t i = 0; i < UniqueIDsize; i++) {
    DeviceID += String(UniqueID[i]);
  }

  // Generate DID:
  DID = "did:iota:test" + DeviceID;

  // Create a JSON object
  StaticJsonDocument<400> jsonDocument; // Adjust buffer size as needed
  jsonDocument["id"] = DID;
  jsonDocument["controller"] = "did:iota:root";
  jsonDocument["serial"] = DeviceID;
  jsonDocument["proof"] = "NEEDS_PROOF";

  // Create a nested JSON object
  JsonObject verificationMethod = jsonDocument.createNestedObject("verificationMethod");
  verificationMethod["id"] = "did:iota:test1/path";
  verificationMethod["type"] = "Ed25519VerificationKey2018";
  verificationMethod["controller"] = "did:iota:root";
  verificationMethod["publicKey"] = "";

  // Serialize JSON object to a string
  serializeJson(jsonDocument, DID_Document_String);
}

void loop() {
  if (client.connected()) {
    // Create a JSON object for DID
    StaticJsonDocument<400> jsonDID; // Adjust buffer size as needed
    jsonDID["DID"] = DID;

    // Serialize JSON object to a string
    String jsonData;
    serializeJson(jsonDID, jsonData);

    // Send JSON string to server
    client.println(jsonData);
    Serial.println("Message sent to server:" + jsonData);
    delay(500);

    String dataReceived = Serial.readStringUntil('\n'); // Read data until newline character
    // Split string into parts based on comma separator
    int commaIndex = dataReceived.indexOf(',');
    String stringData = dataReceived.substring(0, commaIndex);
    int iterationNumber = dataReceived.substring(commaIndex + 1).toInt();

    // Send DID document if server requests
    if (stringData.startsWith("request-did-doc")) {
      client.println(DID_Document_String);
      delay(5000);
    }

    // Send temperature data to server
    client.println(carrier.Env.readTemperature());

  } else {
    // If the connection is lost, attempt to reconnect
    Serial.println("Connection lost. Reconnecting...");
    if (client.connect(server, port)) {
      Serial.println("Reconnected to server");
    } else {
      Serial.println("Reconnection failed");
    }
  }
}
