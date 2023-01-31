import streamlit as st
import pandas as pd
import snowflake.connector
import requests
from urllib.error import URLError

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

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +  this_fruit_choice)
   fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

#new section to displayfruityvice api response
st.header('Fruityvice Fruit Advice')
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    st.dataframe(back_from_function)
  
except URLError as e:
  st.error()
 

st.header('The fruit load list contains:')
#snowflake related stuff
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from fruit_load_list")
      return my_cur.fetchall()
   
#add a button to get fruit
if st.button('Get fruit load list'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   my_cnx.close()
   st.dataframe(my_data_rows)

#adding second box
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
      return "Thanks for adding " + new_fruit

add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add fruit to the list'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   st.text(back_from_function)

   
