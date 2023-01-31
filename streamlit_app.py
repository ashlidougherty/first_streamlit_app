import streamlit as st
import pandas as pd
import snowflake.connector
import requests

#setting up menu

st.title("My Parents New Healthy Diner")
st.header("Breakfast Favorites")
st.text("🫐Omega 3 & Blueberry Oatmeal")
st.text("Kale, Spinach & Rocket Smoothie")
st.text("🐣Hard-boiled Free-Range Egg")
st.text("🥑Avocado Toast")

st.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")

#adding smoothie ingredients as a df
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

st.dataframe(fruits_to_show)

#new section to displayfruityvice api response
st.header('Fruityvice Fruit Advice')
fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +  fruit_choice)
#st.text(fruityvice_response.json())

#normalizes the json response
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#then turns it into a dataframe
st.dataframe(fruityvice_normalized)

#connecting to snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("Fruit load list contains:")
st.dataframe(my_data_rows)

#adding second box
add_my_fruit = st.text_input('What fruit would you like to add?')
st.write('Thanks for adding ', add_my_fruit)

#this will not work correctly but go with it
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
