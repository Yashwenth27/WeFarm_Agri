import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
try:
    cred = credentials.Certificate('keys/iaaids-9da95-firebase-adminsdk-oy159-374219d78d.json')
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://iaaids-9da95-default-rtdb.firebaseio.com/'})
except:
    pass
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
st.title("Machine Requirements")
st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)


ref = db.reference("machines")
with st.sidebar:
    if st.button("Go Back"):
        try:
            if st.session_state["utype"]=="farmer":
                st.switch_page("pages/f_dash.py")
            elif st.session_state["utype"]=="customer":
                st.switch_page("pages/c_dash.py")
            elif st.session_state["utype"]=="wholer":
                st.switch_page("pages/w_dash.py")
        except:
            st.switch_page("Home_Page.py")

ref = db.reference("machines")
c1,c2,c3 = st.columns(3)
split = 0
datas = ref.get()
for i in datas:
    img = datas[i]["image"]
    types = datas[i]["type"]
    model = datas[i]["model"]
    rent = datas[i]["rent"]
    contact = datas[i]["contact"]
    loc = datas[i]["loc"]
    if split % 3 == 0:
        with c1:
            with st.container(border=True):
                st.image(img)
                st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)
                a,b = st.columns(2)
                with a:
                    st.markdown(f"<h3><u>{i}<u></h3>",unsafe_allow_html=True)
                    st.write(types)
                    st.write(model)
                with b:
                    with st.container(border=True):
                        st.write(rent)
                        st.write("📞"+contact)
                        st.write("📌"+loc)
    elif split % 3 == 1:
        with c2:
            with st.container(border=True):
                st.image(img)
                st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)
                a,b = st.columns(2)
                with a:
                    st.markdown(f"<h3><u>{i}<u></h3>",unsafe_allow_html=True)
                    st.write(types)
                    st.write(model)
                with b:
                    with st.container(border=True):
                        st.write(rent)
                        st.write("📞"+contact)
                        st.write("📌"+loc)
    else:
        with c3:
            with st.container(border=True):
                st.image(img)
                st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)
                a,b = st.columns(2)
                with a:
                    st.markdown(f"<h3><u>{i}<u></h3>",unsafe_allow_html=True)
                    st.write(types)
                    st.write(model)
                with b:
                    with st.container(border=True):
                        st.write(rent)
                        st.write("📞"+contact)
                        st.write("📌"+loc)
    split+=1

with st.expander("Want to Sell Machines?"):
    st.subheader("Application For Selling Machineries:")
    k,l = st.columns(2)
    with k:
        mname=st.text_input("Machine Name")
        types=st.text_input("Machine Type")
        model=st.text_input("Model")
        image=st.text_input("Image URL")
    with l:
        rent=st.text_input("Seller Name")
        contact=st.text_input("Contact")
        loc=st.text_input("Location")
        m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: green;
        color: white;
        width: 200px;
        text-alingn: center;
    }
    </style>""", unsafe_allow_html=True)
        if st.button("Upload"):
            ref.child(mname).set(
                {
                    "type":types,
                    "model":model,
                    "image":image,
                    "rent":rent,
                    "contact":contact,
                    "loc":loc
                }
            )