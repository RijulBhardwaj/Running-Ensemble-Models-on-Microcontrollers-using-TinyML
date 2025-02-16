import serial
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def calibrate_mq2(sensor_value):
    ppm = sensor_value / 100  # Placeholder formula, ned to modify based on new values rudra will say
    return ppm


sensor_readings = [916, 935, 939, 938, 921, 925, 940, 945, 945, 947, 947, 943, 947, 946, 947, 950, 956, 956, 955, 954]


ppm_values = [calibrate_mq2(x) for x in sensor_readings]

# temp dataset
data = {
    'sensor_reading': sensor_readings,
    'ppm': ppm_values,
    'leak_severity': ['Low', 'Low', 'Low', 'Low', 'Moderate', 'Moderate', 'High', 'High', 'High', 'High', 'Low', 'Low', 'Moderate', 'High', 'High', 'High', 'High', 'Moderate', 'Moderate', 'High'],
    'fire_risk': ['Low', 'Low', 'Low', 'Low', 'Medium', 'Medium', 'High', 'High', 'High', 'High', 'Low', 'Low', 'Medium', 'High', 'High', 'High', 'High', 'Medium', 'Medium', 'High'],
    'flammability': ['Low', 'Low', 'Low', 'Low', 'Moderate', 'Moderate', 'High', 'High', 'High', 'High', 'Low', 'Low', 'Moderate', 'High', 'High', 'High', 'High', 'Moderate', 'Moderate', 'High'],
    'gas_type': ['Methane', 'Methane', 'Methane', 'Methane', 'Butane', 'Butane', 'Butane', 'Methane', 'Methane', 'Butane', 'Methane', 'Methane', 'Methane', 'Butane', 'Butane', 'Methane', 'Butane', 'Butane', 'Methane', 'Methane']
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


for label, y in labels.items():
    print(f"Training model for {label}...")
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    
    y_pred = model.predict(X_test)

    
    accuracy = accuracy_score(y_test, y_pred)
    print(f'{label} Model Accuracy: {accuracy:.4f}')

    trained_models[label] = model

#serial communication port
try:
    ser = serial.Serial('COM3', 9600)  
    print("Successfully connected to the Arduino.")
    
   
    while True:
        
        line = ser.readline().decode('utf-8').strip()
        if line.startswith('Gas Level'):
            sensor_value = int(line.split(':')[1].strip())  # Extracting the sensor reading
            ppm_value = calibrate_mq2(sensor_value)  # Convert to PPM
            print(f"Sensor Reading: {sensor_value}, PPM: {ppm_value}")
            
            
            input_data = pd.DataFrame([[sensor_value, ppm_value]], columns=['sensor_reading', 'ppm'])

            # Predicing all parameters
            for label, model in trained_models.items():
                prediction = model.predict(input_data)
                print(f"{label} Prediction: {prediction[0]}")
        
except serial.SerialException as e:
    print(f"Error: {e}")

