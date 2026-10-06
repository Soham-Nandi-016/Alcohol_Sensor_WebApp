import serial
import time
import json
import re
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# --- CONFIGURATION ---
SERIAL_PORT = os.environ.get('SERIAL_PORT', 'COM7')
BAUD_RATE = 9600
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
# ---------------------

def setup_supabase() -> Client:
    """Initializes the Supabase client."""
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error initializing Supabase: {e}")
        return None

def main():
    print(f"Starting Python Bridge on {SERIAL_PORT}...")
    
    supabase = setup_supabase()
    if not supabase:
        return

    try:
        # Initialize Serial Connection
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset
        print("Connected to Arduino.")
    except Exception as e:
        print(f"Failed to connect to Serial Port {SERIAL_PORT}: {e}")
        return

    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                
                if line:
                    try:
                        # Extract numeric value from strings like "Alcohol Level: 228"
                        match = re.search(r'\d+', line)
                        if match:
                            level = int(match.group())
                            print(f"Received Level: {level}")

                            # Push to Supabase
                            data = {
                                "level": level
                            }
                            
                            response = supabase.table("alcohol_logs").insert(data).execute()
                            print(f"Logged to Supabase: {response.data}")
                        else:
                            print(f"No numerical data found in: {line}")

                    except Exception as e:
                        print(f"Error processing line: {e}")

        except KeyboardInterrupt:
            print("\nBridge stopped by user.")
            break
        except Exception as e:
            print(f"Critical Error: {e}")
            time.sleep(1)

    ser.close()

if __name__ == "__main__":
    main()
