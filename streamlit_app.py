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
    page_icon="🤗💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Oversea Student Healthcare Chatbot')
st.markdown('Welcome to the Oversea Student Healthcare Chatbot! Please select a tab from the sidebar to get started.')

# Sidebar navigation
st.sidebar.title('Navigation')
st.sidebar.markdown('Choose a tab to get started.')
st.sidebar.markdown('---')
st.sidebar.markdown('**Tabs:**')
st.sidebar.markdown('- Overview')
st.sidebar.markdown('- Disease Diagnosis')
st.sidebar.markdown('- Find Nearest Pharmacy')
st.sidebar.markdown('- Chatbot for Insurance Information')
st.sidebar.markdown('---')
st.sidebar.markdown('**About:**')
st.sidebar.markdown('This is a chatbot application that provides healthcare information to oversea students. It offers disease diagnosis, pharmacy location, and insurance information services.')

def fetch_my_location(latitude, longitude):
    api_key = 'pk.569b2648485cbbc6c23f0a1bc7fd78fb'  
    url = f'https://us1.locationiq.com/v1/reverse?key={api_key}&lat={latitude}&lon={longitude}&format=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['display_name']
    else:
        return None

NOMINATIM_API_URL = "https://nominatim.openstreetmap.org"
NOMINATIM_DETAILS_ENDPOINT = f"{NOMINATIM_API_URL}/details"
NOMINATIM_SEARCH_ENDPOINT = f"{NOMINATIM_API_URL}/search"
NOMINATIM_REVERSE_ENDPOINT = f"{NOMINATIM_API_URL}/reverse"

def fetch_osm_details(osm_id: str, osm_type: str, params: Dict[str, int]) -> dict:
    params_query = "&".join(f"{param_name}={param_value}" for param_name, param_value in params.items())
    request_url = f"{NOMINATIM_DETAILS_ENDPOINT}?osmtype={osm_type}&osmid={osm_id}&{params_query}&format=json"
    print(request_url)

    response = requests.get(request_url)
    response.raise_for_status()
    return response.json()


def fetch_osm_search(query: str, params: Dict[str, int]) -> dict:
    params_query = "&".join(f"{param_name}={param_value}" for param_name, param_value in params.items())
    request_url = f"{NOMINATIM_SEARCH_ENDPOINT}?q={query}&{params_query}&format=json"
    print(request_url)

    response = requests.get(request_url)
    response.raise_for_status()
    return response.json()


def fetch_osm_reverse(lat: float, lon: float, zoom: int, params: Dict[str, int]) -> dict:
    params_query = "&".join(f"{param_name}={param_value}" for param_name, param_value in params.items())
    request_url = f"{NOMINATIM_REVERSE_ENDPOINT}?lat={lat}&lon={lon}&zoom={zoom}&{params_query}&format=json"
    print(request_url)

    response = requests.get(request_url)
    response.raise_for_status()
    return response.json()

def location_api_tab():
    st.title('Find Nearest Pharmacy')
    st.markdown('This tab helps you find the nearest pharmacy to your current location. Please enter your current location to get started.')

    # Get user's current location

def main(command):
    if command == "details":
        result = fetch_osm_details(osm_id="175905", osm_type="R", params=query_params)
    elif command == "search":
        result = fetch_osm_search(query="New York", params=query_params)
    elif command == "reverse":
        result = fetch_osm_reverse(lat=40.7127281, lon=-74.0060152, zoom=10, params=query_params)
    else:
        raise Exception("Wrong command.")

    pprint(result)
    with open(f"{command}_result.json", "w") as output_file:
        output_file.write(json.dumps(result, ensure_ascii=False))
