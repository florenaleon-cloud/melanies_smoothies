import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Crear sesión usando los secretos de la app (connections.snowflake)
session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Título y descripción
st.title(f":cup_with_straw: Example Streamlit App :cup_with_straw: {st.__version__}")
st.write("Choose the fruits you want in your custom Smoothie!")

# Nombre en el pedido
name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be: ", name_on_order)

# Obtener opciones de frutas desde Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    [row['FRUIT_NAME'] for row in my_dataframe.collect()],
    max_selections=5
)

# Construir la cadena de ingredientes
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = (
        "insert into smoothies.public.orders(ingredients,name_on_order) "
        "values ('" + ingredients_string + "','" + name_on_order + "')"
    )

    st.write(my_insert_stmt)

# Botón para enviar pedido
time_to_insert = st.button('Submit Order')

if time_to_insert:
    if ingredients_list and name_on_order:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order+'!', icon="✅")
    else:
        st.error("Please enter your name and select at least one ingredient!")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon") 
st.text(smoothiefroot_response)
