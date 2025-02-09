import streamlit as st

home_page = st.Page(page="views/Home.py",title="Home",default = True)
hospital_location = st.Page(page="views/hospitals.py",title="Hospital Finder")
fitness = st.Page(page="views/fitness.py",title="Fitness")
ask_ai = st.Page(page="views/AskAI.py",title="AskAI")

st.markdown("""<style>
.st-emotion-cache-h4xjwg {
    
display : none }
body {
        background-color: #101820;
        color: #F2F4F3;
        font-family: 'Arial', sans-serif;


</style>""",unsafe_allow_html=True)

pg = st.navigation(pages=[home_page, ask_ai ,hospital_location,fitness])
pg.run()