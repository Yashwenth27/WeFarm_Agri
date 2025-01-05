import streamlit as st
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
page = st_navbar(pages, styles=styles, selected="About Us",logo_path="pages/ZenTech_Logo.svg")
if page=="Home":
    if st.session_state["utype"]=="farmer":
        st.switch_page("pages/f_dash.py")
    elif st.session_state["utype"]=="customer":
        st.switch_page("pages/c_dash.py")
    elif st.session_state["utype"]=="wholer":
        st.switch_page("pages/w_dash.py")
if page=="Log out":
    st.switch_page("Home_Page.py")
st.title("About Us")
st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)
st.markdown(
    '''
<style>
        body {
            background-color: white;
            color: black;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .container {
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h2 {
            color: green;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        h4 {
            color: green;
            font-size: 1.7em;
            margin-top: 20px;
        }
        p {
            text-align: justify;
            line-height: 1.6;
            font-size: 1.5em;
        }
    </style>''',unsafe_allow_html=True)
st.write('''
    <div class="container">
        <h2><u>Intelligent Agri-App Information Dissemination System (IAAIDS)</u></h2>
        <p>Welcome to IAAIDS, your ultimate agricultural technology partner. Our innovative web application offers a customized dashboard for farmers, customers, and wholesalers, integrating advanced tools and real-time data to elevate farming efficiency and market connectivity.</p>
        <h4><u>Features:</u></h4>
        <h4>1. Weather Forecast</h4>
        <p>Stay ahead with precise weather forecasts, enabling farmers to plan their activities efficiently and mitigate weather-related risks.</p>
        <h4>2. Real-Time Soil Information</h4>
        <p>Harnessing IoT technology, our app provides live soil data through sensors embedded in farmlands. Monitor moisture, pH, and nutrient levels in real time to make informed soil management decisions.</p>
        <h4>3. Crop Demand Insights</h4>
        <p>Align your production with market needs using our crop demand feature. Farmers can see which crops are in high demand based on customer quotes within the app, ensuring strategic and profitable planting decisions.</p>
        <h4>4. Buyer and Seller Connectivity</h4>
        <p>IAAIDS connects you with the right people:</p>
        <ul>
            <li><strong><p>Buyer Details:</strong> Access information and contact details of customers seeking to purchase your produce.</p></li>
            <li><strong><p>Seller Information:</strong> Easily find and connect with sellers offering farming machinery, streamlining your procurement process.</p></li>
        </ul>
        <h4>5. Disease Detection</h4>
        <p>Our advanced machine learning model analyzes tomato plant leaves to detect diseases with 99.2% accuracy. Receive timely diagnoses and effective remedies to maintain healthy crops and reduce losses.</p>
        <p>IAAIDS is dedicated to empowering farmers with cutting-edge technology, fostering a smarter, more sustainable agricultural ecosystem. Join us in transforming agriculture for a better future.</p>
    </div>
'''
,unsafe_allow_html=True)

st.write("---")
st.subheader("Users Comments:")
a,b = st.columns(2)
with a:
    with st.container(border=True):
        st.write("⭐⭐⭐⭐")
        st.write(
            '"Absolutely love how IAAIDS integrates cutting-edge tech to boost farming efficiency—this is the future of agriculture!"'
        )
        st.caption("~Yashwenth S")
    with st.container(border=True):
        st.write("⭐⭐⭐⭐⭐")
        st.write(
            '"Incredible initiative! The real-time soil info and disease detection features are game-changers for farmers."'
        )
        st.caption("~Ramanan")
with b:
    with st.container(border=True):
        st.write("⭐⭐⭐⭐⭐")
        st.write(
            '"IAAIDS is revolutionizing agriculture with its smart dashboard and weather forecasts—cant wait to see more!"'
        )
        st.caption("~Kishore")
    with st.container(border=True):
        st.write("⭐⭐⭐⭐")
        st.write(
            '"Kudos to the IAAIDS team for such an innovative app—helping farmers make informed decisions has never been easier!"'
        )
        st.caption("~Vishnu")

st.write("---")
st.subheader("Write to Us")
with st.expander("Click Here!"):
    message = st.text_area("Message","Your Message!",max_chars=500)
    if st.button("Send 📧"):
        st.success("Your Message Sent to the team.. We will Get back to you soon...✌🏻")