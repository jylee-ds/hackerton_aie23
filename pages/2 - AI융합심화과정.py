# Import Liabrary
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
import io
import requests
from bs4 import BeautifulSoup
import xlsxwriter

# Collection of def
def find_info(df):
    not_nan = []
    info = {}

    for i in df.values:
        for j in i:
            if str(j) != 'nan':
                not_nan.append(j)

    for i in range(0, len(not_nan), 2):
        info[not_nan[i]] = not_nan[i + 1]

    return info

# Main Interface
st.header("응용정보공학 AI융합심화전공 졸업 조건 확인")
st.text("응용정보공학 단일전공 이수 기준")

st.markdown("""
<style>
img {
    max-height: 300px;
}

.streamlit-expenderContent div {
    display: flex;
    justify-content: center;
    font-size: 20px:
}

[data-testid="stExpanderToggleIcon"] {
    visibility: hidden;
}

[class="st-emotion-cache-p5msec eqpbllx2"] {
    pointer-events: none;
}

[data-testid='StyledFullScreenButton'] {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

data = st.sidebar.file_uploader("Upload Excel File Here")

if data:
    st.divider()
    st.text('Your Grades')

    wb = openpyxl.load_workbook(data)
    sheet_selector = st.sidebar.selectbox("Select Sheet:", wb.sheetnames)

    # DataFrame of grade
    df_grade = pd.read_excel(data, sheet_selector, header=4)
    columns_need = ['학기', '교과목명', '과목 종별', '학점', '평가', '학정번호']
    df = df_grade[columns_need]
    df = df.fillna(method='ffill')
    df['학기'] = df['학기'].str.replace(' ', '')

    st.dataframe(df, width=1000)

    # Additional Information
    major_list = []
    for i in df['학정번호'].values:
        if 'GAI' in i:
            major_list.append('응정')
        elif 'GKE' in i:
            major_list.append('한교')
        elif 'GBL' in i:
            major_list.append('바생')
        elif 'GCM' in i:
            major_list.append('문미')
        elif 'GIC' in i:
            major_list.append('국통')
        else:
            major_list.append('extra')

    major_34_list = []
    for i in df['학정번호'].values:
        if i[3] == '3' or i[3] == '4':
            major_34_list.append('YES')
        else:
            major_34_list.append('NO')

    df['전공'] = major_list
    df['3000&4000'] = major_34_list

    # DataFrame of Personal Info
    df_name = pd.read_excel(data, sheet_selector)
    df_name = df_name.head(2)
    info_dict = find_info(df_name)
    text = ''

    for key, values in info_dict.items():
        text += f'  {key} :  {values}  /'

    st.divider()
    st.markdown('__Your Info__')
    st.write(text)

    st.divider()
    AIC = 9
    major_base = 18
    major_req = 9
    major_optional = 24
    GAI3006 = 3

    for index, index2 in zip(df['학정번호'], df['과목 종별']):
        if AIC >= 3 and 'AIC' in index:
            AIC -= 3
            continue
        if index == 'GAI3006':
            GAI3006 -= 3
            continue
        if 'GAI' in index:
            if index2 == '전기' and major_base >= 3:
                major_base -= 3
                continue
            if index2 == '전필' and major_req >= 3:
                major_req -= 3
                continue
            if index2 == '전선' and major_optional >= 3:
                major_optional -= 3
                continue

    complete = []
    needed = []

    st.write('응용정보공학 AI융합심화전공 졸업 하려면 다음 조건들을 만족해야 합니다:')
    st.write('AI 코어과목:', AIC, '학점')
    st.write('1전공 AI 융합심화전공(GAI3006):', GAI3006, '학점')
    st.write('응용정보공학 전기:', major_base, '학점')
    st.write('응용정보공학 전필:', major_req, '학점')
    st.write('응용정보공학 전선:', major_optional, '학점')
    
    chart = {'Index': ['AI 코어과목', '1전공 AI 융합심화전공(GAI3006)', '전기', '전필', '전선'], '이수학점': [9 - AIC, 3 - GAI3006, 18 - major_base, 9 - major_req, 24 - major_optional],
             '필요학점': [AIC, GAI3006, major_base, major_req, major_optional]}
    chart_final = pd.DataFrame(chart)
    chart_final = chart_final.set_index('Index')
    st.bar_chart(chart_final)
    
