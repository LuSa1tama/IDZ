import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Прогноз цены недвижимости", layout="centered")
st.title("🏠 Прогнозирование цены недвижимости")
st.markdown("### Введите параметры квартиры")

col1, col2 = st.columns(2)

with col1:
    площадь = st.number_input("Площадь (м²)", min_value=20.0, max_value=500.0, value=65.0)
    комнаты = st.number_input("Количество комнат", min_value=1, max_value=10, value=2)

with col2:
    расстояние = st.number_input("Расстояние до центра (км)", min_value=0.0, max_value=50.0, value=8.5)
    инфраструктура = st.number_input("Инфраструктура (балл 1-10)", min_value=1, max_value=10, value=7)

район = st.selectbox("Район", ["Западный", "Северный", "Центральный", "Южный"])

# Загрузка модели
@st.cache_resource
def load_model():
    try:
        with open('best_model.pkl', 'rb') as f:
            model = pickle.load(f)
        st.success("Модель загружена: " + str(type(model).__name__))
        return model
    except Exception as e:
        st.error(f"Ошибка загрузки модели: {e}")
        return None

model = load_model()

if st.button("🔮 Рассчитать цену", type="primary"):
    if model is None:
        st.stop()
    
    input_data = pd.DataFrame({
        'Площадь': [площадь],
        'Комнаты': [комнаты],
        'РасстояниеДоЦентраКм': [расстояние],
        'Инфраструктура': [инфраструктура],
        'Район_Западный': [1 if район == "Западный" else 0],
        'Район_Северный': [1 if район == "Северный" else 0],
        'Район_Центральный': [1 if район == "Центральный" else 0],
        'Район_Южный': [1 if район == "Южный" else 0]
    })
    
    prediction = model.predict(input_data)[0]
    st.success(f"**Предсказанная цена: {prediction:,.0f} рублей**")