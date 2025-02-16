#include <Servo.h>         // Include the Servo library
#include <SoftwareSerial.h> // Include SoftwareSerial library

// Pin definitions
#define SIM800_TX 2
#define SIM800_RX 3
#define GAS_SENSOR_PIN A0
#define RELAY_PIN 9
#define BUZZER_PIN 8

// Threshold for gas detection
int gasThreshold = 150;

// SIM800C setup
SoftwareSerial sim800SS(SIM800_TX, SIM800_RX);
char PHONE_1[21] = "7004012040"; // Replace with your phone number
char gasalert[141] = "Gas Leakage Detected";

// Servo setup
Servo myServo;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  sim800SS.begin(9600);

  // Initialize Servo
  myServo.attach(10);  // Attach servo to pin 10
  myServo.write(0);    // Set initial position to 0 degrees

  // Initialize relay and buzzer
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  Serial.println("System Ready!");
}

void loop() {
  int gasLevel = analogRead(GAS_SENSOR_PIN); // Read gas sensor value

  Serial.print("Gas Level: ");
  Serial.println(gasLevel);

  if (gasLevel < gasThreshold) {
    // Gas detected, activate alert
    Serial.println("Gas detected!");

    // Move servo to 90 degrees
    myServo.write(90);
    delay(2000); // Keep servo at 90 degrees for 2 seconds

    // Activate relay and buzzer
    digitalWrite(RELAY_PIN, HIGH);
    digitalWrite(BUZZER_PIN, HIGH);

    // Send SMS and make a call
    send_multi_sms();
    make_multi_call();

    // Reset servo position
    myServo.write(0);
  } else {
    // Reset relay and buzzer if no gas detected
    digitalWrite(RELAY_PIN, LOW);
    digitalWrite(BUZZER_PIN, LOW);
  }

  delay(500); // Delay before next reading
}

void send_multi_sms() {
  Serial.println("Sending SMS...");
  send_sms(PHONE_1, gasalert);
}

void send_sms(String phone, String message) {
  sim800SS.println("AT+CMGF=1"); // Set SMS mode
  delay(100);
  sim800SS.println("AT+CMGS=\"" + phone + "\"");
  delay(100);
  sim800SS.print(message);
  sim800SS.write(26); // Send Ctrl+Z to send SMS
  delay(5000); // Wait for SMS to send
  Serial.println("SMS Sent!");
}

void make_multi_call() {
  Serial.println("Making call...");
  make_call(PHONE_1);
}

void make_call(String phone) {
  sim800SS.println("ATD" + phone + ";");
  delay(20000); // Wait for call duration
  sim800SS.println("ATH"); // Hang up
  delay(1000);
  Serial.println("Call Ended!");
}