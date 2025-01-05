import streamlit as st

from streamlit_extras.let_it_rain import rain
from streamlit_navigation_bar import st_navbar
pages = ["Home", "About Us","Log out","","",""]


    
styles = {
    "nav": {
        "background-color": "green",
        "justify-content": "left",
    },
    "img": {
        "padding-right": "14px",
    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "background-color": "white",
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "14px",
    }
}
st.set_page_config(initial_sidebar_state="collapsed",layout="wide",page_icon="🪴",page_title="Home Page")
page = st_navbar(pages, styles=styles, selected=None,logo_path="pages/ZenTech_Logo.svg")
if page=="Home":
    if st.session_state["utype"]=="farmer":
        st.switch_page("pages/f_dash.py")
    elif st.session_state["utype"]=="customer":
        st.switch_page("pages/c_dash.py")
    elif st.session_state["utype"]=="wholer":
        st.switch_page("pages/w_dash.py")
if page=="About Us":
    st.switch_page("pages/About_Us.py")
if page=="Log out":
    st.switch_page("Home_Page.py")
m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: green;
        color: white;
        width: 200px;
        text-alingn: center;
    }
    </style>""", unsafe_allow_html=True)
# with c2: 
#     if st.button("Go Back"):
#         
#     if st.button("🔓Log Out"):
#         st.switch_page("pages/Logout.py")


# import requests
# import json
# import streamlit as st


# st.title("Weather Application")


# state = st.text_input("Enter State:")
# city = st.text_input("Enter City:")


# if st.button("Get Weather"):
#     if city and state:
#         api_key = "f2250789eda0c682291e62d94cb4d241"
#         url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state}&appid={api_key}&units=metric"
        
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             st.success("Weather data fetched successfully!")
#             data = response.json()
            
#             # Display Weather Details using st.metric
#             st.write(f"**Weather:** {data['weather'][0]['description'].title()}")
#             st.metric(label="Temperature", value=f"{data['main']['temp']} °C", delta=f"Feels like {data['main']['feels_like']} °C")
#             st.metric(label="Humidity", value=f"{data['main']['humidity']}%")
#             st.metric(label="Pressure", value=f"{data['main']['pressure']} hPa")
#             st.metric(label="Wind Speed", value=f"{data['wind']['speed']} m/s")
#             st.metric(label="Latitude", value=f"{data['coord']['lat']}°")
#             st.metric(label="Longitude", value=f"{data['coord']['lon']}°")
#         else:
#             st.error("Error occurred while fetching data. Please check the city and state names.")
#     else:
#         st.warning("Please enter both State and City.")


import requests
import json
import streamlit as st
import geocoder


st.title("🌍 🌤️ Weather Forecast : Today")
st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)

import time
with st.spinner("📍 **Fetching your location...**"):
    g = geocoder.ip('me')
    if g.city and g.state:
        city = g.city
        state = g.state
        st.subheader(f"📍 **{city}, {state}**")
    else:
        st.warning("⚠️ Could not detect location. Please check your internet connection.")
        city = st.text_input("Enter City:")
        state = st.text_input("Enter State:")
    time.sleep(2)

if city and state:
    api_key = "f2250789eda0c682291e62d94cb4d241"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        success_message = st.empty()  # This creates an empty placeholder for the message

        # Display the success message
        success_message.success("✅ Weather data fetched successfully!")

        # Wait for 2 seconds, then clear the message
        time.sleep(2)
        success_message.empty()
        #st.success("✅ Weather data fetched successfully!")
        data = response.json()
        print(data)
        
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.metric(label="🌤️ Weather", value=data['weather'][0]['description'].title())
            with st.container(border=True):
                st.metric(label="🌡️ Temperature", value=f"{data['main']['temp']} °C", delta=f"Feels like {data['main']['feels_like']} °C")
            with st.container(border=True):
                st.metric(label="💧 Humidity", value=f"{data['main']['humidity']}%")
        
        with col2:
            with st.container(border=True):
                st.metric(label="🌬️ Wind Speed", value=f"{data['wind']['speed']} m/s")
            with st.container(border=True):
                st.metric(label="📊 Pressure", value=f"{data['main']['pressure']} hPa")
            with st.container(border=True):
                a,b = st.columns(2)
            
                with a:
                    st.metric(label="🧭 Latitude", value=f"{data['coord']['lat']}°")
                with b:
                    st.metric(label="🧭 Longitude", value=f"{data['coord']['lon']}°")
        
    else:
        st.error("Error occurred while fetching data. Please check the city and state names.")
else:
    st.warning("Please ensure valid location details are provided.")


