import streamlit as st
import random
from streamlit_extras.let_it_rain import rain
from streamlit_navigation_bar import st_navbar

# List of pages for navigation
pages = ["Home", "About Us", "Log out", "", "", ""]
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

st.set_page_config(initial_sidebar_state="collapsed", layout="wide", page_icon="🪴", page_title="Home Page")
page = st_navbar(pages, styles=styles, selected=None, logo_path="pages/ZenTech_Logo.svg")

# Redirect based on user type
if page == "Home":
    if st.session_state["utype"] == "farmer":
        st.switch_page("pages/f_dash.py")
    elif st.session_state["utype"] == "customer":
        st.switch_page("pages/c_dash.py")
    elif st.session_state["utype"] == "wholer":
        st.switch_page("pages/w_dash.py")

if page == "About Us":
    st.switch_page("pages/About_Us.py")

if page == "Log out":
    st.switch_page("Home_Page.py")

m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: green;
        color: white;
        width: 200px;
        text-align: center;
    }
    </style>""", unsafe_allow_html=True)

st.title("Soil Information")

# Randomized NPK and pH values for soil
N_value = random.randint(50, 200)  # in kg/ha
P_value = random.randint(20, 100)  # in kg/ha
K_value = random.randint(30, 150)  # in kg/ha
pH_value = round(random.uniform(5.5, 7.5), 2)  # pH scale (0-14)

# Display NPK values with units
st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)


a, b, c = st.columns(3)
with a:
    with st.container(border=True):
        st.metric(label="Nitrogen (N)", value=f"{N_value} kg/ha", delta=f"-{random.uniform(0.1, 5.0):.2f} kg/ha")
with b:
    with st.container(border=True):
        st.metric(label="Potassium (K)", value=f"{K_value} kg/ha", delta=f"-{random.uniform(0.1, 5.0):.2f} kg/ha")
with c:
    with st.container(border=True):
        st.metric(label="Phosphorus (P)", value=f"{P_value} kg/ha", delta=f"+{random.uniform(0.1, 5.0):.2f} kg/ha")

z, x, c = st.columns(3)
with z:
    with st.container(border=True):
        st.metric(label="Humidity", value=f"{random.uniform(30, 50):.1f}%", delta=f"+{random.uniform(0.1, 2.0):.2f}%")
with x:
    with st.container(border=True):
        st.metric(label="pH", value=f"{pH_value}", delta=f"+{random.uniform(0.1, 0.5):.2f}")

# # Rain effect for decoration
# rain(
#     emoji="🌿",
#     font_size=54,
#     falling_speed=10,
#     animation_length="infinite"
# )

# List of crops based on NPK and pH
crop_criteria = {
    "Rice": {"NPK": (120, 60, 60), "pH": (5.5, 6.5)},
    "Wheat": {"NPK": (120, 60, 40), "pH": (6.0, 7.0)},
    "Corn": {"NPK": (120, 60, 60), "pH": (5.8, 7.0)},
    "Soybeans": {"NPK": (40, 60, 40), "pH": (6.0, 7.0)},
    "Cotton": {"NPK": (80, 40, 40), "pH": (5.5, 7.0)},
    "Sugarcane": {"NPK": (120, 60, 60), "pH": (5.5, 7.5)},
    "Barley": {"NPK": (80, 40, 40), "pH": (6.0, 7.5)},
    "Potatoes": {"NPK": (5, 10, 30), "pH": (5.0, 6.5)},
    "Tomatoes": {"NPK": (5, 10, 10), "pH": (6.0, 6.8)},
    "Carrots": {"NPK": (5, 10, 10), "pH": (6.0, 6.8)},
    "Cabbage": {"NPK": (10, 20, 20), "pH": (6.0, 6.8)},
    "Peanuts": {"NPK": (10, 20, 10), "pH": (5.8, 7.0)},
    "Coffee": {"NPK": (10, 10, 10), "pH": (6.0, 6.5)},
    "Cocoa": {"NPK": (4, 7, 10), "pH": (6.0, 7.0)},
    "Bananas": {"NPK": (12, 12, 17), "pH": (5.5, 7.0)},
    "Apples": {"NPK": (10, 10, 10), "pH": (6.0, 7.0)},
    "Grapes": {"NPK": (10, 10, 10), "pH": (6.0, 6.5)},
    "Tobacco": {"NPK": (10, 20, 20), "pH": (5.8, 6.5)},
    "Sunflower": {"NPK": (50, 30, 30), "pH": (6.0, 7.5)},
}

# Function to calculate the absolute difference
def calculate_difference(soil_value, ideal_value):
    return abs(soil_value - ideal_value)

# Function to calculate pH difference
def calculate_pH_difference(soil_pH, pH_range):
    pH_min, pH_max = pH_range
    return min(abs(soil_pH - pH_min), abs(soil_pH - pH_max))

# Calculate the crop score based on NPK and pH differences
crop_scores = []

for crop, details in crop_criteria.items():
    N_diff = calculate_difference(N_value, details['NPK'][0])
    P_diff = calculate_difference(P_value, details['NPK'][1])
    K_diff = calculate_difference(K_value, details['NPK'][2])
    pH_diff = calculate_pH_difference(pH_value, details['pH'])
    
    # Total difference score: The lower the score, the better the match
    total_diff = N_diff + P_diff + K_diff + pH_diff
    crop_scores.append((crop, total_diff, N_diff, P_diff, K_diff, pH_diff))

# Sort crops based on the total difference score
sorted_crops = sorted(crop_scores, key=lambda x: x[1])

# Display the optimal crop and its NPK and pH values
st.header("Top 2 Optimal Crops for This Soil:")

# Display the top 2 crops with their ideal NPK and pH values
g,h = st.columns(2)
for i in range(2):
    best_crop = sorted_crops[i]
    crop_name = best_crop[0]
    crop_details = crop_criteria[crop_name]
    if i==0:
        with g:
            with st.container(border=True):
                st.subheader(f"{i+1}. {crop_name}")
                st.write(f"**Ideal NPK Values**: Nitrogen (N) = {crop_details['NPK'][0]} kg/ha, Phosphorus (P) = {crop_details['NPK'][1]} kg/ha, Potassium (K) = {crop_details['NPK'][2]} kg/ha")
                st.write(f"**Ideal pH Range**: {crop_details['pH'][0]} - {crop_details['pH'][1]}")
    else:
        with h:
            with st.container(border=True):
                st.subheader(f"{i+1}. {crop_name}")
                st.write(f"**Ideal NPK Values**: Nitrogen (N) = {crop_details['NPK'][0]} kg/ha, Phosphorus (P) = {crop_details['NPK'][1]} kg/ha, Potassium (K) = {crop_details['NPK'][2]} kg/ha")
                st.write(f"**Ideal pH Range**: {crop_details['pH'][0]} - {crop_details['pH'][1]}")

d, e = st.columns(2)

with d:
    with st.expander("Ideal N,P,K Values Info"):
        st.image("pages/npk_veg.png")
with e:
    with st.expander("Ideal pH Values Info"):
        st.image("pages/ph_veg.png")