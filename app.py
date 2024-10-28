import streamlit as st
import pandas as pd

# GitHub에서 Excel 파일의 Raw URL
FILE_URL = 'https://raw.githubusercontent.com/HANNAAPPA/suhakyeohang/main/chulcheck.xlsx'

@st.cache_data
def load_data():
    data = pd.read_excel(FILE_URL)

    # '학급' 열을 문자열로 강제 변환
    data['학급'] = data['학급'].astype(str)
    
    # 날짜 형식을 요일로 변환
    data['요일'] = pd.to_datetime(data['날짜']).dt.day_name()
    
    return data.applymap(str)

# Excel 파일 로드
data = load_data()

# Streamlit 드롭다운 필터 UI
st.title("학생 명단 조회")

# 날짜, 교시, 학급 드롭다운 생성
dates = sorted(data['요일'].unique()) if '요일' in data.columns else []
periods = sorted(data['교시'].unique()) if '교시' in data.columns else []
classes = sorted(data['학급'].unique()) if '학급' in data.columns else []

# 1차 드롭다운: 요일 선택
selected_date = st.selectbox("요일 선택", dates)

# 선택한 요일에 맞는 교시 목록 필터링
filtered_periods = sorted(data[data['요일'] == selected_date]['교시'].unique())
selected_period = st.selectbox("교시 선택", filtered_periods)

# 선택한 요일과 교시에 맞는 학급 목록 필터링
filtered_classes = sorted(data[(data['요일'] == selected_date) & (data['교시'] == selected_period)]['학급'].unique())
selected_class = st.selectbox("학급 선택", filtered_classes)

# 선택한 필터에 맞는 데이터 필터링
filtered_data = data[(data['요일'] == selected_date) & 
                     (data['교시'] == selected_period) & 
                     (data['학급'] == selected_class)]

# 결과 출력
st.subheader("학생 명단")
if not filtered_data.empty:
    # 연번 추가
    filtered_data.reset_index(drop=True, inplace=True)
    filtered_data['연번'] = filtered_data.index + 1  # 인원수 추가
    filtered_data = filtered_data[['연번', '학번', '이름']]  # 필요한 열만 선택

    # 인덱스 없이 표 형식으로 출력
    st.table(filtered_data.style.hide_index())  # 인덱스 숨기기
else:
    st.write("해당 조건에 맞는 학생이 없습니다.")
