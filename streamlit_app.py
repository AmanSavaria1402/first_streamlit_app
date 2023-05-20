import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.title('Breakfast Favourites')

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

# helper functions
def get_fruityvice_data(this_fruit_choice):
    # getting api call for fruit
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
    # normalizing the json using pandas to create a dataframe
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# new section to display the fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        fruityvice_normalized = get_fruityvice_data(fruit_choice)
        # displaying it as a dataframe
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()
# dont run anything past this till we troubleshoot

streamlit.header("The fruite load list contains:")
# snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list;")
        return my_cur.fetchall()

# add a button to load the fruit
if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)


streamlit.stop()
listFruitChoice = streamlit.text_input("What fruit would you like to add?", 'Jackfruit')
streamlit.text(f'Thanks for adding {listFruitChoice}')

my_cur.execute("Insert into fruit_load_list values ('from streamlit');")