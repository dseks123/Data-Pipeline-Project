
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
#sns.set_style('white_grid')

@st.cache()
def fetch_data():
    engine = create_engine('postgres://dennisssekamaanya:dennis123@localhost:5432/dennisssekamaanya')
    return pd.read_sql_query('SELECT * FROM "flight_data"', con = engine)

flightdf = fetch_data()

st.write('''
# Welcome to Streamlit!
We shall use this app to expore and analyze our flight dataset
''')


#GENERAL SAMPLE STATS
col1, col2 = st.beta_columns(2)
col1.header('Sample Stats by Airline')
butt1 = col1.button('10 Worst Airport Performers')

if butt1: 
    data1 = flightdf.groupby('airline').mean().reset_index().sort_values(by='departure_delay', ascending = False)[['departure_delay','air_system_delay', 'security_delay', 'airline_delay', 'late_aircraft_delay', 'weather_delay']].head(10)  
    fig1, ax1 = plt.subplots(figsize=(15,8))
    ax1.plot(x = 'airline', y = 'departure_delay', data = data1)
    ax1.plot(x = 'airline', y = 'air_system_delay', data = data1)
    ax1.plot(x = 'airline', y = 'security_delay', data = data1)
    ax1.plot(x = 'airline', y = 'airline_delay', data = data1)
    ax1.plot(x = 'airline', y = 'late_aircraft_delay', data = data1)
    ax1.plot(x = 'airline', y = 'weather_delay', data = data1)
    plt.grid()
    ax1.legend(['Departure Delay', 'Air-System Delay', 'Security Delay', 'Airline Delay', 'Late Aircraft Delay', 'Weather Delay'], loc = 0)
    ax1.set_xlabel('AIRLINES')
    ax1.set_ylabel('MEAN DEPARTURE DELAY(MIN)')
    st.pyplot(fig1)
    #st.beta_set_page_config(layout="wide")


col2.header('Sample Stats by Airport')
butt2 = col2.button('10 Worst Airline Performers')
if butt2:
    data2 = flightdf.groupby('departure_delay').mean().reset_index().sort_values(by='departure_delay', ascending = False)[['taxi_out', 'air_system_delay', 'security_delay', 'airline_delay', 'late_aircraft_delay', 'weather_delay']].head(10)    
    st.dataframe(data2)

    sns.set_style('darkgrid')
    fig2, ax2 = plt.subplots(figsize = (15,8))
    w = 0.2
    g1 = np.arange(len(data2['origin_airport']))
    g2 = [i+w for i in g1]
    g3 = [i+w for i in g2]
    g4 = [i+w for i in g3]
    g5 = [i+w for i in g4] 
    g6 = [i+w for i in g5]
    g7 = [i+w for i in g6]
    g1 = ax2.bar('origin_airport','mean_depdelay', w, data = data2)
    g2 = ax2.bar(g2, 'mean_taxiout', w, data = data2)
    g3 = ax2.bar(g3, 'airsys_delay', w, data = data2)
    g4 = ax2.bar(g4, 'security_delay', w, data = data2)
    #g5 = ax2.bar(g5, 'airline_delay', w, data = data2)
    #g6 = ax2.bar(g6, 'aircraft_delay', w, data = data2)
    #g7 = ax2.bar(g7, 'weather_delay',w,data = data2)
    #plt.grid()
    ax2.legend(['Mean Departure Delay', 'Mean Taxi-Out', 'Air-System Delay', 'Security Delay', 'Airline Delay', 
    'Late Aircraft Delay', 'Weather Delay'], loc = 0)
    ax2.set_xlabel('DEPARTURE AIRPORT')
    ax2.set_ylabel('MEAN AIRPORT DELAY(MIN)')
    ax2.set_xticklabels(data2['origin_airport'], rotation=90)
    fig2.tight_layout()
    st.pyplot(fig2)

#DIRECT QUERY INPUTś

#1. DEPARTURE DELAY BY AIRPORT
col1a, col1b = st.beta_columns(2)
expander1 = col1a.beta_expander('Departure Delay by Airport')
airport_from = expander1.selectbox('Select Airport', ["-Select An Airport-"]+list(flightdf['origin_name'].unique()))
expander1a = col1b.beta_expander('Analyze By:')
to_analyze_by = expander1a.multiselect('Select stats', ('airline', 'month','taxi_out', 'departure_delay', 'air_system_delay', 'security_delay', 'airline_delay', 'late_aircraft_delay', 'weather_delay'))

butt3 = expander1a.button('Click To Show Graph')
if butt3:
    airport_Dep_stats = flightdf[flightdf['origin_name'] == '{}'.format(airport_from)]
    #st.dataframe(airport_Dep_stats.head(5))
    airport_Dep_stats1 = airport_Dep_stats.groupby(to_analyze_by[:1]).mean().reset_index()[to_analyze_by]
    #st.dataframe(airport_Dep_stats1.head(5))
    #PLOT A GRAPH OF THE AIRLINE DELAY AT THE SELECTED AIRPORT
    cols = to_analyze_by[1:]
    col_num = len(cols)
    figd, axd = plt.subplots()
    for item in cols:
        axd.plot(to_analyze_by[0], item, data = airport_Dep_stats1)

    axd.legend(cols)
    axd.set_xlabel(str(to_analyze_by[:1]).upper())
    axd.set_ylabel('MINUTES')
    axd.set_title('MEAN FLIGHT-DELAY AT {}'.format(airport_from))
    st.pyplot(figd)
    


#2. ARRIVAL DELAY BY AIRPORT

col2a, col2b = st.beta_columns(2)
expander2 = col2a.beta_expander('Arrival Delay by Airport')
airport_to = expander2.multiselect('Select Airport', ['-Select An Airport-']+list(flightdf['dest_name'].unique()))
expander2b = col2b.beta_expander('Analyze By:')
airport_to_stats = expander2b.multiselect('Select Stats',('taxi_out', 'departure_delay', 'arrival_delay', 'taxi_in', 'air_system_delay', 'security_delay', 'airline_delay', 'late_aircraft_delay', 'weather_delay'))

#butt2a = expander2b.button('Show Graph')
#3. ROUTE ANALYSIS

col3a, col3b, col3c = st.beta_columns(3)
expander3a = col3a.beta_expander('By Route')
carr_select = expander3a.selectbox('Choose Airline', ['-Select Airport-']+list(flightdf.airline.unique()))
expander3b = col3b.beta_expander('Departure Airport')
flying_from = expander3b.selectbox('From: Select Airport', ['-Select Airport-']+ list(flightdf[flightdf.airline == '{}'.format(carr_select)]['origin_name'].unique()))
#flying_from = expander3b.selectbox('From: Select Airport', pd.read_sql_query("SELECT DISTINCT(origin_airport) FROM flight_data WHERE airline = '%s'" %carr_select))
expander3c = col3c.beta_expander('Destination Airport')
flying_to = expander3c.selectbox('To: Select Airport', flightdf[(flightdf.airline == '{}'.format(carr_select)) & (flightdf['origin_name'] == '{}'.format(flying_from))]['dest_name'].unique())
#flying_to = expander3c.selectbox('To: Select Airport', pd.read_sql_query("SELECT DISTINCT(destination_airport) FROM flight_data WHERE airline = '%s' AND origin_airport = '%s'" %(carr_select,flying_from), con = engine))

#butt3c = expander3c.button('Show Graph')





    

    