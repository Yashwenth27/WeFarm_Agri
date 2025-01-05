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
if st.button("Go Back"):
    if st.session_state["utype"]=="farmer":
        st.switch_page("pages/f_dash.py")
    elif st.session_state["utype"]=="customer":
        st.switch_page("pages/c_dash.py")
    elif st.session_state["utype"]=="wholer":
        st.switch_page("pages/w_dash.py")
st.title("Wtf")