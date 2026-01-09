# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Example Streamlit App :cup_with_straw: {st.__version__}")

st.write("Choose the fruits you want in your custom Smoothie!")

# ✅ Snowflake session for Streamlit Cloud
cnx = st.connection("snowflake")
session = cnx.session

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

fruit_df = (
    session
    .table("smoothies.public.fruit_options")
    .select(col('FRUIT_NAME'))
    .collect()
)

fruit_options = [row.FRUIT_NAME for row in fruit_df]

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,
    max_selections=5
)

my_insert_stmt = None

if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    my_insert_stmt = (
        "INSERT INTO smoothies.public.orders (ingredients, name_on_order) "
        f"VALUES ('{ingredients_string}', '{name_on_order}')"
    )

    st.write(my_insert_stmt)

time_to_insert = st.button('Submit Order')

if time_to_insert:
    if not name_on_order:
        st.warning("Please enter a name for your Smoothie 🙏")
    elif not ingredients_list:
        st.warning("Please choose at least one ingredient 🍓")
    else:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
