import network
from machine import Pin, ADC, Timer
import dht
import urequests
import ujson
import time

# Firebase Realtime Database URL and API Key
FIREBASE_URL = "https://test1209-99790-default-rtdb.asia-southeast1.firebasedatabase.app"
FIREBASE_API_KEY = "AIzaSyAEVknkMcwpL9MUOkEhFkGid_LjI-_J7cw"

# Initialize MQ-2 gas sensors (connected to ADC pin 35 and 34)
adc_gas1 = ADC(Pin(35))
adc_gas2 = ADC(Pin(34))
adc_gas1.atten(ADC.ATTN_11DB)  # Full range: 0 - 3.3V
adc_gas2.atten(ADC.ATTN_11DB)

# Initialize DHT sensor (connected to pin 23)
dht_sensor = dht.DHT11(Pin(23))

# WiFi connection
print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('sillyboy', '12345678s1')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

# RPM sensor variables (connected to pin 19)
tach_count = 0
rpm = 0

# Interrupt handler to count tachometer pulses
def tach_interrupt(pin):
    global tach_count
    tach_count += 1

# Attach interrupt to tachometer pin (Yellow Wire)
tach_pin = Pin(14, Pin.IN, Pin.PULL_UP)  # Connect Yellow Wire to pin 19
tach_pin.irq(trigger=Pin.IRQ_FALLING, handler=tach_interrupt)

# Timer to calculate RPM every second
def calculate_rpm(timer):
    global tach_count, rpm
    rpm = (tach_count / 4) * 60  # Assuming 2 pulses per revolution
    tach_count = 0
    #print("RPM:", rpm)

# Initialize the timer for RPM calculation
rpm_timer = Timer(0)
rpm_timer.init(period=1000, mode=Timer.PERIODIC, callback=calculate_rpm)

# Function to get current timestamp for Firebase
def get_current_timestamp():
    t = time.localtime()
    date = "{:02d}-{:02d}-{:04d}".format(t[2], t[1], t[0])  # Format: dd-mm-yyyy
    time_str = "{:02d}-{:02d}-{:02d}".format(t[3], t[4], t[5])  # Format: hh-mm-ss
    return date, time_str

# Function to publish data to Firebase
def publish_to_firebase(data):
    date, time_str = get_current_timestamp()
    firebase_path = f"{FIREBASE_URL}/{date}/{time_str}.json?auth={FIREBASE_API_KEY}"
    
    # Send the request to Firebase
    response = urequests.put(firebase_path, data=ujson.dumps(data))
    
    if response.status_code == 200:
        print(f"Data successfully sent to Firebase at {date} {time_str}")
    else:
        print(f"Failed to send data, status: {response.status_code}, message: {response.text}")
    
    response.close()

# Timer to collect and publish all data every 5 seconds
def publish_all_data(timer):
    try:
        # Read gas sensors
        gas_value1 = adc_gas1.read()
        gas_value2 = adc_gas2.read()
        gas_diff = gas_value1 - gas_value2
        
        # Read DHT sensor
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        
        # Prepare data for Firebase
        sensor_data = {
            "rpm": rpm,
            "temperature": temperature,
            "humidity": humidity,
            "gasdiff": gas_diff
        }
        
        # Publish data to Firebase
        publish_to_firebase(sensor_data)
        
        # Print all data
        print(f"Temperature: {temperature}C, Humidity: {humidity}%, Gas Difference: {gas_diff}, RPM: {rpm}")
    
    except OSError as e:
        print("Error reading sensors:", e)

# Initialize the timer for publishing data
publish_timer = Timer(-1)
publish_timer.init(period=5000, mode=Timer.PERIODIC, callback=publish_all_data)

# Main loop
while True:
    time.sleep(1)  # Main loop sleep to prevent excessive CPU usage