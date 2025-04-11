import requests
import json
import time
from requests.auth import HTTPDigestAuth

# Printer API settings
api_url = "http://192.168.151.27/api/v1/status"  # Replace with your printer's actual IP
api_key = "2D7329TS679fcbfa"

headers = {
    # "X-Api-Key": api_key,
    "Authorization": 'Digest username="maker", realm="Printer API", nonce="dca577670000207b", url="/api/v1/status", response="9f805487daaa4e50f83988b6159e995'
}

# List of files to print
Print_Files = {
    "Cone_0.4n_0.2mm_PLA_MK4IS_11m.bgcode",
    "cube_0.4n_0.2mm_PLA_MK4IS_16m.bgcode",
    "Cylinder_0.4n_0.2mm_PLA_MK4IS_22m.bgcode",
    "HOLLOW_RECTANGLE_0.4n_0.2mm_PLA_MK4IS_1h47m.bgcode",
    "Pyramid_0.4n_0.2mm_PLA_MK4IS_12m.bgcode",
    "Rectangle_0.4n_0.2mm_PLA_MK4IS_21m.bgcode",
    "Rectangular_Prisim_0.4n_0.2mm_PLA_MK4IS_22m.bgcode",
    "sphere_r-24mm_0.4n_0.2mm_PLA_MK4IS_53m.bgcode"
}

# Function to get the printer data
def get_printer_data():
    try:
        response = requests.get(api_url, auth=HTTPDigestAuth('maker', 'swNuc3Wv6YHL5ho'))
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Function to log data into a JSON file
def log_data(data, filename="printer_data_log.json"):
    try:
        with open(filename, 'a') as file:
            json.dump(data, file)
            file.write("\n")
        print(f"Data logged successfully.")
    except IOError as e:
        print(f"Error writing to file: {e}")

# Function to send a print job:
def start_print(file_name):
    """Uploads and starts a print on PrusaLink"""
    url = "http://192.168.151.27/api/v1/print"
    data = {"file": file_name}

    response = requests.post(url, json=data, auth=HTTPDigestAuth('maker', 'swNuc3Wv6YHL5ho'))

    if response.status_code == 200:
        print(f"Started print: {file_name}")
        return True
    else:
        print(f"Failed to start print: {file_name}, Error: {response.text}")
        return False

# Function to check printer status and wait for job completion
def check_print_status():
    """Waits for current print to finish before starting the next one"""
    while True:
        data = get_printer_data()
        if data:
            printer_state = data["printer"]["state"]

            if printer_state == "FINISHED":
                print("Print completed!")
                return True     # Proceed to next print

        time.sleep(30)  # Check every 30 seconds

# Function to collect data while the printer is printing, then stop automatically
def collect_data(interval=5):
    print("Starting data collection...")

    while True:
        data = get_printer_data()  # Fetch data from printer API

        if data:
            printer_state = data["printer"]["state"]  # Get the printer state
            
            if printer_state == "PRINTING":
                data['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
                log_data(data)
            
            elif printer_state in ["PAUSED", "FINISHED"]:  
                data['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
                log_data(data)  # Prints the FINISHED statement instead of just exiting
                print(f"Print completed. Printer state: {printer_state}. Stopping data collection.")
                break  # Exit the loop when the print is finished

        time.sleep(interval)

# Main loop: Queue prints + Collect data
for i, gcode in enumerate(Print_Files):
    print(f"Starting job {i + 1}/{len(Print_Files)}: {gcode}")

    if start_print(gcode):
        collect_data(interval=5)    # Start data collection -- collect every 5 seconds
        check_print_status()    # Wait for print to finish
        print(f"Print {i + 1}/{len(Print_Files)} completed.")

print("All prints completed. Data collection done.")