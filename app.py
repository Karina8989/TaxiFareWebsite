import streamlit as st
import datetime
import requests
import pandas as pd

def gecode(address):
    params = {'q' : address, 'format' : 'json'}
    places = requests.get(f'https://nominatim.openstreetmap.org/search?', params = params).json()
    return places[0]['lat'], places[0]['lon']


st.markdown('''
# Taxi fare app''')

day = st.date_input("What day?", datetime.date(2019, 7, 6))
st.write('Day:', day)
time = st.time_input('What time?', datetime.time(12, 10, 20))
st.write('Time', time)

#pickup_date = st.date_input('pickup datetime', datetime.datetime(2012, 10, 6, 12, 10, 20))
#pickup_time = st.time_input('pickup datetime', datetime.datetime(2012, 10, 6, 12, 10, 20))
pickup_datetime = f'{day} {time}UTC'

passenger = st.slider('How many passengers?', 1, 6, 1)
st.write('Passenger:', passenger)

pickup_address = st.text_input('Your address', '175 5th Avenue NYC')
st.write('The current address is', pickup_address)

dropoff_address = st.text_input('Destination address', '175 5th Avenue NYC')
st.write('The destination address is', dropoff_address)


pickup = gecode(pickup_address)
dropoff = gecode(dropoff_address)

pickup_longitude = pickup[1]
pickup_latitude = pickup[0]
dropoff_longitude = dropoff[1]
dropoff_latitude = dropoff[0]



key = '2012-10-06 12:10:20.0000001'

params =dict(
    key = key,
    pickup_datetime=pickup_datetime,
    pickup_longitude=float(pickup_longitude),
    pickup_latitude=float(pickup_latitude),
    dropoff_longitude=float(dropoff_longitude),
    dropoff_latitude=float(dropoff_latitude),
    passenger_count=passenger
)


url = 'http://taxifare.lewagon.ai/predict_fare/'

response = requests.get(url, params=params).json()

st.markdown('''
## Price:''')

st.write('The approximate amount is', round(response['prediction'], 2))