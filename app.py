import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 1. Загружаем переменные из .env
load_dotenv()

# 2. Получаем ключ Groq из системы
groq_api_key = os.getenv("GROQ_API_KEY")

# 3. Инициализируем клиент OpenAI, но направляем его на бесплатный сервер Groq!
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key,
)

# 4. Интерфейс Streamlit
st.title("🎓 AI Study Planner")
st.write("Создай персональный план подготовки к экзамену за пару секунд!")

subject = st.text_input("Какой предмет сдаешь?", placeholder="Например: Web Programming")
days = st.slider("Сколько дней осталось до экзамена?", min_value=1, max_value=30, value=7)
level = st.selectbox("Твой текущий уровень:", ["Beginner (С нуля)", "Intermediate (Знаю базу)", "Advanced (Нужно повторить)"])

# 5. Логика генерации
if st.button("Сгенерировать план"):
    if not subject:
        st.warning("Пожалуйста, введи название предмета!")
    elif not groq_api_key or "gsk_" not in groq_api_key:
        st.error("Ошибка: API-ключ Groq не найден или введен неверно в файле .env!")
    else:
        with st.spinner("AI мгновенно анализирует программу и составляет план..."):
            try:
                system_prompt = "Ты — опытный тьютор и эксперт по подготовке к экзаменам. Твоя задача — составлять четкие, структурированные и реалистичные учебные планы на русском языке."
                user_prompt = f"Составь план подготовки к экзамену по предмету '{subject}' на {days} дней. Мой уровень: {level}. Разбей план по дням, укажи ключевые темы и дай 2-3 практических совета."

                # Делаем запрос к бесплатной быстрой модели Llama 3
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7
                )

                study_plan = response.choices[0].message.content

                st.success("Твой план готов!")
                st.markdown(study_plan)

            except Exception as e:
                st.error(f"Произошла ошибка при обращении к AI: {e}")