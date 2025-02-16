import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import serial
import random

# Function to simulate calibration for MQ2 sensor values
def calibrate_mq2(sensor_value):
    """
    Simulate calibration by converting sensor readings to PPM values.
    Adjust the formula based on known gas characteristics.
    """
    if sensor_value < 150:
        ppm = sensor_value * 0.1  # Low threshold for Methane
    elif sensor_value < 500:
        ppm = sensor_value * 0.2  # Simulating Butane range
    else:
        ppm = sensor_value * 0.3  # Simulating general air or other gases
    return ppm

# Create a synthetic dataset for MQ2 readings
sensor_readings = list(range(0, 1024))  # Full range of sensor values (0-1023)
ppm_values = [calibrate_mq2(x) for x in sensor_readings]

# Simulate corresponding parameters based on ranges
def classify_gas(sensor_value):
    if sensor_value < 150:
        return "Methane"
    elif sensor_value < 500:
        return "Butane"
    else:
        return "Air"

def classify_leak_severity(sensor_value):
    if sensor_value < 150:
        return "Low"
    elif sensor_value < 500:
        return "Moderate"
    else:
        return "High"

def classify_fire_risk(sensor_value):
    if sensor_value < 150:
        return "Low"
    elif sensor_value < 500:
        return "Medium"
    else:
        return "High"

def classify_flammability(sensor_value):
    if sensor_value < 150:
        return "Low"
    elif sensor_value < 500:
        return "Moderate"
    else:
        return "High"

# Generate dataset
data = {
    'sensor_reading': sensor_readings,
    'ppm': ppm_values,
    'leak_severity': [classify_leak_severity(x) for x in sensor_readings],
    'fire_risk': [classify_fire_risk(x) for x in sensor_readings],
    'flammability': [classify_flammability(x) for x in sensor_readings],
    'gas_type': [classify_gas(x) for x in sensor_readings]
}

df = pd.DataFrame(data)

# Features (independent variables) and Labels (dependent variables)
X = df[['sensor_reading', 'ppm']]  # Input features
labels = {
    'leak_severity': df['leak_severity'],
    'fire_risk': df['fire_risk'],
    'flammability': df['flammability'],
    'gas_type': df['gas_type']
}

trained_models = {}

# Train DecisionTree models for each parameter
for label, y in labels.items():
    print(f"Training model for {label}...")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Evaluate accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{label} Model Accuracy: {accuracy:.4f}")

    # Store trained model
    trained_models[label] = model

# Serial communication for real-time sensor reading
try:
    ser = serial.Serial('COM3', 9600)  # Adjust COM port as needed
    print("Successfully connected to the Arduino.")

    while True:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith('Gas Level'):
            sensor_value = int(line.split(':')[1].strip())  # Extract sensor reading
            ppm_value = calibrate_mq2(sensor_value)  # Convert to PPM
            print(f"Sensor Reading: {sensor_value}, PPM: {ppm_value}")

            # Prepare input data for prediction
            input_data = pd.DataFrame([[sensor_value, ppm_value]], columns=['sensor_reading', 'ppm'])

            # Predict parameters
            for label, model in trained_models.items():
                prediction = model.predict(input_data)
                print(f"{label} Prediction: {prediction[0]}")

except serial.SerialException as e:
    print(f"Error: {e}")
