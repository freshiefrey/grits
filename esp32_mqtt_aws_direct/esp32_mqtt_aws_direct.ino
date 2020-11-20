#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>


// Update these with values suitable for your network.
const char* ssid = "Joust";
const char* password = "jljttm89";
const char* mqtt_server = "54.255.221.131";
//String
#define mqtt_port 1883
#define MQTT_USER "Daryl"
#define MQTT_PASSWORD "wmk9199"
//#define MQTT_SERIAL_PUBLISH_CH "/icircuit/ESP32/serialdata/tx"
#define MQTT_SERIAL_RECEIVER_CH "GRITS/Gesture"

WiFiClient wifiClient;

PubSubClient client(wifiClient);

//Pin setup
int motor1Pin1 = 27;
int motor1Pin2 = 26;
int motor2Pin1 = 33;
int motor2Pin2 = 32;
int led1 = 14;

//int enable1Pin = 15;
int mtr_ctrl_stat = 0;
int led_ctrl_stat = 0;
int led_prev_stat = 0;

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(), MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("connected");
      //Once connected, publish an announcement...
      //      client.publish("/icircuit/presence/ESP32/", "hello world");
      // ... and resubscribe
      client.subscribe(MQTT_SERIAL_RECEIVER_CH);
      Serial.println("subscribed to: ");
      Serial.println(MQTT_SERIAL_RECEIVER_CH);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte *payload, unsigned int length) {
  payload[length] = '\0';
  String s = (char*)payload;
  Serial.println(s);
  if (s == "\"Pushback\"") {
    mtr_ctrl_stat = 1;
  }
  if (s == "\"Buddha clap\""){
    Serial.println("Buddha clap detected!");
    led_ctrl_stat = !led_ctrl_stat;
  }
}

void motor_ctrl() {
  Serial.println("moving motor");
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin2, HIGH);
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor2Pin1, LOW);
  delay(1000);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin2, LOW);
  delay(1000);
  Serial.println("motor stopped");
}

void led_ctrl() {
  Serial.println("toggle led");
  led_prev_stat = led_ctrl_stat;
  if (led_ctrl_stat == 1){
    digitalWrite(led1, HIGH);
  }
  else{
    digitalWrite(led1, LOW);
  }
}

void setup() {
  //motor pin setup
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  
  pinMode(led1, OUTPUT);

  Serial.begin(115200);
  Serial.setTimeout(500);// Set time out for
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  reconnect();
}

void loop() {
  client.loop();
//  mtr_ctrl_stat = 1;
  if (mtr_ctrl_stat == 1) {
    mtr_ctrl_stat = 0;
    motor_ctrl();
  }
  while (led_ctrl_stat != led_prev_stat){
    led_ctrl();
  }
}
