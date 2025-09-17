import streamlit as st
import requests

#TODO: Update with your FastAPI URL
FASTAPI_URL = "http://fastapi:8000/predict"

st.title("Customer Satisfaction Classifier")


gender = st.selectbox('Pick a gender', ['male', 'female'])
customer_type = st.selectbox('Pick a customer type', ['Loyal Customer', 'disloyal Customer'])
age = st.number_input('Age', min_value=0, max_value=120, value=30)
type_of_travel = st.selectbox('Pick a type of travel', ['Personal Travel', 'Business travel'])
class_of_service = st.selectbox('Pick a class of service', ['Eco', 'Eco Plus', 'Business'])
flight_distance = st.number_input('Flight distance', min_value=0, value=500)
inflight_wifi_service = st.number_input('Inflight wifi service (1-5)', min_value=1, max_value=5, value=3)
departure_arrival_time_convenient = st.number_input('Departure/Arrival time convenient (1-5)', min_value=1, max_value=5, value=3)
ease_of_online_booking = st.number_input('Ease of online booking (1-5)', min_value=1, max_value=5, value=3)
gate_location = st.number_input('Gate location (1-5)', min_value=1, max_value=5, value=3)
food_and_drink = st.number_input('Food and drink (1-5)', min_value=1, max_value=5, value=3)
online_boarding = st.number_input('Online boarding (1-5)', min_value=1, max_value=5, value=3)
seat_comfort = st.number_input('Seat comfort (1-5)', min_value=1, max_value=5, value=3)
inflight_entertainment = st.number_input('Inflight entertainment (1-5)', min_value=1, max_value=5, value=3)
onboard_service = st.number_input('Onboard service (1-5)', min_value=1, max_value=5, value=3)
leg_room_service = st.number_input('Leg room service (1-5)', min_value=1, max_value=5, value=3)
baggage_handling = st.number_input('Baggage handling (1-5)', min_value=1, max_value=5, value=3)
checkin_service = st.number_input('Checkin service (1-5)', min_value=1, max_value=5, value=3)
inflight_service = st.number_input('Inflight service (1-5)', min_value=1, max_value=5, value=3)
cleanliness = st.number_input('Cleanliness (1-5)', min_value=1, max_value=5, value=3)
departure_delay_in_minutes = st.number_input('Departure delay in minutes', min_value=0, value=0)
arrival_delay_in_minutes = st.number_input('Arrival delay in minutes', min_value=0, value=0)

if st.button("Predict"):
    input_data = {
        "gender": gender,
        "customer_type": customer_type,
        "age": age,
        "type_of_travel": type_of_travel,
        "class_of_service": class_of_service,
        "flight_distance": flight_distance,
        "inflight_wifi_service": inflight_wifi_service,
        "departure_arrival_time_convenient": departure_arrival_time_convenient,
        "ease_of_online_booking": ease_of_online_booking,
        "gate_location": gate_location,
        "food_and_drink": food_and_drink,
        "online_boarding": online_boarding,
        "seat_comfort": seat_comfort,
        "inflight_entertainment": inflight_entertainment,
        "onboard_service": onboard_service,
        "leg_room_service": leg_room_service,
        "baggage_handling": baggage_handling,
        "checkin_service": checkin_service,
        "inflight_service": inflight_service,
        "cleanliness": cleanliness,
        "departure_delay_in_minutes": departure_delay_in_minutes,
        "arrival_delay_in_minutes": arrival_delay_in_minutes,
    }
    
    response = requests.post(FASTAPI_URL, json=input_data)
    prediction = response.json()["satisfaction"]
    
    st.success(f"The model predicts satisfaction: {prediction}")