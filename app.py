import streamlit as st
import pandas as pd
import requests

def fetch_kolumbus_bicycle_data():
    response = requests.get('https://api.kolumbus.no/api/parkings?type=CityBike')
    data = response.json()
    return data

def colorize_marker(available_vehicles, capacity):
    if available_vehicles == 0:
        return '#e16363'
    elif available_vehicles == capacity:
        return '#48c892'
    elif available_vehicles > capacity:
        return '#00ff2e'
    else:
        return '#70b2d5'

def size_marker(available_vehicles, capacity):
    max_size=150
    if available_vehicles == 0:
        return max_size
    return ( available_vehicles / capacity ) * max_size

def convert_to_data_colums(data):
    return map(
        lambda x: [
            x['latitude'],
            x['longitude'],
            colorize_marker(x['available_vehicles'], x['capacity']),
            size_marker(x['available_vehicles'],x['capacity'])
        ], 
        data)

data = fetch_kolumbus_bicycle_data()

empty_slot = filter(lambda x: x['available_vehicles'] == 0, data)
full = filter(lambda x: x['available_vehicles'] == x['capacity'], data)

empty_slot_data = pd.DataFrame(
    convert_to_data_colums(data),
    columns=['lat', 'lon', 'color', 'size'])

st.map(empty_slot_data, color='color', size='size')