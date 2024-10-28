import streamlit as st
import pandas as pd

# GitHub에서 Excel 파일의 Raw URL
FILE_URL = 'https://raw.githubusercontent.com/HANNAAPPA/suhakyeohang/main/chulcheck1.xlsx'

@st.cache_data
def load_data():
    data = pd.read_excel(FILE_URL)

    # '학급' 열을 문자열로 강제 변환
    data['학급'] = data['학급'].astype(str)
    
    # '학번' 열을 문자열로 강제 변환
    data['학번'] = data['학번'].astype(str)
    
    # 날짜 형식을 한글 요일로 변환
    data['요일'] = pd.to_datetime(data['날짜']).dt.day_name()
    data['요일'] = data['요일'].replace({
        'Monday': '월요일', 
        'Tuesday': '화요일', 
        'Wednesday': '수요일', 
        'Thursday': '목요일', 
        'Friday': '금요일', 
        'Saturday': '토요일', 
        'Sunday': '일요일'
    })
    
    # 날짜에서 시간 제거
    data['날짜'] = pd.to_datetime(data['날짜']).dt.strftime('%Y-%m-%d')  # 날짜 형식으로 변환
    
    return data

# Excel 파일 로드
data = load_data()

# Streamlit 드롭다운 필터 UI
st.title("학생 명단 조회")

# 날짜, 교시, 학급 드롭다운 생성
dates = sorted(data['날짜'].unique()) if '날짜' in data.columns else []
periods = sorted(data['교시'].unique()) if '교시' in data.columns else []
classes = sorted(data['학급'].unique()) if '학급' in data.columns else []

# 1차 드롭다운: 날짜 선택
selected_date = st.selectbox("날짜 선택", dates)

# 선택한 날짜에 해당하는 요일 얻기
selected_weekday = pd.to_datetime(selected_date).day_name()
korean_weekday = {
    'Monday': '월요일', 
    'Tuesday': '화요일', 
    'Wednesday': '수요일', 
    'Thursday': '목요일', 
    'Friday': '금요일', 
    'Saturday': '토요일', 
    'Sunday': '일요일'
}[selected_weekday]

st.write(f"선택한 날짜: {selected_date} ({korean_weekday})")

# 선택한 날짜에 맞는 교시 목록 필터링
filtered_periods = sorted(data[data['날짜'] == selected_date]['교시'].unique())

# 2차 드롭다운: 교시 선택
selected_period = st.selectbox("교시 선택", filtered_periods)

# 선택한 날짜와 교시에 맞는 학급 목록 필터링
filtered_classes = sorted(data[(data['날짜'] == selected_date) & (data['교시'] == selected_period)]['학급'].unique())
selected_class = st.selectbox("학급 선택", filtered_classes)

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

    # 데이터프레임을 Streamlit에 표시
    st.dataframe(filtered_data, use_container_width=True)  # 인덱스 숨기기
else:
    st.write("해당 조건에 맞는 학생이 없습니다.")
