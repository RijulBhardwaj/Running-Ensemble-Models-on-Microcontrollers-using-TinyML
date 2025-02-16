 
import serial 
import requests 
import time 
 
arduino = serial.Serial('/dev/ttyUSB0', 9600) 
server_url = "http://localhost:5000/gas_data" 
 
while True: 
    gas_data = arduino.readline().decode('utf-8').strip() 
    response = requests.post(server_url, json={"gas_level": gas_data}) 
    print(f"Sent gas data: {gas_data}, Server Response: {response.text}") 
    time.sleep(1) 
