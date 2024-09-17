import requests
import pandas as pd

# Firebase Realtime Database URL
FIREBASE_URL = "https://test1209-99790-default-rtdb.asia-southeast1.firebasedatabase.app"

# Fetch data from Firebase for a specific date
def fetch_data_from_firebase(date):
    try:
        response = requests.get(f"{FIREBASE_URL}/{date}.json")
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Convert data to DataFrame and save it to CSV
def convert_data_to_csv(data, filename):
    records = []
    
    for time_key, values in data.items():
        timestamp_str = f"17-09-2024 {time_key}"
        timestamp = pd.to_datetime(timestamp_str, format="%d-%m-%Y %H-%M-%S")
        
        row = {
            'timestamp': timestamp,
            'rpm': values.get('rpm', 0),
            'temperature': values.get('temperature', 0),
            'humidity': values.get('humidity', 0),
            'gasdiff': values.get('gas_difference', 0)
        }
        records.append(row)
    
    df = pd.DataFrame(records)
    df.to_csv(filename, index=False)

def main():
    # Fetch the data from Firebase for the specific date
    date = "17-09-2024"
    data = fetch_data_from_firebase(date)
    
    if data:
        # Convert the data to CSV
        convert_data_to_csv(data, 'rpm_data.csv')
        print("Data has been successfully written to rpm_data.csv")

if __name__ == "__main__":
    main()