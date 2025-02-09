import streamlit as st
from streamlit.components.v1 import html


def style_box(text, border_color, text_color):
    return f"""
    <div style="border: 2px solid {border_color}; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
        <p style="color: {text_color}; font-size: 16px;">{text}</p>
    </div>
    """



st.markdown(
    """<style>

    }
    .main-container {
        max-width: 1200px;
        margin: auto;
    }
    </style>""",
    unsafe_allow_html=True,
)

st.html(f"""<h1 style = "font-size:50px;margin-top:0px;margin-bottom:0px;text-align:center;font-family: 'Georgia', serif;
    font-weight: bold;">HealthSphere</h1>""")
st.markdown(
    """<div class='main-container'>
        <h2 style='color: #ffffff;'>Welcome to Your Healthcare Companion</h2>
        <p>Explore our unique features designed to make healthcare accessible, intuitive, and comprehensive. Below is a detailed explanation of each section of our app.</p>
    </div>""",
    unsafe_allow_html=True,
)


# Section 1: Ask AI
st.markdown("## Ask AI")
st.markdown(
    style_box(
        "HealthSphere AI is your personal medical assistant, equipped to provide insights into your health concerns. You can input your symptoms or medical queries, and the AI will assist with possible conditions and suggest solutions. Additionally, you can upload medical reports for a detailed AI-powered diagnosis. This feature ensures you have reliable, science-backed information to address your health questions.",
        border_color="#28a745",
        text_color="white",
    ),
    unsafe_allow_html=True,
)
st.page_link("views/AskAI.py")
# Section 2: Hospital Finder
st.markdown("## Hospital Finder")
st.markdown(
    style_box(
        "Our Hospital Finder is designed to help you locate medical facilities anywhere in the world. Simply enter your location manually, and the app will provide a list of nearby hospitals, including their addresses and contact details. Alternatively, use the interactive map feature to pinpoint hospitals closest to your chosen location. This functionality ensures that you have access to essential healthcare information whenever you need it.",
        border_color="#28a745",
        text_color="#white",
    ),
    unsafe_allow_html=True,
)
st.page_link("views/hospitals.py")
# Section 3: Fitness (Coming Soon)
st.markdown("## Fitness (Coming Soon)")
st.markdown(
    style_box(
        "Our upcoming Fitness section will leverage AI to revolutionize your fitness journey. This feature will integrate with wearable devices and health monitoring systems to provide real-time insights into your physical activities. It will also include tools for tracking gym workouts and offering personalized fitness advice. Stay tuned for this cutting-edge addition to HealthSphere AI.",
        border_color="#ff0000",
        text_color="#white",
    ),
    unsafe_allow_html=True,
)
st.page_link("views/fitness.py")
st.markdown(
    """<div class='main-container'>
        <p>HealthSphere AI is committed to enhancing your healthcare experience through innovative and reliable solutions. Explore the app and take a step towards better health today.</p>
    </div>""",
    unsafe_allow_html=True,
)







