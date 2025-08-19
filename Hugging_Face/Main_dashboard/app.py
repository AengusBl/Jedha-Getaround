import streamlit as st

st.set_page_config(
    page_title="Getaround Project",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
  )

late_returns_page = st.Page("late_returns.py", title="Analysis Dashboard", icon=":material/car_rental:")
price_api_docs = st.Page("docs.py", title="Try it out!", icon=":material/api:")
price_api_mlflow = st.Page("price_api_mlflow.py", title="MLFlow Tracking Server", icon=":material/model_training:")

pg = st.navigation({
    "Late Returns": [late_returns_page],
    "The Pricing API": [price_api_docs, price_api_mlflow]
})
pg.run()