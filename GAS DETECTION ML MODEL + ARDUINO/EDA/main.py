import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Step 1: Load the dataset
def load_dataset(file_path):
    """
    Load the dataset, extract sensor readings and corresponding gas type.
    
    :param file_path: Path to the dataset (CSV file).
    :return: X (features) and y (target - gas type).
    """
    # Load the dataset
    df = pd.read_csv(file_path)

    # Apply a safe lambda function to extract gas type from the 'Gas' column
    df['Gas'] = df['Gas'].apply(lambda x: x.split('_')[1] if isinstance(x, str) and '_' in x else x)  # Handle missing '_'

    # Feature columns (sensor readings)
    X = df[['MQ2', 'MQ3', 'MQ5', 'MQ6', 'MQ7', 'MQ8', 'MQ135']].values

    # Target column (gas type)
    y = df['Gas'].values

    return X, y



# Step 2: Train a model to classify the gas type
def train_model(X, y):
    """
    Train a RandomForestClassifier on the sensor readings and gas types.

    :param X: Features (sensor readings)
    :param y: Target (gas types)
    :return: Trained model
    """
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize the RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Evaluate the model
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    return clf

# Step 3: Derive thresholds based on predictions
def derive_thresholds(clf, X, y):
    """
    Derive the thresholds for each gas type based on the classifier's predictions.
    
    :param clf: The trained classifier.
    :param X: Features (sensor readings).
    :param y: True labels (gas types).
    :return: Dictionary containing thresholds for each gas type.
    """
    # Convert y to a Pandas Series to use the unique() method
    unique_gases = pd.Series(y).unique()

    thresholds = {}

    # Calculate the threshold for each unique gas type
    for gas in unique_gases:
        # Get the predicted probabilities for the current gas type
        probs = clf.predict_proba(X)[:, 1]  # Assuming binary classification
        thresholds[gas] = np.percentile(probs, 95)  # Set threshold at 95th percentile

    return thresholds


# Main function
def main():
    # Set file path to your dataset
    file_path = "C:/Coding Projects/GAS DETECTION ML MODEL + ARDUINO/dataset/Gas_Sensors_Measurements.csv"



    # Step 1: Load and preprocess the data
    X, y = load_dataset(file_path)

    # Step 2: Train the model and classify gas types
    clf = train_model(X, y)

    # Step 3: Derive thresholds for each gas type
    thresholds = derive_thresholds(clf, X, y)

if __name__ == "__main__":
    main()
