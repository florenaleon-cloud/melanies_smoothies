import streamlit as st

st.title("Snowflake test")

cnx = st.connection("snowflake")
session = cnx.session

result = session.sql("SELECT CURRENT_USER(), CURRENT_ROLE()").collect()
st.write(result)
