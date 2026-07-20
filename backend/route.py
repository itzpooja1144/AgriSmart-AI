from flask import Blueprint, request, render_template, redirect, jsonify
import pickle
import numpy as np
import os
import pandas as pd
import requests          
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from dotenv import load_dotenv
from groq import Groq
from dotenv import load_dotenv
import os

API_KEY = "16b017cbcad811efce8a81b7b7b2d542"

with open("../ML_Model/crop_model.pkl", "rb") as f:
    crop_model = pickle.load(f)
route = Blueprint("route", __name__)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ===============================
# LOAD CNN MODEL
# ===============================

cnn_model = tf.keras.models.load_model(
    "../ML_Model/disease_model.keras"
)


with open("../ML_Model/disease_classes.pkl", "rb") as f:
    disease_classes = pickle.load(f)
# ===============================
# LOAD DISEASE CSV
# ===============================

disease_data = pd.read_csv(
    "../datasets/disease_data.csv"
)



# ===============================
# HOME PAGE
# ===============================

@route.route("/")
def index():
    return redirect("/dashboard")
# ===============================
# DASHBOARD
# ===============================



@route.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    weather = None
    city = "Karnal"

    if request.method == "POST":
        city = request.form.get("city")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:

        condition = data["weather"][0]["main"]

        if condition == "Clear":
            condition = "Sunny"
        elif condition == "Clouds":
            condition = "Cloudy"
        elif condition == "Rain":
            condition = "Rainy"
        else:
            condition = data["weather"][0]["description"].title()

        weather = {
            "city": "Punjab",
            "temperature": round(data["main"]["temp"]),
            "humidity": data["main"]["humidity"],
            "condition": condition,
            "icon": data["weather"][0]["icon"],
            "wind": data["wind"]["speed"]
        }

    return render_template(
        "dashboard.html",
        weather=weather
    )

# ===============================
# CROP PAGE
# ===============================

@route.route("/crop")
def crop_page():

    return render_template("crop.html")
# ===============================
# MARKET PRICE PREDICTION
# ===============================

@route.route("/market")
def market_page():

    return render_template("market.html")



@route.route("/predict_market", methods=["POST"])
def predict_market():

    crop_name = request.form.get("crop_name")
    market_name = request.form.get("market_name")
    region = request.form.get("region")


    prices = {

        "Wheat": {
            "government": 2425,
            "mandi": 2350,
            "private": 2480
        },

        "Rice": {
            "government": 2369,
            "mandi": 3200,
            "private": 3350
        },

        "Maize": {
            "government": 2225,
            "mandi": 2100,
            "private": 2250
        },

        "Cotton": {
            "government": 7521,
            "mandi": 6500,
            "private": 6800
        },

        "Sugarcane": {
            "government": 3400,
            "mandi": 3800,
            "private": 4000
        }
    }


    price = prices.get(
        crop_name,
        {
            "government":0,
            "mandi":0,
            "private":0
        }
    )


    return render_template(
        "market_result.html",
        crop=crop_name,
        market=market_name,
        region=region,
        price=price
    )
# ===============================
# DISEASE PAGE
# ===============================

@route.route("/disease")
def disease_page():

    return render_template("disease.html")



# ===============================
# DISEASE PREDICTION
# ===============================

@route.route("/predict_disease", methods=["POST"])
def predict_disease():


    image_file = request.files["leaf_image"]


    upload_folder = "../uploads"


    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)



    file_path = os.path.join(
        upload_folder,
        image_file.filename
    )


    image_file.save(file_path)



    # IMAGE PROCESSING

    img = image.load_img(
        file_path,
        target_size=(128,128)
    )


    img_array = image.img_to_array(img)


    img_array = np.expand_dims(
        img_array,
        axis=0
    )


    img_array = img_array / 255.0



    # MODEL PREDICTION

    prediction = cnn_model.predict(img_array)


    disease_index = np.argmax(prediction)


    disease = disease_classes[disease_index]


    confidence = np.max(prediction) * 100



    # CSV MATCHING

    clean_name = disease.lower().replace("_"," ")


    info = disease_data[
        disease_data["disease"]
        .str.lower()
        .apply(lambda x: x in clean_name)
    ]



    if not info.empty:

        crop_name = info.iloc[0]["crop_name"]
        severity = info.iloc[0]["severity"]
        symptoms = info.iloc[0]["symptoms"]
        treatment = info.iloc[0]["treatment"]

    else:

        crop_name = "Not Available"
        severity = "Not Available"
        symptoms = "Not Available"
        treatment = "Not Available"



    return render_template(
    "disease_result.html",

    image_name=image_file.filename,

    crop_name=crop_name,

    disease=disease,

    confidence=round(confidence, 2),

    severity=severity,

    symptoms=symptoms,

    treatment=treatment
)
# ===============================
# CROP PREDICTION
# ===============================

@route.route("/predict_crop", methods=["POST"])
def predict_crop():

    N = float(request.form.get("N"))
    P = float(request.form.get("P"))
    K = float(request.form.get("K"))
    temperature = float(request.form.get("temperature"))
    humidity = float(request.form.get("humidity"))
    rainfall = float(request.form.get("rainfall"))

    data = [[
        N,
        P,
        K,
        temperature,
        humidity,
        rainfall
    ]]

    crop = crop_model.predict(data)[0]

    return render_template(
        "crop_result.html",
        N=N,
        P=P,
        K=K,
        temperature=temperature,
        humidity=humidity,
        rainfall=rainfall,
        crop=crop
    )

@route.route("/weather", methods=["GET", "POST"])
def weather():

    weather = None
    city = "Karnal"

    if request.method == "POST":
        city = request.form.get("city")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather = {
            "city": data["name"],
            "temperature": round(data["main"]["temp"]),
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "wind": data["wind"]["speed"]
        }

    return render_template(
        "weather.html",
        weather=weather
    )
@route.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


@route.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()
    message = data.get("message")

    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are AgriSmart AI, an agriculture expert.

Rules:
- Reply in the same language as the user's question (Hindi, Punjabi, or English).
- Maximum 100 words.
- Use bullet points.
- Give practical farming advice.
- Be friendly and simple.
- If the user greets you (Hi, Hello, Kaise ho, Kive a), respond with a short friendly greeting and ask how you can help with farming.
"""
},
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.5,
            max_tokens=200
        )

        return jsonify({
            "reply": chat_completion.choices[0].message.content
        })

    except Exception as e:
        return jsonify({
            "reply": str(e)
        })