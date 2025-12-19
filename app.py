import streamlit as st
import google.generativeai as genai
import os

# 1. 화면 설정
st.set_page_config(page_title="웅아! 오늘 뭐 해먹지?", page_icon="🥘")

# 2. 제목과 디자인
st.title("🥘 웅아! 오늘 뭐 해먹지?")
st.markdown("### Legendary AI Master Chef")
st.info("냉장고에 있는 재료를 알려주세요! (예: 계란, 파, 스팸)")

# 3. API 키 연결
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API 키 설정을 확인해주세요!")

# 4. 채팅 기록 저장소
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 이전 대화 화면에 보여주기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자가 입력했을 때 동작
if prompt := st.chat_input("재료를 입력하세요..."):
    # 내 말 보여주기
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI가 대답하기
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        with st.chat_message("assistant"):
            with st.spinner("요리법을 생각하는 중..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"오류가 났어요: {e}")
