import pandas as pd
import streamlit as st
import preprocessor as pr
import helper as hp
import plotly.express as px

df = pd.read_csv('data/athlete_events.csv')
region_df = pd.read_csv('data/noc_regions.csv')

df = pr.preprocess(df, region_df)
st.set_page_config(layout='wide')
st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
   'Select an option',
   ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

def title_medal_tally(title):
   return st.markdown(f'''
   #### {title}
   ''')

if user_menu == 'Medal Tally':
   st.title('Medal Tally')
   years, country = hp.country_year_list(df)
   
   selected_year = st.sidebar.selectbox('Select Year', years)
   selected_country = st.sidebar.selectbox('Select Country', country)

   medal_tally = hp.fetch_medal_tally(df, selected_year, selected_country)

   if selected_year == 'Overall' and selected_country == 'Overall':
      title_medal_tally('Overall Tally')
   elif selected_year != 'Overall' and selected_country == 'Overall':
      title_medal_tally('Medal Tally in ' + str(selected_year) + ' Olympics')
   elif selected_year == 'Overall' and selected_country != 'Overall':
      title_medal_tally(str(selected_country) + ' Overall Performance')
   else:
      title_medal_tally(selected_country + ' Performance in ' + str(selected_year) + ' Olympics')
   st.table(medal_tally)

elif user_menu == 'Overall Analysis':
   st.title('Top Statistics')
   editions = df['Year'].unique().shape[0]
   cities = df['City'].unique().shape[0]
   sports = df['Sport'].unique().shape[0]
   events = df['Event'].unique().shape[0]
   athletes = df['Name'].unique().shape[0]
   nations = df['region'].unique().shape[0]

   col1, col2, col3 = st.columns(3)
   with col1:
      title_medal_tally('Editions')
      st.header(editions)
   with col2:
      title_medal_tally('Hosts')
      st.header(cities)
   with col3:
      title_medal_tally('Sports')
      st.header(sports)

   col1, col2, col3 = st.columns(3)
   with col1:
      title_medal_tally('Events')
      st.header(events)
   with col2:
      title_medal_tally('Nations')
      st.header(nations)
   with col3:
      title_medal_tally('Atheletes')
      st.header(athletes)

   nations_overtime = hp.data_overtime(df, 'region')
   fig = px.line(nations_overtime, x='Edition', y='region')
   st.title('Participating Nations Over The Years')
   st.plotly_chart(fig)

   events_overtime = hp.data_overtime(df, 'Event')
   fig = px.line(events_overtime, x='Edition', y='Event')
   st.title('Events Over The Years')
   st.plotly_chart(fig)

