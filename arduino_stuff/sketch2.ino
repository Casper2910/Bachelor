#include <WiFiNINA.h>
#include <ArduinoJson.h>

char ssid[] = "wifi";      // your network SSID (name)
char pass[] = "pass";   // your network password
int status = WL_IDLE_STATUS;          // the WiFi status

IPAddress server(192, 168, 0, 133);   // IP address of the target device
int port = 8080;                        // port of the target device

WiFiClient client;

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

  // Generate hash for id based on serial number:
  uint32_t hashValue = hash32((const uint8_t *)& serialNumber, sizeof(serialNumber));
  // Convert the hash value to a hexadecimal string
  char hashString[9]; // 8 characters for a 32-bit hash plus 1 for null terminator
  sprintf(hashString, "%08X", hashValue); // Convert hash value to hexadecimal string

  // Generate DID:
  DID = "did:iota:test" + String(hashValue);

  // Create a JSON object
    StaticJsonDocument<400> jsonDocument; // Adjust buffer size as needed
    jsonDocument["id"] = DID;
    jsonDocument["controller"] = "did:iota:root";
    jsonDocument["serial"] = String(ESP.getChipId(), HEX));
    jsonDocument["proof"] = "NEEDS_PROOF";

    // Create a nested JSON object
    JsonObject verificationMethod = jsonDocument.createNestedObject("verificationMethod");
    verificationMethod["id"] = "did:iota:test1/path";
    verificationMethod["type"] = "Ed25519VerificationKey2018";
    verificationMethod["controller"] = "did:iota:root";
    verificationMethod["publicKey"] = "";

    // Serialize JSON object to a string
    String jsonString;
    serializeJson(jsonDocument, jsonString);
}

void loop() {
  if (client.connected()) {
    // Send JSON string to server
    client.println(DID);
    Serial.println("Message sent to server:" + DID);
    delay(500)

    String dataReceived = Serial.readStringUntil('\n'); // Read data until newline character
    // Split string into parts based on comma separator
    int commaIndex = dataReceived.indexOf(',');
    String stringData = dataReceived.substring(0, commaIndex);
    int iterationNumber = dataReceived.substring(commaIndex + 1).toInt();

    if (stringData.startsWith('request-did-doc'){

    }

  }
    // Wait a bit before sending the next message
    delay(5000);
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
