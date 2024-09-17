import requests
import pandas as pd
import time
import os
import joblib
from datetime import datetime

FIREBASE_URL = "https://test1209-99790-default-rtdb.asia-southeast1.firebasedatabase.app"
CSV_FILENAME = 'DataFetch.csv'
MODEL_FILE = "secret.pkl"

# Label mapping
label_mapping = {
    0: 'normal',
    1: 'error with rpm',
    2: 'error with temperature',
    3: 'error with humidity',
    4: 'error with gasdiff'
}

# Fetch data from Firebase for a specific date
def fetch_data_from_firebase(date):
    try:
        response = requests.get(f"{FIREBASE_URL}/{date}.json")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Predict status using the model
def predict_status(model, scaler, data):
    features = ['rpm', 'temperature', 'humidity', 'gasdiff']
    X = pd.DataFrame(data, index=[0])[features]
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)
    return label_mapping.get(prediction[0], 'unknown')

# Convert new data to DataFrame, predict status, and append it to CSV
def append_new_data_to_csv(data, filename, last_timestamp, model, scaler):
    records = []
    
    for time_key, values in data.items():
        timestamp_str = f"{today_date} {time_key}"
        timestamp = pd.to_datetime(timestamp_str, format="%d-%m-%Y %H-%M-%S")
        
        if last_timestamp is None or timestamp > last_timestamp:
            row = {
                'timestamp': timestamp,
                'rpm': values.get('rpm', 0),
                'temperature': values.get('temperature', 0),
                'humidity': values.get('humidity', 0),
                'gasdiff': values.get('gasdiff', 0),
                'status': predict_status(model, scaler, values)
            }
            records.append(row)
    
    if records:
        df = pd.DataFrame(records)
        df.to_csv(filename, mode='a', header=not os.path.exists(filename), index=False)
        
        # Return the maximum timestamp from the newly added records
        return max(records, key=lambda x: x['timestamp'])['timestamp']
    
    return last_timestamp

def main():
    global today_date
    today_date = datetime.now().strftime("%d-%m-%Y")  # Get today's date in the required format
    
    # Load the model and scaler
    try:
        model_data = joblib.load(MODEL_FILE)
        scaler = model_data['scaler']
        model = model_data['model']
        print("Model and scaler loaded successfully.")
    except Exception as e:
        print(f"Error loading model and scaler: {e}")
        return
    
    last_timestamp = None
    
    if os.path.exists(CSV_FILENAME):
        # Load the last timestamp from the existing CSV file
        try:
            df = pd.read_csv(CSV_FILENAME)
            last_timestamp = pd.to_datetime(df['timestamp']).max()
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            # Handle empty or corrupted CSV
            last_timestamp = None

    while True:
        data = fetch_data_from_firebase(today_date)
        
        if data:
            last_timestamp = append_new_data_to_csv(data, CSV_FILENAME, last_timestamp, model, scaler)
            print(f"Appended new data up to {last_timestamp}")
        
        time.sleep(10)

if __name__ == "__main__":
    main()
