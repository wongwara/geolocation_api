import streamlit as st

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
    # Add content for the disease diagnosis tab

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