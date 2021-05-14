import streamlit as st

import psycopg2
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn 
import datetime 
import io

engine = create_engine('postgres://dennisssekamaanya:dennis123@localhost:5432/dennisssekamaanya')
st.write('''
# Welcome to Streamlit!
We shall use this app to expore and analyze our flight dataset
''')
st.write('''
1. 10 airlines with worst departure delay:
''')
button = st.button('Departure Delay by Airline')
if button: 
    data = pd.read_sql_query('''SELECT airline, AVG(departure_delay) AS dep_delay FROM "flight_data" 
    GROUP BY airline
    ORDER BY dep_delay desc ''', con=engine)
    st.dataframe(data)


st.write('''
2. Airports with Worst Departure Delay
''')
button = st.button('Departure Delay by Airport')
if button:
    data = pd.read_sql('''
    SELECT origin_airport, AVG(departure_delay AS Dep_Delay, air_system_delay, security_delay, airline_delay), 
    late_aircraft_delay, weather_delay FROM flight_data
    GROUP BY origin_airport, air_system_delay, security_delay, airline_delay, 
    airline_delay, late_aircraft_delay, weather_delay
    ORDER BY Dep_Delay desc
    LIMIT 50''', con=engine)
    st.dataframe(data)