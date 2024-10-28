import streamlit as st
import pandas as pd

# GitHub에서 Excel 파일의 Raw URL
FILE_URL = 'https://raw.githubusercontent.com/HANNAAPPA/suhakyeohang/main/chulcheck.xlsx'

@st.cache_data
def load_data():
    data = pd.read_excel(FILE_URL)
    
    # '학급' 열을 문자열로 강제 변환
    data['학급'] = data['학급'].astype(str)
    
    return data.applymap(str)

# Excel 파일 로드
data = load_data()

# Streamlit 드롭다운 필터 UI
st.title("학생 명단 조회")

# 날짜, 교시, 학급 드롭다운 생성
dates = sorted(data['날짜'].unique()) if '날짜' in data.columns else []
periods = sorted(data['교시'].unique()) if '교시' in data.columns else []
classes = sorted(data['학급'].unique()) if '학급' in data.columns else []

selected_date = st.selectbox("날짜 선택", dates)
selected_period = st.selectbox("교시 선택", periods)
selected_class = st.selectbox("학급 선택", classes)

# 선택한 필터에 맞는 데이터 필터링
filtered_data = data[(data['날짜'] == selected_date) & 
                     (data['교시'] == selected_period) & 
                     (data['학급'] == selected_class)]

# 결과 출력
st.subheader("학생 명단")
if not filtered_data.empty:
    # 연번 추가
    filtered_data.reset_index(drop=True, inplace=True)
    filtered_data['연번'] = filtered_data.index + 1  # 인원수 추가
    filtered_data = filtered_data[['연번', '학번', '이름']]  # 필요한 열만 선택

    st.table(filtered_data)  # 표 형식으로 출력
else:
    st.write("해당 조건에 맞는 학생이 없습니다.")
