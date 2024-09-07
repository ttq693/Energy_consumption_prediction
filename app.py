from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)

# Load the model and the scaler
model = load_model('"C:\Users\tazin\OneDrive\Desktop\flask\model.h5"')
scaler = StandardScaler()  # Normally, you would load a pre-fit scaler

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract data from form
        substation = request.form.get('substation', type=int)
        feeder = request.form.get('feeder', type=int)
        temperature = request.form.get('temperature', type=float)
        humidity = request.form.get('humidity', type=float)
        wind_speed = request.form.get('wind_speed', type=float)
        pressure = request.form.get('pressure', type=float)

        # Create DataFrame for prediction
        input_data = pd.DataFrame({
            'substation': [substation],
            'feeder': [feeder],
            'temperature': [temperature],
            'humidity': [humidity],
            'wind_speed': [wind_speed],
            'pressure': [pressure]
        })
        # Scale data
        scaled_data = scaler.transform(input_data)  # Use your pre-fit scaler here

        # Predict
        prediction = model.predict(scaled_data)[0][0]

        return render_template('index.html', prediction=f'Predicted Energy Consumption: {prediction}')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
