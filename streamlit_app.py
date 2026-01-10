st.write(
    session.sql(
        "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_DATABASE()"
    ).collect()
)
