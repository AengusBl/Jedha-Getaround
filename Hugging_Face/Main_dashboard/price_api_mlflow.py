import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(
    page_title="Getaround Project",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
  )

components.iframe(os.environ["MLFLOW_TRACKING_SERVER_URL"], height=1500)
