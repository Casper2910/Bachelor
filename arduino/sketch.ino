#include <WiFiNINA.h>
#include <ArduinoJson.h>
#include <Arduino_MKRIoTCarrier.h>
#include <ArduinoUniqueID.h>

char ssid[] = "wifi";       // your network SSID (name)
char pass[] = "pass";       // your network password
int status = WL_IDLE_STATUS; // the WiFi status

IPAddress server(192, 168, 0, 155); // IP address of the target device
int serverPort = 8081;              // port of the target device
int listenPort = 8082;              // port to listen for incoming requests

WiFiClient client;
WiFiServer wifiServer(listenPort);  // Define WiFiServer object to listen on port 8082

MKRIoTCarrier carrier;

String DID;                 // Variable for DID
String DID_Document_String; // Variable for DID document as string
String DeviceID;            // Variable for unique identifier for device

void setup() {
  Serial.begin(9600);

  // Connect to WiFi network
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
  while (!connectToServer()) {
    Serial.println("Connection failed. Reconnecting...");
    delay(5000);
  }

  // Get unique identifier
  UniqueIDdump(Serial);
  for (size_t i = 0; i < UniqueIDsize; i++) {
    DeviceID += String(UniqueID[i]);
  }

  // Generate DID
  DID = "did:iota:test" + DeviceID;

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
  verificationMethod["publicKey"] = "";

  // Serialize JSON object to a string
  serializeJson(jsonDocument, DID_Document_String);

  // Initialize the MKR IoT Carrier
  if (!carrier.begin()) {
    Serial.println("Carrier initialization failed. Please check your carrier connections.");
    while (1); // Halt the program
  } else {
    Serial.println("Carrier initialized successfully.");
  }

  wifiServer.begin(); // Start listening for incoming connections
}

void loop() {
  // Check if the client is connected
  if (!client.connected()) {
    // If not connected, attempt to reconnect
    if (!connectToServer()) {
      Serial.println("Connection lost. Reconnecting...");
    }
  } else {
    // Create a JSON object for DID
    StaticJsonDocument<200> jsonDID;

    // Populate JSON object with data
    jsonDID["DID"] = DID;
    float temp = carrier.Env.readTemperature();
    jsonDID["temperature"] = temp;

    // Serialize JSON object to a string
    String jsonData;
    serializeJson(jsonDID, jsonData);

    // Send JSON string to server
    client.print(jsonData);
    delay(2000);

    // Check if there is any incoming request from the server
    WiFiClient serverClient = wifiServer.available();
    if (serverClient) {
      String request = serverClient.readStringUntil('\r'); // Read the request
      Serial.println("Request received: " + request);
      int check = request.toInt();

      // If the request is 'request-did-doc', send the DID document to the server
      // Check if the request is equal to "request-did-doc"
      // 69420 is the number to look for
      if (check == 69420) {
        Serial.println("Received request for DID document");
        client.print(DID_Document_String);
        Serial.println("Sent DID document to server: " + DID_Document_String);
        delay(10000); // Delay to prevent flooding the server
      }

      serverClient.stop(); // Close the connection with the server
    }
  }
}

bool connectToServer() {
  if (client.connect(server, serverPort)) {
    Serial.println("Connected to server");
    return true;
  } else {
    Serial.println("Connection failed");
    return false;
  }
}
