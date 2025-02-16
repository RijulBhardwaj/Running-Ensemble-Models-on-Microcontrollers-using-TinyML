 
from flask import Flask, request 
app = Flask(__name__) 
 
@app.route('/gas_data', methods=['POST']) 
def receive_gas_data(): 
    data = request.json 
    print(f"Received gas data: {data['gas_level']}") 
    return "Data received", 200 
 
if __name__ == '__main__': 
    app.run(debug=True) 
