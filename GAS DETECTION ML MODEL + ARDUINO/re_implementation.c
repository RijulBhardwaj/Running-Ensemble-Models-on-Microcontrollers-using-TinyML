#include <Servo.h>
#include <SoftwareSerial.h>
#include <RandomForestModel.h>

// Hardware Definitions
#define SIM800_TX 2
#define SIM800_RX 3
#define GAS_SENSOR_PIN A0
#define RELAY_PIN 9
#define BUZZER_PIN 8
#define FAN_PIN 7
#define POWER_CHECK_PIN A1

// Safety Thresholds
const int LEL_LPG = 20000;    // Lower Explosive Limit for LPG (ppm)
const int CALIBRATION_THRESHOLD = 15; // % variation for drift detection
const unsigned long PERSISTENT_LEAK_TIME = 300000; // 5 minutes

// Global Variables
float prevPPM[3] = {0};       // Circular buffer for rate calculation
unsigned long lastSensorCheck = 0;
unsigned long persistentLeakStart = 0;
bool fanActive = false;

// Model Initialization (Trained coefficients)
RandomForestModel riskModel(0.12, 0.25, 1.8, 0.05);

SoftwareSerial sim800SS(SIM800_TX, SIM800_RX);
Servo gasValveServo;

// Phone Configuration
char PHONE_1[21] = "7004012040";
String alertMessage = "DANGER! Gas Leak Detected:\n";

void setup() {
  Serial.begin(9600);
  sim800SS.begin(9600);
  
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  pinMode(POWER_CHECK_PIN, INPUT);
  
  gasValveServo.attach(10);
  gasValveServo.write(0);
  
  calibrateSensor();
}

void loop() {
  float ppm = getCalibratedPPM();
  float rateOfIncrease = calculateRateOfIncrease(ppm);
  float explosionRisk = predictExplosionRisk(ppm, rateOfIncrease);
  
  handleSafetySystems(ppm, rateOfIncrease, explosionRisk);
  monitorPowerSupply();
  checkSensorHealth(ppm);
  
  delay(1000);
}

float getCalibratedPPM() {
  static float baseline = 0;
  int raw = analogRead(GAS_SENSOR_PIN);
  
  // Apply temperature compensation (example formula)
  float temp = readTemperature(); // Implement temperature sensor reading
  float compensated = raw * (1 + (25 - temp) * 0.02);
  
  // Convert to PPM using sensor characteristics
  float rs_ro = (1023.0 - compensated) / compensated;
  return pow(10, (log10(rs_ro) - 0.6) / (-0.4)); // MQ-2 approximation for LPG
}

float predictExplosionRisk(float ppm, float rate) {
  // Use Random Forest model to predict time to dangerous levels
  return riskModel.predictWaktu(ppm, rate);
}

void handleSafetySystems(float ppm, float rate, float risk) {
  // Gas Type Classification
  String gasType = classifyGasType(ppm, rate);
  
  // Risk Assessment
  String riskAssessment = assessCompositeRisk(ppm, risk);
  
  // Ventilation Control
  controlVentilation(ppm, risk);
  
  // Emergency Actions
  if(risk > 0.8 || ppm > LEL_LPG * 0.4) {
    triggerEmergencyProtocol(gasType, ppm, risk);
  }
  
  // Data Logging
  logSystemStatus(ppm, gasType, riskAssessment);
}

String classifyGasType(float ppm, float rate) {
  // Uses pattern recognition based on response characteristics
  if(rate > 50 && ppm > 1000) return "LPG/Propane";
  if(rate > 20 && ppm < 1000) return "Smoke/CO";
  return "Unknown Combustible";
}

void controlVentilation(float ppm, float risk) {
  // Smart fan control with hysteresis
  static unsigned long lastVentilationCheck = 0;
  
  if(millis() - lastVentilationCheck > 60000) {
    bool needsVentilation = ppm > 1000 || risk > 0.5;
    
    if(needsVentilation && !fanActive) {
      digitalWrite(FAN_PIN, HIGH);
      fanActive = true;
      checkVentilationEfficiency(ppm);
    }
    else if(!needsVentilation && fanActive) {
      digitalWrite(FAN_PIN, LOW);
      fanActive = false;
    }
    
    lastVentilationCheck = millis();
  }
}

void checkVentilationEfficiency(float initialPPM) {
  unsigned long start = millis();
  while(millis() - start < 300000) { // 5-minute monitoring
    float currentPPM = getCalibratedPPM();
    if(currentPPM < initialPPM * 0.7) {
      logEvent("Ventilation Effective");
      return;
    }
    delay(60000);
  }
  logEvent("Ventilation Ineffective!");
  sendAlert("Ventilation System Failure");
}

void triggerEmergencyProtocol(String gasType, float ppm, float risk) {
  gasValveServo.write(90); // Close gas valve
  digitalWrite(RELAY_PIN, HIGH); // Cut power
  activateAlarmPattern();
  
  String message = "EMERGENCY! " + gasType + " Leak\n";
  message += "PPM: " + String(ppm) + "\n";
  message += "Explosion Risk: " + String(risk*100) + "%";
  
  sendAlert(message);
  escalateEmergencyIfNeeded();
}

void checkSensorHealth(float currentPPM) {
  static float calibrationValues[10];
  static byte index = 0;
  
  // Store calibration values
  calibrationValues[index] = currentPPM;
  index = (index + 1) % 10;
  
  // Check drift every 10 minutes
  if(millis() - lastSensorCheck > 600000) {
    float avg = 0;
    for(int i=0; i<10; i++) avg += calibrationValues[i];
    avg /= 10;
    
    if(abs(avg - calibrationValues[0]) > CALIBRATION_THRESHOLD) {
      sendAlert("Sensor Drift Detected! Needs Calibration");
    }
    
    lastSensorCheck = millis();
  }
}

void escalateEmergencyIfNeeded() {
  static unsigned long emergencyStart = 0;
  static byte escalationLevel = 0;
  
  if(emergencyStart == 0) emergencyStart = millis();
  
  if(millis() - emergencyStart > 300000) { // 5 minutes
    sendAlert("EMERGENCY ESCALATION: Contacting Fire Department");
    // Implement additional escalation procedures
    escalationLevel++;
    emergencyStart = millis();
  }
}

// Helper functions for peripheral operations
void calibrateSensor() {
  logEvent("Starting Sensor Calibration");
  // Implement proper calibration routine
  delay(2000); // Warm-up time
}

float readTemperature() {
  // Implement DS18B20 or DHT22 reading
  return 25.0; // Placeholder
}

void logSystemStatus(float ppm, String gasType, String risk) {
  Serial.print("PPM: ");
  Serial.print(ppm);
  Serial.print(" | Gas Type: ");
  Serial.print(gasType);
  Serial.print(" | Risk Level: ");
  Serial.println(risk);
}

void logEvent(String message) {
  Serial.print("[EVENT] ");
  Serial.println(message);
}

void sendAlert(String message) {
  sim800SS.println("AT+CMGF=1");
  delay(100);
  sim800SS.println("AT+CMGS=\"" + String(PHONE_1) + "\"");
  delay(100);
  sim800SS.print(message);
  sim800SS.write(26);
  delay(5000);
}

void activateAlarmPattern() {
  for(int i=0; i<3; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(1000);
    digitalWrite(BUZZER_PIN, LOW);
    delay(500);
  }
}

void monitorPowerSupply() {
  int powerReading = analogRead(POWER_CHECK_PIN);
  if(powerReading < 500) {
    sendAlert("WARNING: Power Supply Interrupted");
    // Implement battery backup switch
  }
}