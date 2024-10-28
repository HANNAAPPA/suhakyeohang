import streamlit as st
import pandas as pd

# GitHub에서 Excel 파일의 Raw URL
FILE_URL = 'https://raw.githubusercontent.com/HANNAAPPA/suhakyeohang/main/chulcheck.xlsx'

@st.cache_data
def load_data():
    data = pd.read_excel(FILE_URL)
    # 모든 열을 문자열로 변환
    return data.applymap(str)

# Excel 파일 로드
data = load_data()

# Streamlit 드롭다운 필터 UI
st.title("학생 명단 조회")

# 날짜, 교시, 학급 드롭다운 생성
dates = sorted(data['날짜'].unique())
periods = sorted(data['교시'].unique())
classes = sorted(data['학급'].unique())

selected_date = st.selectbox("날짜 선택", dates)
selected_period = st.selectbox("교시 선택", periods)
selected_class = st.selectbox("학급 선택", classes)

# 선택한 필터에 맞는 데이터 필터링
filtered_data = data[(data['날짜'] == selected_date) & 
                     (data['교시'] == selected_period) & 
                     (data['학급'] == selected_class)]

# 결과 출력
st.subheader("학생 명단")
for _, row in filtered_data.iterrows():
    st.write(f"{row['학번']} - {row['이름']}")
