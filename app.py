import pandas as pd
import streamlit as st
import preprocessor as pr
import helper as hp
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('data/athlete_events.csv')
region_df = pd.read_csv('data/noc_regions.csv')

df = pr.preprocess(df, region_df)
st.set_page_config(page_title='Olympics Analysis', page_icon='https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png', 
                  layout="wide")
hide_menu_style = '''
   <style>
      #MainMenu {visibility: hidden; }
      footer {visibility: hidden;}
   </style>
'''
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
   'Select an option',
   ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

def title_medal_tally(title):
   return st.markdown(f'''
   #### {title}
   ''')

if user_menu == 'Medal Tally':
   st.sidebar.title('Medal Tally')
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

   # ========= Participating Nations =========
   nations_overtime = hp.data_overtime(df, 'region')
   fig = px.line(nations_overtime, x='Edition', y='region')
   st.title('Participating Nations Over The Years')
   st.plotly_chart(fig)

   # ========= Events Over The Years =========
   events_overtime = hp.data_overtime(df, 'Event')
   fig = px.line(events_overtime, x='Edition', y='Event')
   st.title('Events Over The Years')
   st.plotly_chart(fig)

   # ========= Athletes Over The Years =========
   athletes_overtime = hp.data_overtime(df, 'Name')
   fig = px.line(athletes_overtime, x='Edition', y='Name')
   st.title('Athletes Over The Years')
   st.plotly_chart(fig)

   # ========= Numbers of Events Over Time (Sport) =========
   st.title('Numbers of Events Over Time (Sport)')
   fig, ax = plt.subplots(figsize=(20,20))
   x = df.drop_duplicates(['Year', 'Sport', 'Event'])
   ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', 
                           values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
   st.pyplot(fig)

   # ========= Most Successfull Athletes =========
   st.title('Most Successfull Athletes')
   sport_list = df['Sport'].unique().tolist()
   sport_list.sort()
   sport_list.insert(0, 'Overall')

   selected_sport = st.selectbox('Select a Sport', sport_list)
   x = hp.most_successful(df, selected_sport)
   st.table(x)

elif user_menu == 'Country-wise Analysis':
   st.title('Country-wise Analysis')

   country_list = df['region'].dropna().unique().tolist()
   country_list.sort()

   st.sidebar.title('Country-wise Analysis')
   selected_country = st.sidebar.selectbox('Select a Country', country_list)

   title_medal_tally(selected_country + ' Medal Tally Over The Years')
   country_df = hp.yearwise_medaltally(df, selected_country)
   fig = px.line(country_df, x='Year', y='Medal')
   st.plotly_chart(fig)

   
   pt = hp.country_event_heatmap(df, selected_country)
   title_medal_tally(selected_country + ' Numbers In The Following Sports')
   try:
      fig, ax = plt.subplots(figsize=(20, 20))
      ax = sns.heatmap(pt, annot=True)
      st.pyplot(fig)
   except Exception:
      st.error(selected_country + ' Has No Identity')

   title_medal_tally('Top 10 Athletes of ' + selected_country)
   topSuccessful_df = hp.most_successful_countrywise(df, selected_country)
   st.table(topSuccessful_df)

else:
   st.title('Athletes Wise Analysis')

   title_medal_tally('Distribution of Age')
   athletes_df = df.drop_duplicates(subset=['Name', 'region'])
   x1 = athletes_df['Age'].dropna()
   x2 = athletes_df[athletes_df['Medal'] == 'Gold']['Age'].dropna()
   x3 = athletes_df[athletes_df['Medal'] == 'Silver']['Age'].dropna()
   x4 = athletes_df[athletes_df['Medal'] == 'Bronze']['Age'].dropna()
   fig = ff.create_distplot([x1, x2, x3, x4], ['Age Distribution', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], 
                   show_hist=False, show_rug=False)
   st.plotly_chart(fig)

   title_medal_tally('Sports (Gold Medalist)')
   x, name = hp.athleteswise_analysis(athletes_df)
   fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
   fig.update_layout(autosize=False, width=850, height=600)
   st.plotly_chart(fig)

   title_medal_tally('Height vs Weight')
   sport_list = df['Sport'].unique().tolist()
   sport_list.sort()
   sport_list.insert(0, 'Overall')

   selected_sport = st.selectbox('Select a Sport', sport_list)
   temp_df = hp.weight_v_height(df, selected_sport)
   fig, ax = plt.subplots()
   ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=50)
   st.pyplot(fig)

   title_medal_tally('Men vs Women Participation Over The Years')
   final = hp.men__v_women(df)
   fig = px.line(final, x='Year', y=['Male', 'Female'])
   st.plotly_chart(fig)