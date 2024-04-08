import streamlit as st
from geopy.geocoders import Nominatim
import requests
import folium 
import pandas as pd
from streamlit_folium import folium_static
from geopy.distance import geodesic
import location_api
from folium.plugins import MarkerCluster
import time 

yellow_pages = pd.read_csv('yellow_pages_pharmacy_df.csv') 
nsw_pharmacy = pd.read_csv('nsw_pharmacy_df.csv') 

# Initialize chat history
chat_history = []

# # page setup
# st.set_page_config(
#     page_title="Oversea Student Healthcare Find Nearest Pharmacies",
#     page_icon="🤗💬"
# )

# st.title('Oversea Student Healthcare Find Nearest Pharmacies')
# st.markdown('Welcome to New South Wales Nearest Pharmacies finding!')
# st.markdown('We will need you to provide your current latitude and longitude.')
# st.markdown('Once you provide the latitude and longitude, we will find the nearest pharmacies for you.')
# st.markdown('You can find your current location from [here](https://www.gps-coordinates.net/my-location)')


# def get_user_location():
#     default_latitude = -33.8837
#     default_longitude = 151.2006
    
#     latitude = st.number_input("Enter latitude:", format="%.6f", min_value=-90.0, max_value=90.0, value=default_latitude)
#     longitude = st.number_input("Enter longitude:", format="%.6f", value=default_longitude)
    
#     return latitude, longitude

# def get_current_location():
#     try:
#         response = requests.get('https://api.my-ip.io/v2/ip.json')
#         # Check if the response status code is 429 (Rate Limit Exceeded)
#         if response.status_code == 429:
#             print("Rate limit exceeded. Waiting for cooldown...")
#             time.sleep(120)  # Wait for 60 seconds before retrying
#             response = requests.get('https://api.my-ip.io/v2/ip.json')  # Retry the request

#         if response.status_code == 200:
#             location = response.json()
#             print("API response:", location)  # Debugging: Print API response
#             if 'location' in location and 'lat' in location['location'] and 'lon' in location['location']:
#                 latitude = float(location['location']['lat'])
#                 longitude = float(location['location']['lon'])
#                 return latitude, longitude
#             else:
#                 print("Latitude or longitude not found in API response.")
#                 return None, None
#         else:
#             print("Error:", response.status_code)
#             return None, None
#     except requests.exceptions.RequestException as e:
#         print("Error:", e)
#         return None, None


# def main():
#     st.title("User Location and Nearest Pharmacies Finder")
#     st.write("Please provide your location and find the nearest pharmacies.")

#     # Get user location
#     user_location = get_user_location()
#     if user_location[0] is not None and user_location[1] is not None:
#         st.write("User location:", user_location)
#         st.write("You can try the following locations:")
#         st.write("Try Sydnet Westfield location: lat -33.870098 and long 151.208817.")
#         st.write("Try Sydney Opera House location: lat -33.85681 and long 151.21514.")
#         st.write("Try Sydney Airport location: lat -33.9461 and long 151.17722.")
#         st.write("Try Sydney Olympic Park location: lat -33.848461 and long 151.063713.")
#         st.write("Try Penrith library location: lat -33.7505 and long 150.6899.")
#         # Find nearest pharmacies
#         nearest_pharmacies = location_api.find_nearest_pharmacies(user_location, yellow_pages, top_n=10)

#         if nearest_pharmacies:
#             st.subheader("Top 10 Nearest Pharmacies:")
#             for i, (pharmacy, distance) in enumerate(nearest_pharmacies, start=1):
#                 st.write(f"#{i}: {pharmacy['pharmacy_name']} - Distance: {distance:.2f} km")

#             # Create a Folium map
#             map_center = user_location
#             m = folium.Map(location=map_center, zoom_start=15)

#             # Create a MarkerCluster
#             marker_cluster = MarkerCluster().add_to(m)

#             # Add markers for user location and nearest pharmacies
#             folium.Marker(location=map_center, popup="Your Location", icon=folium.Icon(color="green")).add_to(m)
#             for pharmacy, distance in nearest_pharmacies:
#                 popup_text = f"{pharmacy['pharmacy_name']}<br>Distance: {distance:.2f} km"
#                 folium.Marker(location=(pharmacy['latitude'], pharmacy['longitude']), popup=popup_text).add_to(marker_cluster)

#             # Change the color of the nearest pharmacy marker to red
#             nearest_pharmacy_location = (nearest_pharmacies[0][0]['latitude'], nearest_pharmacies[0][0]['longitude'])
#             folium.Marker(location=nearest_pharmacy_location, popup="Nearest Pharmacy", icon=folium.Icon(color="red")).add_to(m)

#             # Display the map
#             folium_static(m)
#         else:
#             st.error("No pharmacies found.")
#     else:
#         st.error("Failed to retrieve user location.")

# if __name__ == "__main__":
#     main()

# page setup
st.set_page_config(
    page_title="Oversea Student Healthcare Find Nearest Pharmacies",
    page_icon="🤗💬"
)

st.title('Oversea Student Healthcare Find Nearest Pharmacies')
st.markdown('Welcome to New South Wales Nearest Pharmacies finding!, We will need you to provide your current latitude and longitude.')
st.markdown('Once you provide the latitude and longitude, we will find the nearest pharmacies for you. You can find your current location from [here](https://www.gps-coordinates.net/my-location)')


def get_user_location_from_chat():
    st.text("Bot: Hello")
    st.text("Bot: Please provide your current latitude and longitude ")
    st.text('in the following format: latitude, longitude'" ")
    user_input = st.text_input("You:", value="-33.8837,151.2006")
    if st.button("Submit"):
        chat_history.append(("You", user_input))
        return user_input

def chat():
    user_input = get_user_location_from_chat()
    if user_input:
        try:
            latitude, longitude = map(float, user_input.split(','))
            user_location = (latitude, longitude)
            nearest_pharmacies = location_api.find_nearest_pharmacies(user_location, yellow_pages, top_n=10)
            if nearest_pharmacies:
                # Create a Folium map
                map_center = user_location
                m = folium.Map(location=map_center, zoom_start=15)

                # Create a MarkerCluster
                marker_cluster = MarkerCluster().add_to(m)

                # Add markers for user location and nearest pharmacies
                folium.Marker(location=map_center, popup="Your Location", icon=folium.Icon(color="green")).add_to(m)
                for pharmacy, distance in nearest_pharmacies:
                    popup_text = f"{pharmacy['pharmacy_name']}<br>Distance: {distance:.2f} km"
                    folium.Marker(location=(pharmacy['latitude'], pharmacy['longitude']), popup=popup_text).add_to(marker_cluster)

                # Change the color of the nearest pharmacy marker to red
                nearest_pharmacy_location = (nearest_pharmacies[0][0]['latitude'], nearest_pharmacies[0][0]['longitude'])
                folium.Marker(location=nearest_pharmacy_location, popup="Nearest Pharmacy", icon=folium.Icon(color="red")).add_to(m)

                # Display the map
                folium_static(m)
                st.subheader("Top 10 Nearest Pharmacies:")
                for i, (pharmacy, distance) in enumerate(nearest_pharmacies, start=1):
                    st.write(f"#{i}: {pharmacy['pharmacy_name']} - Distance: {distance:.2f} km")

            else:
                st.error("No pharmacies found.")
        except ValueError:
            st.error("Invalid input format. Please provide latitude and longitude in the format 'latitude, longitude'.")

if __name__ == "__main__":
    chat()
    st.subheader('You can try the following locations:')
    st.write("Try Sydnet Westfield location: lat -33.870098 and long 151.208817.")
    st.write("Try Sydney Opera House location: lat -33.85681 and long 151.21514.")
    st.write("Try Sydney Airport location: lat -33.9461 and long 151.17722.")
    st.write("Try Sydney Olympic Park location: lat -33.848461 and long 151.063713.")
    st.write("Try Penrith library location: lat -33.7505 and long 150.6899.")

