# Import Liabrary
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
import io
import requests
from bs4 import BeautifulSoup
import xlsxwriter

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

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
st.header("GPA Calculator")
#st.text('Enter the Semester to Calculate Your GPA')

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
    gpa_dict = {'A+': 4.3, 'A0': 4.0, 'A-': 3.7, 'B+': 3.3, 'B0': 3.0, 'B-': 2.7, 'C+': 2.3, 'C0': 2.0, 'C-': 1.7, 'D+': 1.3, 'D0': 1.0, 'D-': 0.7, 'F': 0}

    sem_list = []
    temp = []

    gpa_table = {}

    for index, index2 in zip(df['학기'], df['평가']):
        #st.write(temp)
        #st.write(gpa_table)
        if index not in sem_list:
            if '0학기' in index:
                continue
            if not sem_list:
                sem_list.append(index)
                if index2 == 'P' or index2 == 'NP':
                    continue
                else:
                    temp.append(index2)
            else:
                gpa_table.update({sem_list[-1]: temp.copy()})
                sem_list.append(index)
                temp.clear()
                if index2 not in list(gpa_dict.keys()):
                    continue
                else:
                    temp.append(index2)
        else:
            if index2 not in list(gpa_dict.keys()):
                continue
            else:
                temp.append(index2)
    gpa_table.update({sem_list.pop(): temp})
    
    #st.write(gpa_table)

    sem_list = []
    
    for index in gpa_table.keys():
        sem_list.append(index)
    sem_list.append('Cumulative')
    
    option = st.selectbox('Select a semester to calculate GPA', tuple(sem_list))

    chart = {}
    chart_index = []
    chart_count = []

    gpa = 0
    counter = 0

    if option == 'Cumulative':
        for index in gpa_table.keys():
            for index2 in gpa_table.get(index):
                counter += 1
                gpa += gpa_dict.get(index2)
                if index2 not in chart_index:
                    chart_index.append(index2)
                    chart_count.append(1)
                else:
                    chart_count[chart_index.index(index2)] += 1
        st.write(option, "GPA:", round(gpa / counter, 2))
        
    else:
        for index in gpa_table.get(option):
            gpa += gpa_dict.get(index)
            if index not in chart_index:
                chart_index.append(index)
                chart_count.append(1)
            else:
                chart_count[chart_index.index(index)] += 1
        st.write(option, "GPA:", round(gpa / len(list(gpa_table.get(option))), 2))
    
    chart_final = {'Index': chart_index, 'Count': chart_count}
    ans = pd.DataFrame(chart_final)
    ans = ans.set_index('Index')
    st.bar_chart(ans)
            
            
            
            
            

