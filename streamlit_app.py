import streamlit as st
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
# from chatterbot.conversation import Statement
from geopy.geocoders import Nominatim
import requests
import folium
import json
from typing import Dict
import pandas as pd
from geopy.distance import geodesic

# # Initialize the chatbot
# chatbot = ChatBot('Diagnose Chatbot')

# # Train the chatbot (optional)
# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train('chatterbot.corpus.english')

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

# Sidebar navigation
st.sidebar.title('Navigation')
st.sidebar.markdown('---')
st.sidebar.markdown('- Overview')
st.sidebar.markdown('- Disease Diagnosis')
st.sidebar.markdown('- Find Nearest Pharmacy')
st.sidebar.markdown('- Chatbot for Insurance Information')
st.sidebar.markdown('---')
st.sidebar.markdown('**About:**')
st.sidebar.markdown('This is a chatbot application that provides healthcare information to oversea students. It offers disease diagnosis, pharmacy location, and insurance information services.')
# pk.569b2648485cbbc6c23f0a1bc7fd78fb

def fetch_user_location(latitude, longitude):
    api_key = 'pk.569b2648485cbbc6c23f0a1bc7fd78fb'
    url = f'https://us1.locationiq.com/v1/reverse?key={api_key}&lat={latitude}&lon={longitude}&format=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('lat'), data.get('lon')
    else:
        st.error('Error fetching user location')

# Function to calculate distance between two coordinates
def calculate_distance(user_location, pharmacy_location):
    return geodesic(user_location, pharmacy_location).kilometers

# Function to find nearest pharmacy
def find_nearest_pharmacy(user_location, pharmacy_df):
    pharmacy_df['Distance (km)'] = pharmacy_df.apply(lambda row: calculate_distance(user_location, (row['latitude'], row['longitude'])), axis=1)
    nearest_pharmacy = pharmacy_df.loc[pharmacy_df['Distance (km)'].idxmin()]
    return nearest_pharmacy

# Add functionality to find nearest pharmacy
if 'Find Nearest Pharmacy' in st.session_state:
    st.subheader('Find Nearest Pharmacy')
    
    user_latitude, user_longitude = fetch_user_location()
    st.write(f'User Location: Latitude {user_latitude}, Longitude {user_longitude}')
    
    nearest_pharmacy = find_nearest_pharmacy((user_latitude, user_longitude), df)
    
    st.write('Nearest Pharmacy Information:')
    st.write(nearest_pharmacy)
    
def main():
    # Create a Folium map centered around the user's location
    m = folium.Map(location=[user_latitude, user_longitude], zoom_start=12)

    # Add marker for user's location
    folium.Marker(location=[user_latitude, user_longitude], popup='User Location', icon=folium.Icon(color='blue')).add_to(m)

    # Add marker for nearest pharmacy
    folium.Marker(location=[nearest_pharmacy['latitude'], nearest_pharmacy['longitude']], popup=nearest_pharmacy['Pharmacy name'], icon=folium.Icon(color='green')).add_to(m)

    # Render the map
    folium_static(m)

if __name__ == "__main__":
    main()

