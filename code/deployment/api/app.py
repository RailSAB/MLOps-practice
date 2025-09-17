from fastapi import FastAPI
from pydantic import BaseModel
import joblib


# with open("/Users/rail/Pet-projects/MLOps-practice/models/logreg_best3.pkl", "rb") as f:
#     model = pickle.load(f)

# with open("/Users/rail/Pet-projects/MLOps-practice/models/scaler.pkl", "rb") as f:
#     scaler = pickle.load(f)
model = joblib.load("models/logreg_best3.pkl")
scaler = joblib.load("models/scaler.pkl")

app = FastAPI()

class CustomerData(BaseModel):
    gender: str
    customer_type: str
    age: int
    type_of_travel: str
    class_of_service: str
    flight_distance: int
    inflight_wifi_service: int
    departure_arrival_time_convenient: int
    ease_of_online_booking: int
    gate_location: int
    food_and_drink: int
    online_boarding: int
    seat_comfort: int
    inflight_entertainment: int
    onboard_service: int
    leg_room_service: int
    baggage_handling: int
    checkin_service: int
    inflight_service: int
    cleanliness: int
    departure_delay_in_minutes: int
    arrival_delay_in_minutes: int

@app.post("/predict")
def predict_satisfaction(data: CustomerData):

    input_data = [[
        data.age,
        data.flight_distance,
        data.inflight_wifi_service,
        data.departure_arrival_time_convenient,
        data.ease_of_online_booking,
        data.gate_location,
        data.food_and_drink,
        data.online_boarding,
        data.seat_comfort,
        data.inflight_entertainment,
        data.onboard_service,
        data.leg_room_service,
        data.baggage_handling,  
        data.checkin_service,
        data.inflight_service,
        data.cleanliness,
        data.departure_delay_in_minutes,
        data.arrival_delay_in_minutes,
        1 if data.gender == "male" else 0,
        1 if data.customer_type == "Loyal Customer" else 0,
        1 if data.type_of_travel == "Personal Travel" else 0,
        1 if data.class_of_service == "Eco" else 0,
        1 if data.class_of_service == "Eco Plus" else 0
    ]]

    # apply standard scaling from training

    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    return {"satisfaction": int(prediction[0])}

