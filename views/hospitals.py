import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from scraper import scrape_hospitals  # Import the scraper function

st.html(f"""<h1 style="font-size:50px;margin-top:0px;margin-bottom:0px;text-align:center;
    font-family: 'Georgia', serif; font-weight: bold;">Hospital Finder</h1>""")

# Initialize session state
if "select_box" not in st.session_state:
    st.session_state["select_box"] = None
if "latitude" not in st.session_state:
    st.session_state["latitude"] = None
if "longitude" not in st.session_state:
    st.session_state["longitude"] = None

# Sidebar options
with st.sidebar:
    st.title("Features")
    select_Box = st.selectbox("", options=["Manual", "Use Map 🔥"])
    st.session_state["select_box"] = select_Box
    st.caption("The Hospital Finder app extracts hospital details from Google Maps, providing names, addresses, contact numbers, and websites. It enables fast, automated searches across locations, ensuring easy access to healthcare facilities. With CSV and Excel exports, users can efficiently store and analyze hospital data for informed decision-making.")

# Custom styles
st.markdown("<style>.st-emotion-cache-b0y9n5 {border:none}</style>", unsafe_allow_html=True)
st.markdown("<style>.st-emotion-cache-1tvzk6f {border-radius: 25px; border: 2px solid rgb(277,66,52)}</style>", unsafe_allow_html=True)

# Function to find hospitals
def find_hospitals(location, message):
    if location:
        with st.spinner("Fetching hospital data... Please wait."):
            csv_file = scrape_hospitals(location, search_type=message)  # Call scraper function
            
        if csv_file:
            st.caption(f"Here are some hospitals in {location.replace(' ', '_')}")
            try:
                data = pd.read_csv(csv_file)
                st.dataframe(data)  # Display data as a table
            except pd.errors.EmptyDataError:
                st.error("No data found for this location. Please try another place.")
        else:
            st.error("An error occurred while retrieving hospital data.")
    else:
        st.error("Please enter a location!")

# Function to get address from coordinates
def get_address(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data.get("display_name", "Address not found")
    else:
        return "Error: Unable to fetch address"

# Map-based search
if st.session_state["select_box"] == "Use Map 🔥":
    st.caption("Select a location on the map to find hospitals nearby.")
    m = folium.Map(location=[28.679079, 77.069710], zoom_start=10)

    folium.Marker([28.679079, 77.069710], popup="Delhi", tooltip="Delhi").add_to(m)

    st_data = st_folium(m, width=725)

    if st_data and "last_clicked" in st_data and st_data["last_clicked"]:
        st.session_state["latitude"] = st_data["last_clicked"]["lat"]
        st.session_state["longitude"] = st_data["last_clicked"]["lng"]

    if st.session_state["latitude"] is not None and st.button("Find Hospitals"):
        address = get_address(st.session_state["latitude"], st.session_state["longitude"])
        st.write(f"Address: {address}")
        find_hospitals(address, "in or near")

# Manual search
if st.session_state["select_box"] == "Manual":
    location = st.text_input("Enter the city or location to search for hospitals:")
    if st.button("Find Hospitals"):
        find_hospitals(location, "in or near")








