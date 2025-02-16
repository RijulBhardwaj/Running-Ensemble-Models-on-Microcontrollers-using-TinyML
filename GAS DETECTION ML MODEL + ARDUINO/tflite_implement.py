import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# Your existing sensor readings data
sensor_readings = [916, 935, 939, 938, 921, 925, 940, 945, 945, 947, 947, 943, 947, 946, 947, 950, 956, 956, 955, 954]
ppm_values = [x / 100 for x in sensor_readings]  # Placeholder formula for ppm calculation

# Example labels for different attributes (change as needed)
labels_data = {
    'leak_severity': ['Low', 'Low', 'Low', 'Low', 'Moderate', 'Moderate', 'High', 'High', 'High', 'High', 'Low', 'Low', 'Moderate', 'High', 'High', 'High', 'High', 'Moderate', 'Moderate', 'High'],
    'fire_risk': ['Low', 'Low', 'Low', 'Low', 'Medium', 'Medium', 'High', 'High', 'High', 'High', 'Low', 'Low', 'Medium', 'High', 'High', 'High', 'High', 'Medium', 'Medium', 'High'],
    'flammability': ['Low', 'Low', 'Low', 'Low', 'Moderate', 'Moderate', 'High', 'High', 'High', 'High', 'Low', 'Low', 'Moderate', 'High', 'High', 'High', 'High', 'Moderate', 'Moderate', 'High'],
    'gas_type': ['Methane', 'Methane', 'Methane', 'Methane', 'Butane', 'Butane', 'Butane', 'Methane', 'Methane', 'Butane', 'Methane', 'Methane', 'Methane', 'Butane', 'Butane', 'Methane', 'Butane', 'Butane', 'Methane', 'Methane']
}

# Creating the DataFrame
df = pd.DataFrame({
    'sensor_reading': sensor_readings,
    'ppm': ppm_values,
    'leak_severity': labels_data['leak_severity'],
    'fire_risk': labels_data['fire_risk'],
    'flammability': labels_data['flammability'],
    'gas_type': labels_data['gas_type']
})

# Features (input)
X = df[['sensor_reading', 'ppm']]

# Labels (output)
labels = {
    'leak_severity': df['leak_severity'],
    'fire_risk': df['fire_risk'],
    'flammability': df['flammability'],
    'gas_type': df['gas_type']
}

# Initialize a dictionary to store the trained models
trained_models = {}

# Loop to train a model for each label
for label, y in labels.items():
    print(f"Training model for {label}...")
    
    # Encode categorical labels into numeric values for training
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2)
    
    # Build a simple neural network model
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(X.shape[1],)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(len(label_encoder.classes_), activation='softmax')  # Output layer with as many nodes as the number of classes
    ])
    
    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    # Train the model
    model.fit(X_train, y_train, epochs=10, batch_size=4, verbose=1)
    
    # Evaluate the model
    _, accuracy = model.evaluate(X_test, y_test)
    print(f'{label} Model Accuracy: {accuracy:.4f}')
    
    # Store the trained model
    trained_models[label] = model
    
    # Save the trained model as an .h5 file
    model.save(f"{label}_model.h5")
    print(f"Saved {label} model to disk.")

    # Convert the model to TensorFlow Lite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    # Save the TensorFlow Lite model
    tflite_model_path = f"{label}_model.tflite"
    with open(tflite_model_path, 'wb') as f:
        f.write(tflite_model)
    print(f"Converted {label} model to TensorFlow Lite and saved as {tflite_model_path}")

# Done with training and conversion!
print("Training and conversion to TFLite completed for all models.")
