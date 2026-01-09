import streamlit as st

st.title("Snowflake test")

cnx = st.connection("snowflake")
session = cnx.session

st.success("Connected!")

st.write(
    session.sql("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_DATABASE()").collect()
)
