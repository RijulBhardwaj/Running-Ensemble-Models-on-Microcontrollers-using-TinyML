# Running-Ensemble-Models-on-Microcontrollers-using-TinyML
Based on this technique we showcase one usecase in the endless possibilities of this method : Developed a gas sensor detection system using an Ensemble Random Forest model on an Arduino R3 microcontroller, demonstrating the feasibility of running heavy ensemble models on resource-constrained devices with TinyML optimization.
Gas Leakage Detector Using GSM & Arduino with SMS Alert
This repository contains the complete design, implementation, and documentation for a Gas Leakage Detection System that leverages an Arduino UNO microcontroller, a SIM800 GSM module, and an MQ2 gas sensor. The system is engineered to continuously monitor harmful gas levels in residential, commercial, or industrial settings and automatically alert users via SMS when dangerous thresholds are exceeded. A 16x2 LCD display provides real-time visual feedback of gas concentrations.

Table of Contents
Introduction
Project Motivation
System Overview
Key Components
Working Mechanism
Flowchart & Block Diagram
Literature Review Summary
Implementation Details
Flexibility & Scalability
Practical Applications and Benefits
Setup and Usage
Future Enhancements
License
Introduction
Gas leaks present significant safety hazards due to their potential to cause explosions, fires, and toxic inhalation. Traditional detection methods—such as manual inspections and basic alarms—are not always reliable, especially during off-hours or in remote locations. This project introduces an automated system that not only detects gas leaks in real time but also provides immediate SMS alerts to ensure rapid response.

Project Motivation
Safety Concerns: Gas leaks from LPG, methane, and other volatile compounds can lead to catastrophic incidents.
Need for Automation: Manual monitoring is insufficient; an automated, continuously running system can prevent severe accidents.
Remote Notification: Integration of GSM ensures that even when users are not present on-site, they receive timely alerts.
System Overview
The gas leakage detector is built around an Arduino UNO microcontroller that processes input from the MQ2 gas sensor. When the sensor detects gas concentrations above a predefined threshold, the system triggers an SMS alert via the SIM800 GSM module. Concurrently, a 16x2 LCD display provides a real-time visual representation of the gas concentration levels.

Key Components
Arduino UNO:

Acts as the central processing unit.
Reads the analog signal from the MQ2 sensor.
Compares gas concentration levels to predefined safety thresholds.
Communicates with the GSM module to trigger alerts.
MQ2 Gas Sensor:

Sensitive to LPG, methane, ammonia, alcohol, benzene, and smoke.
Provides both analog and digital outputs based on gas concentration.
Ideal for continuous monitoring due to its fast response time.
SIM800 GSM Module:

Enables the system to send SMS alerts to a predefined mobile number.
Operates on quad-band GSM/GPRS.
Uses AT commands for communication with the Arduino.
Powered by an external 9V/12V DC supply to ensure reliable connectivity.
16x2 LCD Display:

Displays real-time gas concentration data.
Shows warning messages when dangerous gas levels are detected.
Working Mechanism
Continuous Monitoring:

The MQ2 sensor continuously senses gas levels and sends data to the Arduino.
The Arduino processes the sensor’s analog signal, converting it into a meaningful gas concentration value.
Threshold Comparison:

The system compares the measured gas concentration with safety thresholds.
If the concentration exceeds the threshold, the Arduino triggers the alert process.
Alert Activation:

The Arduino sends a command to the SIM800 GSM module to dispatch an SMS alert to a designated mobile number.
Simultaneously, the LCD displays a warning message, such as "Gas Leakage Detected."
Real-Time Display:

The LCD continuously updates with current gas concentration values for on-site monitoring.
Flowchart & Block Diagram
Block Diagram Overview:
MQ2 Sensor: Detects gas concentration → Arduino UNO: Processes data →
SIM800 GSM Module: Sends SMS alert.
16x2 LCD Display: Shows real-time gas levels.
Power Supply: Provides necessary voltages to all components.
Flowchart Highlights:
Start: System powers up.
Monitor Gas Levels: Continuous reading from the MQ2 sensor.
Threshold Check: Is the gas concentration above the safe limit?
Yes: Trigger SMS alert and display warning.
No: Continue monitoring.
End: Process repeats continuously for real-time detection.
Literature Review Summary
This project builds upon previous research and advancements in gas leakage detection systems. Studies in areas such as IoT-based monitoring, low-power sensor networks, and integrated safety systems have influenced the design:

Smart Gas Detection for Home Safety: Integration of gas sensors with GSM alerts.
Industrial IoT Solutions: Cost-effective, low-power monitoring systems.
Laser-Based and Advanced Detection Methods: Enhanced accuracy and response times.
These studies underscore the importance of rapid, automated detection systems that can operate effectively in various environments.

Implementation Details
Hardware Setup:
Wiring diagrams and schematics are included in the /hardware directory.
Power management details to ensure stable operation of the Arduino, GSM module, and sensor.
Software:
Arduino IDE is used for programming.
The code reads sensor data, processes it, and uses AT commands to control the SIM800 module.
Debouncing and calibration routines are implemented for reliable sensor readings.
Testing & Calibration:
Detailed steps for calibrating the MQ2 sensor to set appropriate thresholds.
Testing procedures to validate SMS alert functionality and LCD display accuracy.
Flexibility & Scalability
The system is designed with modularity in mind:

Sensor Integration: Can be extended to support additional sensors (e.g., MQ5 for different gas types).
IoT Expansion: Future enhancements could include integration with IoT platforms for remote data logging and cloud-based monitoring.
Alarm System: Potential to add audible alarms or automated shut-off mechanisms for enhanced safety.
Practical Applications and Benefits
Cost-Effective & Compact: Suitable for both household and small-scale industrial environments.
Real-Time Alerts: Ensures immediate notification via SMS, reducing the risk of severe accidents.
Customizable: Can be adapted to various settings and integrated with other sensors or IoT systems.
Remote Monitoring: Particularly useful in locations where continuous on-site supervision is not feasible.
Setup and Usage
Hardware Assembly:
Follow the wiring diagram in the /hardware folder.
Ensure proper connection of the MQ2 sensor, SIM800 GSM module, and LCD display to the Arduino UNO.
Software Installation:
Open the provided Arduino sketch in the Arduino IDE.
Install any necessary libraries (e.g., LiquidCrystal for the LCD, GSM libraries for SIM800).
Configuration:
Set the threshold levels for gas concentration based on calibration.
Configure the predefined mobile number for SMS alerts.
Deployment:
Upload the sketch to the Arduino.
Power the system and monitor the LCD for real-time gas readings.
Test the SMS functionality by simulating a gas leak condition.
Future Enhancements
IoT Connectivity: Integrate Wi-Fi or NB-IoT modules for remote monitoring and data analytics.
Enhanced UI: Develop a mobile or web application to view historical gas concentration data.
Automated Control: Incorporate automated shut-off valves to prevent gas flow in case of leak detection.
Multi-Sensor Fusion: Expand the system to include additional sensors for comprehensive environmental monitoring.
License
This project is licensed under the MIT License.

