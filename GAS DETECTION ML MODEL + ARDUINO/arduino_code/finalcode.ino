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

// Function to calculate PPM from raw sensor reading
float calculatePPM(int rawValue) {
  float voltage = (rawValue / 1024.0) * 5.0; // Convert to voltage (assuming 5V system)
  float ppm = voltage * 100;                // Example conversion, tune based on calibration
  return ppm;
}

// Functions for label determination
int determineLeakSeverity(float ppm) {
  if (ppm > 300) return 1; // Low
  if (ppm > 150) return 2; // Medium
  return 3;                // High
}

int determineFireRisk(float ppm) {
  if (ppm > 250) return 1; // Low
  return 2;                // High
}

int determineFlammability(float ppm) {
  if (ppm > 250) return 1; // Low
  return 2;                // High
}

String determineGasType(float ppm) {
  if (ppm > 150) return "Non-flammable";
  return "Flammable";
}

// Function to send SMS
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

// Function to make a call
void make_call(String phone) {
  sim800SS.println("ATD" + phone + ";");
  delay(20000); // Wait for call duration
  sim800SS.println("ATH"); // Hang up
  delay(1000);
  Serial.println("Call Ended!");
}

// Function to send multiple SMS
void send_multi_sms() {
  Serial.println("Sending SMS...");
  send_sms(PHONE_1, gasalert);
}

// Function to make multiple calls
void make_multi_call() {
  Serial.println("Making call...");
  make_call(PHONE_1);
}

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
  float ppm = calculatePPM(gasLevel);       // Calculate PPM from raw sensor value

  // Print readings to serial monitor
  Serial.print("Gas Level (Raw): ");
  Serial.println(gasLevel);
  Serial.print("Gas Level (PPM): ");
  Serial.println(ppm);

  // Determine labels
  int leakSeverity = determineLeakSeverity(ppm);
  int fireRisk = determineFireRisk(ppm);
  int flammability = determineFlammability(ppm);
  String gasType = determineGasType(ppm);

  // Print labels to serial monitor
  Serial.print("Leak Severity: ");
  Serial.println(leakSeverity);
  Serial.print("Fire Risk: ");
  Serial.println(fireRisk);
  Serial.print("Flammability: ");
  Serial.println(flammability);
  Serial.print("Gas Type: ");
  Serial.println(gasType);

  // Perform actions based on fire risk
  if (fireRisk == 2) {
    // High fire risk detected
    Serial.println("High fire risk detected!");
    myServo.write(90);          // Move servo to 90 degrees
    delay(2000);                // Keep servo at 90 degrees for 2 seconds
    digitalWrite(RELAY_PIN, HIGH);  // Activate relay
    digitalWrite(BUZZER_PIN, HIGH); // Activate buzzer
    send_multi_sms();           // Send SMS alert
    make_multi_call();          // Make call alert
    myServo.write(0);           // Reset servo position
  } else {
    // No fire risk, reset relay and buzzer
    digitalWrite(RELAY_PIN, LOW);
    digitalWrite(BUZZER_PIN, LOW);
  }

  delay(500); // Delay before next reading
}
