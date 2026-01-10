import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title("🥤 Melanie's Smoothies")

session = get_active_session()

fruit_df = session.table("FRUIT_OPTIONS").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in fruit_df.collect()]

ingredients = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

name_on_order = st.text_input("Name on Smoothie:")

if st.button("Submit Order") and ingredients:
    ingredients_string = " ".join(ingredients)

    session.sql(
        f"""
        INSERT INTO ORDERS (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
        """
    ).collect()

    st.success(f"Your Smoothie is ordered, {name_on_order}! ✅")
