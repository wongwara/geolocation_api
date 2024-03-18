import streamlit as st
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
# from chatterbot.conversation import Statement
from geopy.geocoders import Nominatim
import requests
import folium

# # Initialize the chatbot
# chatbot = ChatBot('Diagnose Chatbot')

# # Train the chatbot (optional)
# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train('chatterbot.corpus.english')

# Initialize chat history
chat_history = []

# page setup
st.set_page_config(
    page_title="Oversea Student Healthcare Chatbot",
    page_icon="🤗💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

def overview_tab():
    st.title('Overview')
    # Add content for the overview tab

def disease_diagnosis_tab():
    st.title('Chatbot for Disease Diagnosis')

    # # Get user input
    # user_input = st.text_input('You:', '')

    # # Handle user input
    # if st.button('Send'):
    #     # Get chatbot response
    #     bot_response = chatbot.get_response(user_input)
        
    #     # Save user input and bot response to chat history
    #     chat_history.append({'user': user_input, 'bot': str(bot_response)})

    # # Display chat history
    # for item in chat_history:
    #     st.write('User:', item['user'])
    #     st.write('Bot:', item['bot'])


# Initialize the Geolocation API
geolocator = Nominatim(user_agent="location-healthcare-chatbot", timeout=10)

def get_coordinates_from_postal_code(postal_code):
    try:
        location = geolocator.geocode(postal_code)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        st.error('Error fetching location:', e)

def get_nearby_pharmacies(latitude, longitude, api_key):
    try:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&type=pharmacy&key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error('Error fetching nearby pharmacies:', response.text)
    except Exception as e:
        st.error('Error fetching nearby pharmacies:', e)

def location_api_tab():
    st.title('Find Nearest Pharmacy')

    # Input field to enter postal code
    postal_code = st.text_input('Enter Postal Code:', '')

    if st.button('Find'):
        # Get coordinates from postal code
        latitude, longitude = get_coordinates_from_postal_code(postal_code)

        if latitude and longitude:
            # Fetch nearby pharmacies
            api_key = "AIzaSyDSuDpjE75aNTRREqqMhlDxwmFHRAz0vcY"
            nearby_pharmacies = get_nearby_pharmacies(latitude, longitude, api_key)

            if nearby_pharmacies:
                # Display map with user location and nearby pharmacies
                m = folium.Map(location=[latitude, longitude], zoom_start=13)
                folium.Marker([latitude, longitude], popup='Your Location').add_to(m)
                
                for result in nearby_pharmacies['results']:
                    pharmacy_name = result['name']
                    pharmacy_location = result['geometry']['location']
                    folium.Marker([pharmacy_location['lat'], pharmacy_location['lng']], popup=pharmacy_name).add_to(m)

                folium_static(m)
            else:
                st.error('No nearby pharmacies found.')
        else:
            st.error('Invalid postal code.')


def insurance_info_tab():
    st.title('Chatbot for Insurance Information')
    # Add content for the insurance information tab


def main():
    st.sidebar.title('Navigation')
    app_mode = st.sidebar.selectbox('Choose a tab', ['Overview', 'Disease Diagnosis', 'Location API', 'Insurance Information'])

    if app_mode == 'Overview':
        overview_tab()
    elif app_mode == 'Disease Diagnosis':
        disease_diagnosis_tab()
    elif app_mode == 'Location API':
        location_api_tab()
    elif app_mode == 'Insurance Information':
        insurance_info_tab()

if __name__ == "__main__":
    main()


# Save chat history after each interaction
# save_chat_history(st.session_state.messages)

# https://discuss.streamlit.io/t/web-geolocation-api-to-get-users-location/9493/2