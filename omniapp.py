import math
import streamlit as st
import numpy as np
import datetime
import requests
import pandas as pd

# Function to retrieve weather data using OpenWeatherMap API
def get_weather_data(city):
    api_key = '251597c2f184b437e4411235bdd71fec'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        return temperature, humidity
    else:
        st.error(f'Error: Unable to fetch weather data for {city}')
        return None, None

# Function to calculate wet bulb temperature using the new formula
def calculate_wet_bulb_temperature(T, RH):
    # Convert RH to a ratio
    RH_ratio = RH 
    # Apply the new formula
    tw = T * math.atan(0.151977 * np.sqrt(RH_ratio + 8.313659)) + \
         0.00391838 * np.sqrt(RH_ratio*RH_ratio*RH_ratio) * math.atan(0.023101 * RH_ratio) - \
         math.atan(RH_ratio - 1.676331) + \
         math.atan(T + RH_ratio) - 4.686035
         
    return tw

st.set_page_config(layout="wide", page_title="Omni Calculator")
st.title("🖩 Wet Bulb Calculator")

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

city_options = [
    "Hyderabad", "Bengaluru", "Mumbai", "Jaipur", "Chandigarh", "Chennai", "Kolkata",
    "Lucknow", "Ahmedabad", "Surat", "Visakhapatnam", "Nagpur", "Amritsar", "Nashik",
    "Bhopal", "Agra", "Patna", "Kanpur", "Pune", "Jamshedpur", "Bhubaneswar", "Warangal",
    "Kochi", "Meerut", "Vijayawada", "Indore", "Vadodara", "Varanasi", "Faridabad",
    "Ghaziabad", "Coimbatore", "Mangaluru", "Dehradun", "Mysuru", "Ludhiana", "Rajkot",
    "Kalaburagi", "Belagavi", "Anantapur", "Madurai", "Raipur", "Salem", "Bikaner", "Jhansi",
    "Cuttack", "Ajmer", "Udaipur", "Prayagraj", "Aurangabad", "New Delhi", "Navi Mumbai"
]

additional_cities = [
    "Yamunanagar", "Warangal", "Vijayanagaram", "Vellore", "Unnao", "Uluberia", "Ulhasnagar", "Ujjain", "Udaipur",
    "Tumkur", "Tiruvottiyur", "Tiruppur", "Tirupati", "Tirunelveli", "Tiruchirappalli", "Thrissur", "Thoothukudi",
    "Thiruvananthapuram", "Thanjavur", "Tenali", "Tadipatri", "Tadepalligudem", "Suryapet", "Surendranagar Dudhrej",
    "Sultan Pur Majra", "Srikakulam", "Sri Ganganagar", "South Dumdum", "Sonipat", "Solapur", "Siwan", "Sirsa",
    "Singrauli", "Siliguri", "Sikar", "Shivpuri", "Shivamogga", "Shimla", "Shahjahanpur", "Serampore", "Secunderabad",
    "Satna", "Satara", "Sasaram", "Sangli-Miraj & Kupwad", "Sambhal", "Sambalpur", "Sambalpur", "Salem", "Saharsa",
    "Saharanpur", "Sagar", "Rourkela", "Rourkela", "Rohtak", "Rewa", "Raurkela Industrial Township", "Ratlam", "Rampur",
    "Ramagundam", "Rajpur Sonarpur", "Rajahmundry", "Raiganj", "Raichur", "Rae Bareli", "Purnia", "Puducherry",
    "Proddatur", "Patiala", "Parbhani", "Panvel", "Panipat", "Panihati", "Panchkula", "Pallavaram", "Pali", "Ozhukarai",
    "Orai", "Ongole", "North Dumdum", "Noida", "Nizamabad", "New Delhi", "Nellore", "Navi Mumbai Panvel Raigad",
    "Narasaraopet", "Nangloi Jat", "Nandyal", "Nanded", "Naihati", "Nagarcoil", "Nadiad", "Mysore", "Muzaffarpur",
    "Muzaffarnagar", "Murwara", "Munger", "Motihari", "Morvi", "Morena", "Moradabad", "Mirzapur", "Miryalaguda",
    "Mira-Bhayandar", "Mau", "Mathura", "Mango", "Mangalore", "Malegaon", "Malda", "Maheshtala", "Mahesana", "Madhyamgram",
    "Madanapalle", "Machilipatnam", "Loni", "Latur", "Kurnool", "Kulti", "Kozhikode", "Kottayam", "Korba", "Kollam",
    "Kolhapur", "Kochi", "Kishanganj", "Kirari Suleman Nagar", "Khora", "Kharagpur", "Khandwa", "Khammam", "Kavali",
    "Katihar", "Karnal", "Karimnagar", "Karawal Nagar", "Karaikudi", "Kamarhati", "Kakinada", "Kadapa", "Junagadh",
    "Jhansi", "Jehanabad", "Jaunpur", "Jamshedpur", "Jamnagar", "Jammu", "Jamalpur", "Jalna", "Jalgaon", "Jalandhar",
    "Imphal", "Ichalkaranji", "Hugli and Chinsurah", "Hubballi-Dharwad", "Hospet", "Hindupur", "Haridwar", "Hapur",
    "Haldia", "Hajipur", "Guwahati", "Gurgaon", "Guntur", "Guntakal", "Guna", "Gulbarga", "Gudivada", "Gorakhpur",
    "Gopalpur", "Gaya", "Gandhinagar", "Gandhidham", "Firozabad", "Fatehpur", "Farrukhabad", "Etawah", "Erode",
    "Eluru", "Durgapur", "Durg", "Dindigul", "Dhule", "Dharmavaram", "Dewas", "Deoghar", "Dehri", "Dehradun", "Davanagere",
    "Darbhanga", "Danapur", "Cuttack", "Chittoor", "Chapra", "Chandrapur", "Chandigarh", "Buxar", "Burhanpur", "Bulandshahr",
    "Bokaro", "Bilaspur", "Bikaner", "Bijapur", "Bihar Sharif", "Bidhan Nagar", "Bidar", "Bhusawal", "Bhubaneswar", "Bhiwani",
    "Bhiwandi", "Bhind", "Bhimavaram", "Bhilwara", "Bhilai", "Bhavnagar", "Bhatpara", "Bharatpur", "Bhalswa Jahangir Pur",
    "Bhagalpur", "Bettiah", "Berhampur", "Bellary", "Belgaum", "Begusarai", "Bathinda", "Bareily", "Bardhaman", "Barasat",
    "Baranagar", "Bally", "Bahraich", "Baharampur", "Bagaha", "Avadi", "Aurangabad", "Asansol", "Arrah", "Anantapur", "Anand",
    "Amroha", "Amravati", "Ambernath", "Ambattur", "Ambala", "Amaravati"
]


city_options.extend(additional_cities)


selected_city = st.selectbox("Select a city", city_options)

temperature, humidity = get_weather_data(selected_city)

if st.button("calculate Wet bulb Temperature"):
        st.header("Results")
        # Calculate Wet Bulb Temperature
        tw = calculate_wet_bulb_temperature(temperature, humidity)
        # Display results
        st.write(f'⌚️Time:{current_time}')
        st.info(f'🌇City: {selected_city}')
        st.info(f'🌡Temperature: {temperature}°C')
        st.info(f'💧Humidity: {humidity}%')
        st.info(f'🌡Wet Bulb Temperature: {tw:.2f}°C')

# Initialize variables to store input values
temperature = 0
humidity = 0
st.header("Slider")

# Slider for temperature
st.subheader("Adjust Temperature:")
temperature = st.slider("Temperature (°C)", 0, 100, key="temperature_input")

    # Slider for humidity
st.subheader("Adjust Humidity:")
humidity = st.slider("Humidity (%)", 0, 100, key="humidity_input")

if st.button("Calculate Wet Bulb Temperature"):
    st.header("Results")
    # Calculate Wet Bulb Temperature
    tw = calculate_wet_bulb_temperature(temperature, humidity)
    # Display results
    st.info(f'🌡 Temperature: {temperature}°C')
    st.info(f'💧 Humidity: {humidity}%')
    st.info(f'🌡 Wet Bulb Temperature: {tw:.2f}°C')

