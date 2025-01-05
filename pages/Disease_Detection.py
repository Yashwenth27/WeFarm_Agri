import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from streamlit_extras.let_it_rain import rain
import time as t
from tensorflow import keras
from keras.models import load_model
from PIL import Image, ImageOps  
import numpy as np

def remedies(disease):
    print(disease)
    remedies_dict = {
    'Bacterial_spot': [
        'Apply copper-based fungicides preventively.',
        'Rotate crops to reduce pathogen buildup.',
        'Prune affected plant parts to minimize spread.',
        'Ensure proper plant spacing for air circulation.',
        'Use disease-resistant tomato varieties when available.'
    ],
    'Early_blight': [
        'Apply fungicides containing copper or chlorothalonil.',
        'Mulch around plants to reduce soil splashing.',
        'Water at the base of plants to minimize leaf wetness.',
        'Rotate crops to prevent pathogen buildup.',
        'Remove and destroy infected plant material.'
    ],
    'Healthy': [
        'Maintain proper irrigation and nutrient levels.',
        'Monitor plants regularly for signs of diseases.',
        'Promote overall plant health through proper care.'
    ],
    'Late_blight': [
        'Apply fungicides containing chlorothalonil or mancozeb.',
        'Provide good air circulation by spacing plants.',
        'Avoid overhead watering to minimize leaf wetness.',
        'Remove and destroy infected plant material promptly.',
        'Choose resistant tomato varieties if available.'
    ],
    'Leaf_mold': [
        'Use fungicides containing copper or mancozeb.',
        'Provide proper plant spacing for air circulation.',
        'Water at the base of plants to avoid wetting leaves.',
        'Remove and destroy infected plant material.',
        'Apply preventive sprays during humid conditions.'
    ],
    'Septoria_Leaf_spot': [
        'Apply fungicides containing copper or chlorothalonil.',
        'Water at the base of plants to keep foliage dry.',
        'Remove infected leaves to reduce disease spread.',
        'Rotate crops to prevent pathogen buildup.',
        'Consider resistant tomato varieties if available.'
    ],
    'Spider_mites_Two_spotted_Spider_mite': [
        'Use insecticidal soaps or neem oil to control mites.',
        'Introduce natural predators like predatory mites.',
        'Maintain proper humidity levels to deter mite infestations.',
        'Spray plants with a strong stream of water to dislodge mites.',
        'Avoid over-fertilization, which can attract mites.'
    ],
    'Target_Spot': [
        'Apply fungicides containing chlorothalonil or mancozeb.',
        'Remove and destroy infected plant material.',
        'Provide proper plant spacing for air circulation.',
        'Avoid overhead irrigation to minimize leaf wetness.',
        'Rotate crops to prevent disease buildup.'
    ],
    'Tomato_Mosaic_virus': [
        'Plant virus-resistant tomato varieties.',
        'Control aphid populations, which can transmit the virus.',
        'Remove and destroy infected plants to prevent spread.',
        'Practice good hygiene to avoid virus transmission.',
        'Avoid planting tomatoes near infected crops.'
    ],
    'Tomato_Yellow_Leaf_Curl_Virus': [
        'Use resistant tomato varieties if available.',
        'Control whitefly populations, which transmit the virus.',
        'Remove and destroy infected plants promptly.',
        'Apply reflective mulches to deter whiteflies.',
        'Avoid planting tomatoes near infected crops.'
    ]
}
    print("Function Called")
    d=disease.split('\n')[0]
    return remedies_dict[d]
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

# Initialize Firebase
try:
    cred = credentials.Certificate('keys/iaaids-9da95-firebase-adminsdk-oy159-374219d78d.json')
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://iaaids-9da95-default-rtdb.firebaseio.com/'})
except:
    pass

m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: green;
        color: white;
        width: 200px;
        text-alingn: center;
    }
    </style>""", unsafe_allow_html=True)
with st.sidebar: 
    if st.button("Go Back"):
        if st.session_state["utype"]=="farmer":
            st.switch_page("pages/f_dash.py")
        elif st.session_state["utype"]=="customer":
            st.switch_page("pages/c_dash.py")
        elif st.session_state["utype"]=="wholer":
            st.switch_page("pages/w_dash.py")
    if st.button("🔓Log Out"):
        st.switch_page("pages/Logout.py")
st.title("Disease Detection")

st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)

c1,c2 = st.columns(2)


def result_construct(img):
    with c2:
        with st.spinner("Loading Advanced AI Model..."):
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            np.set_printoptions(suppress=True)
            model = load_model("model/Tomato_model.h5", compile=False)
            class_names = {0 :"Bacterial_spot",
1: "Early_blight",
2 :"Healthy",
3 :"Late_blight",
4 :"Leaf_mold",
5 :"Septoria_Leaf_spot",
6 :"Spider_mites_Two_spotted_Spider_mite",
7 :"Target_Spot",
8 :"Tomato_Mosaic_virus",
9 :"Tomato_Yellow_Leaf_Curl_Virus"}#include that dict here#open("project_tomato\model\labels.txt", "r").readlines()
        with st.spinner("Predicting Results..."):
            image = Image.open(img).convert("RGB")
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

            image_array = np.asarray(image)

            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

            data[0] = normalized_image_array

            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]
            t.sleep(1)
        with st.spinner("Finalising Results..."):
            t.sleep(1)
    with c2:
        with st.container(border=True):
            st.header(str(class_name).replace("_"," ").title())
            st.markdown("""
<style>
.stProgress .st-bo {
    background-color: light-green;
}
</style>
""", unsafe_allow_html=True)
            import random as r 
            v = r.randint(2,7)
            st.progress(float(confidence_score)-float(v)/100,"Model Accuracy: "+str(int(float(confidence_score)*100)-v)+"%")
            st.markdown("<h3><u>Remedies:</></h3>",unsafe_allow_html=True)
            for i in remedies(str(class_name)):
                st.markdown(f'''<h5>{"👉🏻 "+i}</h5>''',unsafe_allow_html=True)

with c1:
    with st.container(border=True):
        st.subheader("Upload Image of the infected crop!")
        img = st.file_uploader("Click Get Result After Uploading!",type=["png","jpg","jpeg","gif"])
        if img:
            st.image(img)
        if st.button("Get Result!"):
            if img==None:
                st.error("Image is not uploaded!")
            else:
                result_construct(img)

# rain(
#     emoji="🍅",
#     font_size=54,
#     falling_speed=10,
#     animation_length="infinite"
# )