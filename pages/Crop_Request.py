import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from streamlit_extras.let_it_rain import rain
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

st.title("Crop Request")
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
a,b = st.columns(2)
with a:
    with st.container(border=True):
        st.subheader("Request A Crop!")
        st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)
        cname = st.text_input("Crop Name")
        c,d = st.columns(2)
        with c:
            qty = st.text_input("Quantity Required")
        with d:
            unit = st.selectbox("Unit",["Kgs","Ton"])
        loc = st.text_input("Location")
        if st.button("Upload Request"):
            st.balloons()
            ref = db.reference("requests")
            ref2 = db.reference("credentials")
            ref.child(ref2.child("Customer").child(st.session_state["user_id"]).child("fullname").get()+","+cname).set(
                {
                    "crop":cname,
                    "qty":qty,
                    "unit":unit,
                    "loc":loc
                }
            )
            st.experimental_rerun()
with b:
    with st.container(border=True):
        st.subheader("Crops on Demand")
        st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)
        ref = db.reference("requests")
    #try:
        data = ref.get()
        kv = {}
        for i in data:
            crop_name = data[i]["crop"].title()
            quantity = data[i]["qty"]
            metric_unit = data[i]["unit"]
            if crop_name not in kv:
                if metric_unit=="Kgs":
                    kv[crop_name]=(float(quantity)*0.001)
                else:
                    kv[crop_name]=(float(quantity))
            else:
                if metric_unit=="Kgs":
                    kv[crop_name]=kv[crop_name]+(float(quantity)*0.001)
                else:
                    kv[crop_name]=kv[crop_name]+(float(quantity))
        oe = 0
        u,y = st.columns(2)
        for i in kv:
            if oe%2==0:
                with u:
                    with st.container(border=True):
                        st.metric(i.split(",")[0],str(kv[i])+" Tons")
            else:
                with y:
                    with st.container(border=True):
                        st.metric(i.split(",")[0],str(kv[i])+" Tons")
            oe+=1

with st.container(border=True):
    st.subheader("All Requests")
    st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)
    ref = db.reference("requests")
    try:
        data = ref.get()
        oep = 0
        p,l,m,h = st.columns(4)
        for i in data:
            if oep%4==0:
                with p:
                    with st.container(border=True):
                        st.write(i.split(",")[0]+" requested,")
                        st.subheader(data[i]["qty"]+" "+data[i]["unit"])
                        st.write(data[i]["crop"] + "\t📍"+data[i]["loc"])
            elif oep%4==1:
                with l:
                    with st.container(border=True):
                        st.write(i.split(",")[0]+" requested,")
                        st.subheader(data[i]["qty"]+" "+data[i]["unit"])
                        st.write(data[i]["crop"] + "\t📍"+data[i]["loc"])
            elif oep%4==2:
                with m:
                    with st.container(border=True):
                        st.write(i.split(",")[0]+" requested,")
                        st.subheader(data[i]["qty"]+" "+data[i]["unit"])
                        st.write(data[i]["crop"] + "\t📍"+data[i]["loc"])
            else:
                with h:
                    with st.container(border=True):
                        st.write(i.split(",")[0]+" requested,")
                        st.subheader(data[i]["qty"]+" "+data[i]["unit"])
                        st.write(data[i]["crop"] + "\t📍"+data[i]["loc"])
            oep+=1
    except:
        st.warning("No demands at present")
        

# if st.button("Go Back"):
#     if st.session_state["utype"]=="farmer":
#         st.switch_page("pages/f_dash.py")
#     elif st.session_state["utype"]=="customer":
#         st.switch_page("pages/c_dash.py")
#     elif st.session_state["utype"]=="wholer":
#         st.switch_page("pages/w_dash.py")

rain(
    "🥕",
    64,
    5,
    "infinite"
)