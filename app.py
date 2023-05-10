import numpy as np
import pandas as pd
import pickle
import streamlit as st
import json
import math
import base64

result = None

with open(r"C:\Users\abhil\OneDrive\Desktop\Project\HOUSE PRICES PREDICTION\bangalore_house_prices_model.pickle", 'rb') as f:
    __model = pickle.load(f)

with open(r"C:\Users\abhil\OneDrive\Desktop\Project\HOUSE PRICES PREDICTION\columns.json", "r") as f:
    __data_columns = json.load(f)['data_columns']
    __locations = __data_columns[3:]


def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    lis = np.zeros(len(__data_columns))
    lis[0] = sqft
    lis[1] = bath
    lis[2] = bhk
    if loc_index >= 0:
        lis[loc_index] = 1

    price = round(__model.predict([lis])[0], 2)
    strp = ' lakhs'

    if math.log10(price) >= 2:
        price = price / 100
        price = round(price, 2)
        strp = " crores"

    return str(price) + strp


def main() -> object:
    global result
    st.title("Bangalore House Price Predictor")
    html_temp = """
           <div>
           <h2>House Price Prediction ML app</h2>
           </div>
           """
    st.markdown(html_temp, unsafe_allow_html=True)

    sqft = st.slider('Select the square footage of the house:', 500, 5000, step=100, value=1000)
    bhk = st.radio("BHK", (1, 2, 3, 4, 5, 6))
    bath = st.number_input("Number of Bathrooms", min_value=1, step=1)
    location = st.selectbox("Select the Location", __locations)

    if st.button("Predict"):
        result = get_estimated_price(location, sqft, bhk, bath)

    st.success(f"Price = {result}")


if __name__ == "__main__":
    main()