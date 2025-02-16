 
void setup() { 
  Serial.begin(9600); // Initialize serial communication 
} 
 
void loop() { 
  int gasLevel = analogRead(A0); // Read gas sensor value 
  Serial.println(gasLevel); // Send the data over serial 
  delay(1000); // Wait for a second 
} 
