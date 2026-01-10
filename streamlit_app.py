import streamlit as st
from snowflake.snowpark.functions import col

# Snowflake connection (Streamlit Cloud)
cnx = st.connection("snowflake")
session = cnx.session()

st.title("🥤 Example Streamlit App")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")

fruit_df = session.sql(
    "SELECT FRUIT_NAME FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
).to_pandas()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_df["FRUIT_NAME"].tolist(),
    max_selections=5
)

if st.button("Submit Order") and ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    session.sql(
        f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
        """
    ).collect()

    st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
