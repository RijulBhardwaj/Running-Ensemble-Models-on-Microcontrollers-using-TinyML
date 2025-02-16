@echo off
REM Create project folder
mkdir GasLeakageDetection
cd GasLeakageDetection

REM Create the necessary files
echo. > arduino_code.ino
echo. > flask_server.py
echo. > send_gas_data.py
echo. > requirements.txt

REM Add content to arduino_code.ino
echo void setup() { >> arduino_code.ino
echo   Serial.begin(9600); // Initialize serial communication >> arduino_code.ino
echo } >> arduino_code.ino
echo. >> arduino_code.ino
echo void loop() { >> arduino_code.ino
echo   int gasLevel = analogRead(A0); // Read gas sensor value >> arduino_code.ino
echo   Serial.println(gasLevel); // Send the data over serial >> arduino_code.ino
echo   delay(1000); // Wait for a second >> arduino_code.ino
echo } >> arduino_code.ino

REM Add content to flask_server.py
echo from flask import Flask, request >> flask_server.py
echo app = Flask(__name__) >> flask_server.py
echo. >> flask_server.py
echo @app.route('/gas_data', methods=['POST']) >> flask_server.py
echo def receive_gas_data(): >> flask_server.py
echo     data = request.json >> flask_server.py
echo     print(f"Received gas data: {data['gas_level']}") >> flask_server.py
echo     return "Data received", 200 >> flask_server.py
echo. >> flask_server.py
echo if __name__ == '__main__': >> flask_server.py
echo     app.run(debug=True) >> flask_server.py

REM Add content to send_gas_data.py
echo import serial >> send_gas_data.py
echo import requests >> send_gas_data.py
echo import time >> send_gas_data.py
echo. >> send_gas_data.py
echo arduino = serial.Serial('/dev/ttyUSB0', 9600) >> send_gas_data.py
echo server_url = "http://localhost:5000/gas_data" >> send_gas_data.py
echo. >> send_gas_data.py
echo while True: >> send_gas_data.py
echo     gas_data = arduino.readline().decode('utf-8').strip() >> send_gas_data.py
echo     response = requests.post(server_url, json={"gas_level": gas_data}) >> send_gas_data.py
echo     print(f"Sent gas data: {gas_data}, Server Response: {response.text}") >> send_gas_data.py
echo     time.sleep(1) >> send_gas_data.py

REM Add content to requirements.txt
echo Flask==2.2.2 >> requirements.txt
echo requests==2.28.2 >> requirements.txt
echo pyserial==3.5 >> requirements.txt

echo Project setup complete!
