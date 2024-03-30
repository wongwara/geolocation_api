import streamlit as st
from geopy.geocoders import Nominatim
import requests
import folium
import pandas as pd
from geopy.distance import geodesic
import location_api

yellow_pages = pd.read_csv('yellow_pages_pharmacy_df.csv') 
nsw_pharmacy = pd.read_csv('nsw_pharmacy_df.csv') 

# Initialize chat history
chat_history = []

# page setup
st.set_page_config(
    page_title="Oversea Student Healthcare Chatbot",
    page_icon="🤗💬"
)

st.title('Oversea Student Healthcare Chatbot')
st.markdown('Welcome to the Oversea Student Healthcare Chatbot!')

def main():
    st.title("Nearest Pharmacies Finder")
    
    # Get user location
    user_location = location_api.get_user_location()
    if user_location[0] is not None and user_location[1] is not None:
        st.write("User location:", user_location)
        
        # Find nearest pharmacies
        nearest_pharmacies = location_api.find_nearest_pharmacies(user_location, yellow_pages, top_n=10)
        
        if nearest_pharmacies:
            st.subheader("Top 10 Nearest Pharmacies:")
            for i, (pharmacy, distance) in enumerate(nearest_pharmacies, start=1):
                st.write(f"#{i}: {pharmacy['pharmacy_name']} - Distance: {distance:.2f} km")
            
            # Create a Folium map
            map_center = user_location[::-1]  # Reverse latitude and longitude for Folium
            m = folium.Map(location=map_center, zoom_start=10)
            
            # Add markers for nearest pharmacies
            for pharmacy, _ in nearest_pharmacies:
                folium.Marker(location=[pharmacy['latitude'], pharmacy['longitude']],
                              popup=pharmacy['pharmacy_name']).add_to(m)
            
            # Display the map
            folium_static(m)
        else:
            st.error("No pharmacies found.")
    else:
        st.error("Failed to retrieve user location.")

if __name__ == "__main__":
    main()

# def fetch_user_location(latitude, longitude):
#     api_key = 'pk.569b2648485cbbc6c23f0a1bc7fd78fb'
#     url = f'https://us1.locationiq.com/v1/reverse?key={api_key}&lat={latitude}&lon={longitude}&format=json'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get('lat'), data.get('lon')
#     else:
#         st.error('Error fetching user location')

# # Add a button to trigger location retrieval
# if st.button('Get My Location'):
#     latitude, longitude = fetch_user_location()

# # Display latitude obtained from JavaScript
# latitude = st.session_state.latitude
# if latitude:
#     st.write(f'Latitude: {latitude}')

# # Function to calculate distance between two coordinates
# def calculate_distance(user_location, pharmacy_location):
#     return geodesic(user_location, pharmacy_location).kilometers

# # Function to find nearest pharmacy
# def find_nearest_pharmacy(user_location, pharmacy_df):
#     pharmacy_df['Distance (km)'] = pharmacy_df.apply(lambda row: calculate_distance(user_location, (row['latitude'], row['longitude'])), axis=1)
#     nearest_pharmacy = pharmacy_df.loc[pharmacy_df['Distance (km)'].idxmin()]
#     return nearest_pharmacy

# # Add functionality to find nearest pharmacy
# if 'Find Nearest Pharmacy' in st.session_state:
#     st.subheader('Find Nearest Pharmacy')
    
#     user_latitude, user_longitude = fetch_user_location()
#     st.write(f'User Location: Latitude {user_latitude}, Longitude {user_longitude}')
    
#     nearest_pharmacy = find_nearest_pharmacy((user_latitude, user_longitude), yellow_pages)
    
#     st.write('Nearest Pharmacy Information:')
#     st.write(nearest_pharmacy)
    
# def main():
#     # Create a Folium map centered around the user's location
#     m = folium.Map(location=[user_latitude, user_longitude], zoom_start=12)

#     # Add marker for user's location
#     folium.Marker(location=[user_latitude, user_longitude], popup='User Location', icon=folium.Icon(color='blue')).add_to(m)

#     # Add marker for nearest pharmacy
#     folium.Marker(location=[nearest_pharmacy['latitude'], nearest_pharmacy['longitude']], popup=nearest_pharmacy['Pharmacy name'], icon=folium.Icon(color='green')).add_to(m)

#     # Render the map
#     folium_static(m)

# if __name__ == "__main__":
#     main()

