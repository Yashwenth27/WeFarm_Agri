import streamlit as st

# <button style="
#                 width: 80%; 
#                 padding: 10px; 
#                 margin-top: 10px; 
#                 background-color: green; 
#                 color: white;
#                 border-radius: 10px;
#                 font-size: 16px;" onclick="switch_page('{page_name}')">{label}</button>

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
page = st_navbar(pages, styles=styles, selected="Home",logo_path="pages/ZenTech_Logo.svg")

if page=="About Us":
    st.switch_page("pages/About_Us.py")
if page=="Log out":
    st.switch_page("Home_Page.py")
if st.session_state["logged_in"] and st.session_state["user_id"]:
    username = st.session_state['user_id']
    st.title(f"Welcome, {username}")
    st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)

    image_urls = [
        "https://s3.envato.com/files/251358231/2018_07_12_1522_01.jpg",
        "https://gardenerspath.com/wp-content/uploads/2020/09/Common-Tomato-Diseases-Cover.jpg",
        "https://c8.alamy.com/comp/2JRMJW8/farmer-shaking-hands-with-a-businessman-on-a-vineyard-with-grape-nursery-stock-2JRMJW8.jpg"
    ]

    labels = ["Crop Request", "Affected Crop", "Seller Details"]

    # Function to create a card-like button
    def create_card(image_url, label, page_name):
        st.markdown(
            f"""
            <div style="text-align: left; margin-bottom: 10px;">
                <img src="{image_url}" alt="{label}" style="width: 230px; height:230px; border-radius: 10px;">
                
            </div>
            """,
            unsafe_allow_html=True
        )
        m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: green;
            color: white;
            width: 230px;
            margin-bottom: 20px;
            text-alingn: center;
                        
        }
        </style>""", unsafe_allow_html=True)
        if st.button(label,key=image_url):
            st.switch_page(page_name)

    # Function to switch page
    def switch_page(page_name):
        st.switch_page(page_name)

    # Create a 3x3 grid
    rows = 2
    cols = 4
    for i in range(rows):
        columns = st.columns(cols)
        for j in range(cols):
            with columns[j]:
                if i * cols + j < len(image_urls):
                    page_name = f"pages/{labels[i * cols + j].replace(' ', '_')}.py"
                    create_card(image_urls[i * cols + j], labels[i * cols + j], page_name)
else:
    with st.container():
        st.title("Access Blocked!")
        if st.button("Login to Access"):
            st.switch_page("pages/f_login.py")

