import csv
import requests
from geopy.distance import geodesic
import time 
# https://www.my-ip.io/dedicated
def get_user_location():
    try:
        response = requests.get('https://api.my-ip.io/v2/ip.json')
        
        # Check if the response status code is 429 (Rate Limit Exceeded)
        if response.status_code == 429:
            print("Rate limit exceeded. Waiting for cooldown...")
            time.sleep(120)  # Wait for 60 seconds before retrying
            response = requests.get('https://api.my-ip.io/v2/ip.json')  # Retry the request

        if response.status_code == 200:
            location = response.json()
            print("API response:", location)  # Debugging: Print API response
            if 'location' in location and 'lat' in location['location'] and 'lon' in location['location']:
                latitude = float(location['location']['lat'])
                longitude = float(location['location']['lon'])
                return latitude, longitude
            else:
                print("Latitude or longitude not found in API response.")
                return None, None
        else:
            print("Error:", response.status_code)
            return None, None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None, None

latitude, longitude = get_user_location()
if latitude is not None and longitude is not None:
    print("Latitude:", latitude)
    print("Longitude:", longitude)
else:
    print("Error: Failed to retrieve user location.")

def read_pharmacies_from_csv(csv_file):
    pharmacies = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                pharmacy = {
                    'name': row['pharmacy_name'],
                    'address': row['address'],
                    'suburb': row['suburb'],
                    'postal_code': row['postal_code'],
                    'latitude': float(row['latitude']),
                    'longitude': float(row['longitude']),
                    'tel': row['tel'],
                    'link_url': row['link_url']
                }
            except ValueError:
                continue
            pharmacies.append(pharmacy)
    return pharmacies

def find_nearest_pharmacies(user_location, pharmacies, top_n=10):
    nearest_pharmacies = []
    distances = []
    for idx, pharmacy in pharmacies.iterrows():
        pharmacy_location = (pharmacy['latitude'], pharmacy['longitude'])
        if None not in pharmacy_location:
            distance = geodesic(user_location, pharmacy_location).kilometers
            distances.append((pharmacy, distance))
    # Sort distances by distance
    sorted_distances = sorted(distances, key=lambda x: x[1])
    # Get top N pharmacies
    for pharmacy, distance in sorted_distances[:top_n]:
        nearest_pharmacies.append((pharmacy, distance))
    return nearest_pharmacies


# def main():
#     # Get user location
#     user_location = get_user_location()
#     if user_location[0] is not None and user_location[1] is not None:
#         print("User location:", user_location)
#         # Read pharmacies from CSV
#         pharmacies = read_pharmacies_from_csv('yellow_pages_pharmacy_df.csv')
#         # Find nearest pharmacies
#         nearest_pharmacies = find_nearest_pharmacies(user_location, pharmacies, top_n=10)
#         if nearest_pharmacies:
#             print("Top 10 nearest pharmacies:")
#             for i, (pharmacy, distance) in enumerate(nearest_pharmacies, start=1):
#                 print(f"#{i}: {pharmacy['name']} - Distance: {distance:.2f} km")
#         else:
#             print("No pharmacies found.")
#     else:
#         print("Error: Failed to retrieve user location.")

# if __name__ == "__main__":
#     main()
