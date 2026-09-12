import streamlit as st

st.title("Моё первое приложение")
st.write("Привет! Это тестовое приложение на Streamlit.")

name = st.text_input("Введите ваше имя:")
if name:
    st.success(f"Здравствуйте, {name}!")
