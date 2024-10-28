import streamlit as st
import pandas as pd

# GitHub에서 Excel 파일의 Raw URL
FILE_URL = 'https://raw.githubusercontent.com/username/repo_name/main/교육여행분반.xlsx'

# Excel 파일 로드
data = pd.read_excel(FILE_URL)

# Streamlit 드롭다운 필터 UI 및 필터링 로직 (이전 코드와 동일)
st.title("학생 명단 조회")

dates = sorted(data['날짜'].unique())
periods = sorted(data['교시'].unique())
classes = sorted(data['학급'].unique())

selected_date = st.selectbox("날짜 선택", dates)
selected_period = st.selectbox("교시 선택", periods)
selected_class = st.selectbox("학급 선택", classes)

filtered_data = data[(data['날짜'] == selected_date) & 
                     (data['교시'] == selected_period) & 
                     (data['학급'] == selected_class)]

st.subheader("학생 명단")
for _, row in filtered_data.iterrows():
    st.write(f"{row['학번']} - {row['이름']}")
