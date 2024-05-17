#include <WiFiNINA.h>
#include <ArduinoJson.h>
#include <Arduino_MKRIoTCarrier.h>
#include <ArduinoUniqueID.h>

char ssid[] = "wifi";       // your network SSID (name)
char pass[] = "pass";    // your network password
int status = WL_IDLE_STATUS;    // the WiFi status

IPAddress server(192, 168, 0, 155); // IP address of the target device
int serverPort = 8081;              // port of the target device
int listenPort = 8082;              // port to listen for incoming requests

WiFiClient client;
WiFiServer wifiServer(listenPort);  // Define WiFiServer object to listen on port 8082

MKRIoTCarrier carrier;

String DID;                // Variable for DID
String DeviceID;           // Variable for unique identifier for device
String DID_Document;       // Variable to store the DID document as a JSON string

void setup() {
  Serial.begin(9600);

  // Initialize the MKRIoTCarrier
  carrier.begin();

  connectToWiFi(); // Connect to WiFi network

  // Generate DID
  getDeviceID();
  DID = "did:iota:test" + DeviceID;

  // Generate DID Document
  generateDIDDocument();

  // Start listening for incoming connections
  wifiServer.begin();

  Serial.println("Setup complete");
}

void loop() {
  if (client.connected()) {
    Serial.println("CONNECTED");

    // Create a JSON object for sending data
    StaticJsonDocument<100> jsonDID;
    jsonDID["DID"] = DID;
    float temp = carrier.Env.readTemperature();
    jsonDID["temperature"] = temp;

    // Serialize JSON object to a string
    String jsonData;
    serializeJson(jsonDID, jsonData);

    Serial.println("jsonData: " + jsonData);

    // Send JSON string to server
    client.print(jsonData);

    // Check if there is any incoming request from the server
    WiFiClient serverClient = wifiServer.available();
    if (serverClient) {
      String request = serverClient.readStringUntil('\r'); // Read the request
      Serial.println("Request received: " + request);

      if (request == "request-did-doc") {
        Serial.println("Received request for DID document");
        sendDIDDocument(); // Send the DID document to the server
      }

      serverClient.stop(); // Close the connection with the server
    }

    delay(2000); // Wait before sending next data
  } else {
    Serial.println("NOT CONNECTED");
    if (!connectToServer()) {
      Serial.println("Connection lost. Reconnecting...");
      delay(5000); // Wait before attempting to reconnect
    }
  }
}

void connectToWiFi() {
  Serial.print("Attempting to connect to SSID: ");
  Serial.println(ssid);
  status = WiFi.begin(ssid, pass);
  int attempts = 0;
  while (status != WL_CONNECTED && attempts < 5) {
    Serial.println("Connection attempt failed. Retrying...");
    delay(5000);  // Wait before retrying
    status = WiFi.begin(ssid, pass);
    attempts++;
  }

  if (status == WL_CONNECTED) {
    Serial.println("Connected to WiFi");
  } else {
    Serial.println("Failed to connect to WiFi");
    // You might want to implement a mechanism to handle failure, e.g., enter a sleep mode.
  }
}

bool connectToServer() {
  if (client.connect(server, serverPort)) {
    Serial.println("Connected to server");
    return true;
  } else {
    Serial.println("Connection to server failed");
    return false;
  }
}

void getDeviceID() {
  UniqueIDdump(Serial);
  for (size_t i = 0; i < UniqueIDsize; i++) {
    DeviceID += String(UniqueID[i]);
  }
}

void generateDIDDocument() {
  // Create a JSON object for DID document
  StaticJsonDocument<200> jsonDocument;
  jsonDocument["@context"] = "https://w3id.org/security/suites/ed25519-2020/v1";
  jsonDocument["id"] = DID;
  jsonDocument["controller"] = "did:iota:root";
  jsonDocument["serial"] = DeviceID;
  jsonDocument["proof"] = "NEEDS_PROOF";

  // Create a nested JSON object for verification method
  JsonObject verificationMethod = jsonDocument.createNestedObject("verificationMethod");
  verificationMethod["id"] = "did:iota:test1/path";
  verificationMethod["type"] = "Ed25519VerificationKey2018";
  verificationMethod["controller"] = "did:iota:root";
  verificationMethod["publicKey"] = ""; // Add the actual public key if available

  // Serialize JSON object to a string
  serializeJson(jsonDocument, DID_Document);
}

void sendDIDDocument() {
  // Send the DID document to the server
  client.print(DID_Document);
  Serial.println("Sent DID document to server: " + DID_Document);
}
