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
}

void loop() {
  if (client.connected()) {
    // Create a JSON object
    StaticJsonDocument<400> jsonDocument; // Adjust buffer size as needed
    jsonDocument["id"] = "did:iota:test1";
    jsonDocument["controller"] = "did:iota:root";
    jsonDocument["proof"] = "NEEDS_PROOF";

    // Create a nested JSON object
    JsonObject verificationMethod = jsonDocument.createNestedObject("verificationMethod");
    verificationMethod["id"] = "did:iota:test1/path";
    verificationMethod["type"] = "Ed25519VerificationKey2018";
    verificationMethod["controller"] = "did:iota:root";
    verificationMethod["publicKeyBinary"] = "";

    // Serialize JSON object to a string
    String jsonString;
    serializeJson(jsonDocument, jsonString);

    // Send JSON string to server
    client.println(jsonString);
    Serial.println("JSON message sent to server: " + jsonString);

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
