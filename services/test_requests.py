import requests
import time

for i in range(6):
    params = {
        "id": i, 
        "flat_id": i+1, 
        "building_id": 6220, 
        "floor": 9 + (-1 ** (i)) * i, 
        "kitchen_area": 9.90 + (-1 ** (i)) * i, 
        "living_area": 19.900000 + (-1 ** (i)) * i * 2, 
        "rooms": 1, 
        "is_apartment": False, 
        "studio": False, 
        "total_area": 35.099998 + (-1 ** (i)) * i * 3, 
        "build_year": 1965 + (-1 ** (i)) * i * 8, 
        "building_type_int": 6, 
        "latitude": 55.717113, 
        "longitude": 37.781120, 
        "ceiling_height": 2.64, 
        "flats_count": 84, 
        "floors_total": 12, 
        "has_elevator": True
    }
    response = requests.post(f'http://localhost:4601/api/price/?flat_id={i+1}', json=params)
    print("Status Code", response.status_code)
    if response.status_code != 200:
        break
    if i == 3:
            time.sleep(30)

    time.sleep(15)