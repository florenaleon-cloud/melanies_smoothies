import streamlit as st
from snowflake.snowpark.functions import col

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()   # ← ESTO ERA EL ERROR

st.title("🥤 Example Streamlit App")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")

fruit_df = (
    session
    .table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
    .collect()
)

fruit_options = [row.FRUIT_NAME for row in fruit_df]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
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
