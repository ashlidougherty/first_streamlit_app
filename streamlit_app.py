import streamlit as st
import pandas as pd




st.title("My Parents New Healthy Diner")
st.header("Breakfast Favorites")
st.text("🫐Omega 3 & Blueberry Oatmeal")
st.text("Kale, Spinach & Rocket Smoothie")
st.text("🐣Hard-boiled Free-Range Egg")
st.text("🥑Avocado Toast")

st.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

st.dataframe(fruits_to_show)

#new section to displayfruityvice api response
st.header('Fruityvice Fruit Advice')

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
#st.text(fruityvice_response.json())

#normalizes the json response
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#then turns it into a dataframe
st.dataframe(fruityvice_normalized)
