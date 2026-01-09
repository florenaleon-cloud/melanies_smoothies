import streamlit as st

st.title("Snowflake connection test")

cnx = st.connection("snowflake")

st.success("Connected to Snowflake 🎉")

df = cnx.query(
    "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_DATABASE()",
    ttl=0
)

st.dataframe(df)
