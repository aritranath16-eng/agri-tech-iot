import time
import random
from supabase import create_client

# 1. Connect to your Database
SUPABASE_URL = "https://qtnmomvlratulfbwklyj.supabase.co"
SUPABASE_KEY = "sb_publishable_jubeneginJg1j6r0ZnHNYQ_O0B4MuCA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Starting values for our fake sensors
temp = 24.0
humidity = 60.0
co2 = 450.0

print("Starting to send data to Supabase... Press Ctrl+C to stop.")

while True:
    # 3. Alter the numbers slightly to simulate real weather changing
    temp += random.uniform(-0.5, 0.5)
    humidity += random.uniform(-1.5, 1.5)
    co2 += random.uniform(-10.0, 10.0)

    # 4. Package the data
    data_payload = {
        "temperature": round(temp, 2),
        "humidity": round(humidity, 2),
        "co2": round(co2, 2)
    }

    # 5. Send to Supabase
    try:
        supabase.table('sensor_data').insert(data_payload).execute()
        print(f"Sent: {data_payload}")
    except Exception as e:
        print(f"Error sending data: {e}")

    # 6. Wait 3 seconds before sending the next reading
    time.sleep(3)