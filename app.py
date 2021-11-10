import pandas as pd
import streamlit as st
import preprocessor as pr
import helper as hp

df = pd.read_csv('data/athlete_events.csv')
region_df = pd.read_csv('data/noc_regions.csv')

df = pr.preprocess(df, region_df)
st.set_page_config(layout='wide')
st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
   'Select an option',
   ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':
   st.header('Medal Tally')
   years, country = hp.country_year_list(df)
   select_year = st.sidebar.selectbox('Select Year', years)
   select_country = st.sidebar.selectbox('Select Country', country)
   medal_tally = hp.medal_tally(df)
   st.dataframe(medal_tally)

