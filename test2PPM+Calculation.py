import math
import matplotlib.pyplot as plt

# Constants for MQ2 gas sensor
V_in = 12.0  # Supply voltage in Volts (assumed to be 5V)
RL = 10.0  # Load resistance in kOhms
R0 = 0.4388  # R0 value (calculated from fresh air) in kOhms

# Function to calculate RS (sensor resistance) from the analog value
def calculate_RS(analog_value):
    """
    Convert the analog reading to sensor resistance (RS).

    :param analog_value: Analog reading from MQ2 sensor (0-1023)
    :return: RS (sensor resistance) in kOhms
    """
    V_out = (analog_value / 1023.0) * V_in  # Convert analog value to voltage
    
    if V_out == 0:
        return float('inf')  # Handle division by zero by setting RS to infinity
    
    RS = (V_in - V_out) / V_out  # Calculate RS using the formula RS = (Vin - Vout) / Vout
    return RS

def calculate_PPM(RS, m, b):
    """
    Calculate the gas concentration in PPM based on sensor resistance (RS) and the gas-specific constants.

    :param RS: Sensor resistance (RS) in kOhms
    :param m: Slope (for the specific gas)
    :param b: Y-intercept (for the specific gas)
    :return: Gas concentration in PPM
    """
    # Calculate the resistance ratio RS/R0
    RS_R0 = RS / R0

    # Ensure RS_R0 is positive to avoid math domain error
    if RS_R0 <= 0:
        print(f"Invalid RS/R0 value: {RS_R0}. Skipping PPM calculation.")
        return float('inf')  # Return infinity or a placeholder for invalid cases

    # Calculate log(x) using the log-log scale equation
    log_x = (math.log10(RS_R0) - b) / m
    # Inverse log to get x (PPM)
    PPM = 10 ** log_x
    return PPM


# Function to automatically detect gas type based on sensor resistance
def detect_gas_type(RS):
    """
    Detect the gas type based on the sensor resistance (RS).

    :param RS: Sensor resistance (RS) in kOhms
    :return: Gas type detected
    """
    if RS < 1.0:
        return "LPG"
    elif 1.0 <= RS < 5.0:
        return "CO"
    elif 5.0 <= RS < 10.0:
        return "Methane"
    elif 10.0 <= RS < 20.0:
        return "Smoke"
    elif 20.0 <= RS < 30.0:
        return "Butane"
    elif RS >= 30.0:
        return "Alcohol"
    else:
        return "Unknown"

# Function to test the gas concentration and visualize results
def test_gas_with_visualization(analog_value):
    """
    Test the gas concentration for a given analog reading, detect gas type, and visualize data.

    :param analog_value: Analog reading from the sensor (0-1023)
    """
    # Calculate sensor resistance from the analog value
    RS = calculate_RS(analog_value)

    # Detect the gas type
    gas_type = detect_gas_type(RS)

    # Constants for each gas type
    gas_constants = {
        'LPG': {'m': -0.473, 'b': 1.413},
        'Methane': {'m': -0.510, 'b': 1.402},
        'Smoke': {'m': -0.500, 'b': 1.300},
        'CO': {'m': -0.430, 'b': 1.500},
        'Butane': {'m': -0.490, 'b': 1.450},
        'Alcohol': {'m': -0.490, 'b': 1.550},
    }

    # Check if the detected gas type has corresponding constants
    if gas_type not in gas_constants:
        print("Air or Unknown Gas Detected")
        return None, gas_type

    # Get the constants for the selected gas type
    gas_m = gas_constants[gas_type]['m']
    gas_b = gas_constants[gas_type]['b']

    # Calculate PPM for the detected gas type
    PPM = calculate_PPM(RS, gas_m, gas_b)

    print(f"Sensor Resistance (RS): {RS:.4f} kOhms")
    print(f"Gas Type Detected: {gas_type}")
    print(f"Gas Concentration ({gas_type}) in PPM: {PPM:.2f} PPM")

    # Visualization
    analog_values = range(0, 1024)  # Possible analog readings
    # Update RS values for visualization to cap very high values
    RS_values = [min(calculate_RS(a), 1e6) for a in analog_values]
# Exclude invalid PPM values for the plot
    PPM_values = [calculate_PPM(rs, gas_m, gas_b) if rs > 0 else 0 for rs in RS_values]

# Cap PPM values to a reasonable maximum for display
    PPM_values = [min(ppm, 1e6) for ppm in PPM_values]
    

    plt.figure(figsize=(10, 6))
    
    # Plot RS vs Analog Reading
    plt.subplot(2, 1, 1)
    plt.plot(analog_values, RS_values, label="RS (kOhms)", color="blue")
    plt.axvline(x=analog_value, color="red", linestyle="--", label="Input Reading")
    plt.xlabel("Analog Reading")
    plt.ylabel("RS (kOhms)")
    plt.title("Sensor Resistance (RS) vs Analog Reading")
    plt.legend()
    plt.grid(True)

    # Plot PPM vs Analog Reading
    plt.subplot(2, 1, 2)
    plt.plot(analog_values, PPM_values, label=f"{gas_type} Concentration (PPM)", color="green")
    plt.axvline(x=analog_value, color="red", linestyle="--", label="Input Reading")
    plt.xlabel("Analog Reading")
    plt.ylabel("PPM (Parts Per Million)")
    plt.title(f"Gas Concentration ({gas_type}) vs Analog Reading")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Input: Custom analog reading from the sensor
analog_reading = int(input("Enter the analog reading (0-1023): "))

# Test the gas type, concentration, and visualize
test_gas_with_visualization(analog_reading)
