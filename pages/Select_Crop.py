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
st.title("Select Crop")
st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)
ref = db.reference("requests")
data = ref.get()
kv = {}
kv2 = {}
for i in data:
    crop_name = data[i]["crop"].title()
    quantity = data[i]["qty"]
    metric_unit = data[i]["unit"]
    location = data[i]["loc"].title()
    if location not in kv2:
        if metric_unit=="Kgs":
            kv2[location]=[(crop_name,(float(quantity)*0.001))]
        else:
            kv2[location]=[(crop_name,(float(quantity)))]
    else:
        if metric_unit=="Kgs":
            kv2[location].append((crop_name,(float(quantity)*0.001)))
        else:
            kv2[location].append((crop_name,(float(quantity))))
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

col1,col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.subheader("Crops on Demand")
        st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)
    #try:
        oe = 0
        u,y,o = st.columns(3)
        for i in kv:
            if oe%3==0:
                with u:
                    with st.container(border=True):
                        if float(kv[i])<1.0:
                            st.metric(i.split(",")[0],str(float(kv[i])*1000)+" KGs")
                        else:
                            st.metric(i.split(",")[0],str(kv[i])+" Tons")
            elif oe%3==1:
                with y:
                    with st.container(border=True):
                        if float(kv[i])<1.0:
                            st.metric(i.split(",")[0],str(float(kv[i])*1000)+" KGs")
                        else:
                            st.metric(i.split(",")[0],str(kv[i])+" Tons")
            else:
                with o:
                    with st.container(border=True):
                        if float(kv[i])<1.0:
                            st.metric(i.split(",")[0],str(float(kv[i])*1000)+" KGs")
                        else:
                            st.metric(i.split(",")[0],str(kv[i])+" Tons")
            oe+=1
with col2:
    with st.container(border=True):
        st.subheader("Location Based Demand")
        st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)
        locs = []
        for i in kv2:
            locs.append(i)
        loca = st.selectbox("Search Based on Location",locs)
        if st.button("Search!"):
            for i in data:
                name = i.split(",")[0]
                if loca==data[i]["loc"]:
                    with st.chat_message("user",avatar="📦"):
                        with st.expander(data[i]["qty"]+" "+data[i]["unit"]+" of "+data[i]["crop"]):
                            with st.container(border=True):
                                st.write(name)
                                ref2 = db.reference("credentials/Customer")
                                data2 = ref2.get()
                                for i in data2:
                                    if data2[i]["fullname"]==name:
                                        mobile = data2[i]["mobile"]
                                        email = data2[i]["email"]
                                st.write("📞: "+mobile)
                                st.write("📧: "+email)

# if st.button("Go Back"):
#     if st.session_state["utype"]=="farmer":
#         st.switch_page("pages/f_dash.py")
#     elif st.session_state["utype"]=="customer":
#         st.switch_page("pages/c_dash.py")
#     elif st.session_state["utype"]=="wholer":
#         st.switch_page("pages/w_dash.py")
