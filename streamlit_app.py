import streamlit as st
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement

# Initialize the chatbot
chatbot = ChatBot('Diagnose Chatbot')

# Train the chatbot (optional)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

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

    # Get user input
    user_input = st.text_input('You:', '')

    # Handle user input
    if st.button('Send'):
        # Get chatbot response
        bot_response = chatbot.get_response(user_input)
        
        # Save user input and bot response to chat history
        chat_history.append({'user': user_input, 'bot': str(bot_response)})

    # Display chat history
    for item in chat_history:
        st.write('User:', item['user'])
        st.write('Bot:', item['bot'])

def location_api_tab():
    st.title('Location API')
    # Add content for the location API tab

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