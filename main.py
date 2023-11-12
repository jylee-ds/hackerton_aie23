# Import Liabrary
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
import io
import os
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.font_manager as fm

# Basic Setting
st.set_page_config(page_title="GPVC", page_icon="📑")

fm.fontManager.addfont('NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf')
fm._load_fontmanager(try_read_cache=False)
    
plt.rc('font', family='NanumGothic')

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

def major_points_by_types(major):
    major_credits = {}
    if major == '응용정보공학전공':
        major_abr = '응정'
    elif major == '국제통상전공':
        major_abr = '국통'
    elif major == '문화미디어전공':
        major_abr = '문미'
    elif major == '바이오생활공학전공':
        major_abr = '바생'
    elif major == '한국어문화교육전공':
        major_abr = '한교'

    major_basic = df[(df['전공'] == major_abr) & (df['과목 종별'] == '전기')]['학점'].sum()
    major_select = df[(df['전공'] == major_abr) & (df['과목 종별'] == '전선')]['학점'].sum()
    major_man = df[(df['전공'] == major_abr) & (df['과목 종별'] == '전필')]['학점'].sum()
    major_34 = df[df['3-4000'] == 'YES']['학점'].sum()

    major_credits['major_basic'] = int(major_basic)

    major_credits['major_man'] = int(major_man)
    major_credits['major_select'] = int(major_select)
    major_credits['major_34'] = int(major_34)

    return major_credits

def find_requirements(major_main, major_second):
    if major_second == 'None':
        major_credits = {}

        if major_main =='응용정보공학전공':
            major_credits['major_select'] = 24
            major_credits['major_man'] = 12
            major_credits['major_basic'] = 18
            major_credits['major_34'] = 45

        elif major_main == '국제통상전공':
            major_credits = {}
            major_credits['major_select'] = 42
            major_credits['major_man'] = 0
            major_credits['major_basic'] = 6
            major_credits['major_34'] = 45

        elif major_main == '문화미디어전공':
            major_credits = {}
            major_credits['major_select'] = 42
            major_credits['major_man'] = 0
            major_credits['major_basic'] = 6
            major_credits['major_34'] = 45

        elif major_main == '바이오생활공학전공':
            major_credits = {}
            major_credits['major_select'] = 18
            major_credits['major_man'] = 12
            major_credits['major_basic'] = 24
            major_credits['major_34'] = 45

        elif major_main == '한국어문화교육전공':
            major_credits = {}
            major_credits['major_select'] = 6
            major_credits['major_man'] = 42
            major_credits['major_basic'] = 0
            major_credits['major_34'] = 45

        return major_credits

    else:
        major_credits = {}
        major_credits_second = {}

        # main major
        if major_main =='응용정보공학전공':
            major_credits['major_select'] = 15
            major_credits['major_man'] = 12
            major_credits['major_basic'] = 9
            major_credits['major_34'] = 45

        elif major_main == '국제통상전공':
            major_credits['major_select'] = 30
            major_credits['major_man'] = 0
            major_credits['major_basic'] = 6
            major_credits['major_34'] = 45

        elif major_main == '문화미디어전공':
            major_credits['major_select'] = 42
            major_credits['major_man'] = 0
            major_credits['major_basic'] = 6
            major_credits['major_34'] = 45

        elif major_main == '바이오생활공학전공':
            major_credits['major_select'] = 15
            major_credits['major_man'] = 12
            major_credits['major_basic'] = 9
            major_credits['major_34'] = 45

        elif major_main == '한국어문화교육전공':
            major_credits['major_select'] = 6
            major_credits['major_man'] = 0
            major_credits['major_basic'] = 39
            major_credits['major_34'] = 45

        #second major

        if major_second =='응용정보공학전공':
            major_credits_second['major_basic'] = 9
            major_credits_second['major_man'] = 12
            major_credits_second['major_select'] = 15
            major_credits_second['major_34'] = 0

        elif major_second == '국제통상전공':
            major_credits_second['major_basic'] = 6
            major_credits_second['major_man'] = 0
            major_credits_second['major_select'] = 30
            major_credits_second['major_34'] = 0

        elif major_second == '문화미디어전공':
            major_credits_second['major_basic'] = 6
            major_credits_second['major_man'] = 0
            major_credits_second['major_select'] = 30
            major_credits_second['major_34'] = 0

        elif major_second == '바이오생활공학전공':
            major_credits_second['major_basic'] = 9
            major_credits_second['major_man'] = 12
            major_credits_second['major_select'] = 15
            major_credits_second['major_34'] = 0

        elif major_second == '한국어문화교육전공':
            major_credits_second['major_basic'] = 39
            major_credits_second['major_select'] = 6
            major_credits_second['major_man'] = 0
            major_credits_second['major_34'] = 0

        return major_credits, major_credits_second

def major_by_types(major):
    if major == '응용정보공학전공':
        major_abr = '응정'
    elif major == '국제통상전공':
        major_abr = '국통'
    elif major == '문화미디어전공':
        major_abr = '문미'
    elif major == '바이오생활공학전공':
        major_abr = '바생'
    elif major == '한국어문화교육전공':
        major_abr = '한교'

    return major_abr

def create_blank_df(idx_name, rec_name=None):
    blank_df = pd.DataFrame({'index': idx_name, 'required credits': rec_name, 'current credits': [None], 'remaining credits': [None]})
    return blank_df

def remaining_credits_counts():
    my_list = []

    basic = credits_required['major_basic'] - credits_main['major_basic']
    if basic <= 0:
        basic = 0
    my_list.append(basic)

    man = credits_required['major_man'] - credits_main['major_man']
    if man <= 0:
        man = 0
    my_list.append(man)

    select = credits_required['major_select'] - credits_main['major_select']
    if select <= 0:
        select = 0
    my_list.append(select)

    major_34 = credits_required['major_34'] - credits_main['major_34']
    if major_34 <= 0:
        major_34 = 0
    my_list.append(major_34)

    return my_list

def remaining_credits_counts_main():
    my_list = []

    basic = credits_required_main['major_basic'] - credits_main['major_basic']
    if basic <= 0:
        basic = 0
    my_list.append(basic)

    man = credits_required_main['major_man'] - credits_main['major_man']
    if man <= 0:
        man = 0
    my_list.append(man)

    select = credits_required_main['major_select'] - credits_main['major_select']
    if select <= 0:
        select = 0
    my_list.append(select)

    major_34 = credits_required_main['major_34'] - credits_main['major_34']
    if major_34 <= 0:
        major_34 = 0
    my_list.append(major_34)

    return my_list

def remaining_credits_counts_second():
    my_list = []

    basic = credits_required_second['major_basic'] - credits_second['major_basic']
    if basic <= 0:
        basic = 0
    my_list.append(basic)

    man = credits_required_second['major_man'] - credits_second['major_man']
    if man <= 0:
        man = 0
    my_list.append(man)

    select = credits_required_second['major_select'] - credits_second['major_select']
    if select <= 0:
        select = 0
    my_list.append(select)

    major_34 = credits_required_second['major_34'] - credits_second['major_34']
    if major_34 <= 0:
        major_34 = 0
    my_list.append(major_34)

    return my_list

# Main Interface
st.header("Graduation Requirement Validity Checker")
st.text('Import the file located on the left side of the screen')
st.divider()

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
        elif 'GLC' in i:
            major_list.append('GLC교양')
        else:
            major_list.append('extra')

    major_34_list = []
    for i in df['학정번호'].values:
        if str(i[3]) == '3' or str(i[3]) == '4':
            major_34_list.append('YES')
        else:
            major_34_list.append('NO')

    df['전공'] = major_list
    df['3-4000'] = major_34_list

    # DataFrame of Personal Info
    df_name = pd.read_excel(data, sheet_selector)
    df_name = df_name.head(2)
    info_dict = find_info(df_name)
    text = ''

    for key, values in info_dict.items():
        text += f'  {key} :  {values}  /'

    st.divider()
    st.text('Your Info')
    st.write(text)


    # Credit Remained
    st.divider()
    total_credit = np.sum(df['학점'])

    st.subheader('Select Your Major')
    col1, col2 = st.columns(2)

    majors = ['응용정보공학전공', '국제통상전공', '문화미디어전공', '한국어문화교육전공', '바이오생활공학전공']
    second_majors = ['None']


    with col1:
        major_main = st.selectbox('Main Major', tuple(majors))
        majors.remove(major_main)
        second_majors.extend(majors)

    with col2:
        major_second = st.selectbox('Second Major', tuple(second_majors))

    if major_second == 'None':
        credits_main = major_points_by_types(major_main)
        credits_required = find_requirements(major_main, major_second)

        final_df = pd.DataFrame({
        'index': ['전기', '전필', '전선', '3-4000'],

        'required credits': [credits_required['major_basic'],
                             credits_required['major_select'],
                             credits_required['major_man'],
                             credits_required['major_34']],

        'current credits': [credits_main['major_basic'],
                            credits_main['major_select'],
                            credits_main['major_man'],
                            credits_main['major_34']],

        'remaining credits': remaining_credits_counts()
        })

        displayed_df = pd.DataFrame({
        'index': ['전기', '전필', '전선', '3-4000'],

        '이수학점': [credits_main['major_basic'],
                            credits_main['major_select'],
                            credits_main['major_man'],
                            credits_main['major_34']],

        '필요학점': remaining_credits_counts()
        })

        final_df_graph = final_df

        final_df = final_df.set_index('index')
        displayed_df = displayed_df.set_index('index')

    else:
        credits_main = major_points_by_types(major_main)
        credits_second = major_points_by_types(major_second)
        print(credits_second)
        credits_required_main, credits_required_second = find_requirements(major_main, major_second)

        final_df_main = pd.DataFrame({
            'index': ['전기', '전필', '전선', '3-4000'],

            'required credits': [credits_required_main['major_basic'], credits_required_main['major_select'],
                                 credits_required_main['major_man'], credits_required_main['major_34']],

            'current credits': [credits_main['major_basic'], credits_main['major_select'], credits_main['major_man'],
                                credits_main['major_34']],

            'remaining credits': remaining_credits_counts_main()
        })

        final_df_second = pd.DataFrame({
            'index': ['전기', '전필', '전선', '3-4000'],

            'required credits': [credits_required_second['major_basic'], credits_required_second['major_select'],
                                 credits_required_second['major_man'], credits_required_second['major_34']],

            'current credits': [credits_second['major_basic'], credits_second['major_select'], credits_second['major_man'],
                                    credits_second['major_34']],

            'remaining credits': remaining_credits_counts_second()
        })

        displayed_df = pd.DataFrame({
            'index': ['전기', '전필', '전선', '3-4000'],

            '전공1 이수학점': [credits_main['major_basic'], credits_main['major_select'], credits_main['major_man'],
                                credits_main['major_34']],

            '전공1 필요학점': remaining_credits_counts_main(),

            '전공2 이수학점': [credits_second['major_basic'],
                         credits_second['major_man'],
                         credits_second['major_select'],
                         credits_second['major_34']],

            '전공2 필요학점': remaining_credits_counts_second()
        })

        final_df_main = final_df_main.set_index('index')
        final_df_second = final_df_second.set_index('index')

        displayed_df = displayed_df.set_index('index')
        final_df = pd.concat([final_df_main, final_df_second])

        final_df_main_graph = final_df_main
        final_df_second_graph = final_df_second

        final_df_main.reset_index(inplace=True)
        final_df_second.reset_index(inplace=True)

    # expander
    with st.expander(label='Remaining Credits', expanded=True):
        slider_selection = st.select_slider(
            'Select a Category',
            options=['basic', 'bar', 'line']
        )

        if slider_selection == 'basic':
            st.dataframe(displayed_df, width=1000)

        elif slider_selection == 'bar':

            if major_second == 'None':
                st.text('졸업 요건 진행도')
                fig, ax = plt.subplots()

                percentage_values = (final_df_graph['current credits'] / final_df_graph['required credits']) * 100
                percentage_values = percentage_values.apply(lambda x: min(x, 100))

                bars = ax.barh(final_df_graph['index'], percentage_values, linewidth=0.4, left=0)
                ax.set_xlim(0, 100)

                for bar, value in zip(bars, percentage_values):
                    ax.text(value, bar.get_y() + bar.get_height() / 2, f'{value:.1f}%', va='center', ha='left')

                st.pyplot(fig)

            else:
                st.text('전공1 졸업 요건 진행도')
                fig, ax = plt.subplots()

                percentage_values = (final_df_main_graph['current credits'] / final_df_main_graph['required credits']) * 100
                percentage_values = percentage_values.apply(lambda x: min(x, 100))

                bars = ax.barh(final_df_main_graph['index'], percentage_values, linewidth=0.4, left=0)
                ax.set_xlim(0, 100)

                for bar, value in zip(bars, percentage_values):
                    ax.text(value, bar.get_y() + bar.get_height() / 2, f'{value:.1f}%', va='center', ha='left')

                st.pyplot(fig)
                st.divider()

                st.text('전공2 졸업 요건 진행도')
                fig, ax = plt.subplots()

                percentage_values = (final_df_second_graph['current credits'] / final_df_second_graph['required credits']) * 100
                percentage_values = percentage_values.apply(lambda x: min(x, 100))

                bars = ax.barh(final_df_main_graph['index'], percentage_values, linewidth=0.4, left=0)
                ax.set_xlim(0, 100)

                for bar, value in zip(bars, percentage_values):
                    ax.text(value, bar.get_y() + bar.get_height() / 2, f'{value:.1f}%', va='center', ha='left')

                st.pyplot(fig)

        elif slider_selection == 'line':
            if major_second == 'None':
                st.text('필요학점')
                st.line_chart(displayed_df['필요학점'])

            else:
                st.text('전공1: 필요학점')
                st.line_chart(displayed_df['전공1 필요학점'])
                st.divider()

                st.text('전공2: 필요학점')
                st.line_chart(displayed_df['전공2 필요학점'])

        st.divider()

        english = st.select_slider('Choose the number of english classes you are exempt from.', options = ['All', '1', 'None'])

        eng = 0
        religion = 0
        chapel = 0
        RC = 0
        for index in list(df['교과목명']):
            if '기독교' in index:
                religion += 3
            if '채플' in index:
                chapel += 0.5
            if 'RC자기주도' in index:
                RC += 0.5
            if 'RC 101' in index:
                RC += 1
            if 'GLC영어1' in index:
                eng += 3
            if 'GLC영어2' in index:
                eng += 3

        extra = 0
        for index in list(df['과목 종별']):
            if index == '대교':
                extra += 3

        if extra > 9:
            extra = 9

        if english == '1' and 3 - eng < 0:
            eng = 3

        elif english == 'None' and 6 - eng < 0:
            eng = 6

        elif eng > 6:
            eng = 6

        if religion > 3:
            religion = 3

        if chapel > 2:
            chapel = 2

        if RC > 1:
            RC = 1

        if(english == 'All'):
            extra_df = pd.DataFrame({'index': ['기독교', '채플', 'RC', '대학교양'],
                                     'required credits': [3, 2, 1, 9],
                                     'current credits': [religion, chapel, RC, extra],
                                     'remaining credits': [3 - religion, 2 - chapel, 1 - RC, 9 - extra]
                                     })

            extra_displayed_df = pd.DataFrame({'index': ['기독교', '채플', 'RC', '대학교양'],
                                     '이수학점': [religion, chapel, RC, extra],
                                     '필요학점': [3 - religion, 2 - chapel, 1 - RC, 9 - extra]
                                     })

        elif(english == '1'):
            extra_df = pd.DataFrame({'index': ['기독교', '채플', 'RC', '대학교양', '영어'],
                                     'required credits': [3, 2, 1, 9, 3],
                                     'current credits': [religion, chapel, RC, extra, eng],
                                     'remaining credits': [3 - religion, 2 - chapel, 1- RC, 9 - extra, 3 - eng],
                                     })

            extra_displayed_df = pd.DataFrame({'index': ['기독교', '채플', 'RC', '대학교양', '영어'],
                                     '이수학점': [religion, chapel, RC, extra, eng],
                                     '필요학점': [3 - religion, 2 - chapel, 1- RC, 9 - extra, 3 - eng],
                                     })

        else:
            extra_df = pd.DataFrame({'index': ['기독교', '채플', 'RC', '대학교양', '영어'],
                                     'required credits': [3, 2, 1, 9, 6],
                                     'current credits': [religion, chapel, RC, extra, eng],
                                     'remaining credits': [3 - religion, 2 - chapel, 1 - RC, 9 - extra, 6 - eng],
                                     })

            extra_displayed_df = pd.DataFrame({'index': ['기독교', '채플', 'RC', '대학교양', '영어'],
                                     '이수학점': [religion, chapel, RC, extra, eng],
                                     '필요학점': [3 - religion, 2 - chapel, 1 - RC, 9 - extra, 6 - eng],
                                     })

        st.dataframe(extra_displayed_df.set_index('index'), width = 1000)


        buffer = io.BytesIO()

        final_df = final_df.reset_index()
        blank_df = pd.DataFrame({'index': [None], 'required credits': [None], 'current credits': [None], 'remaining credits': [None]})
        sum_df = pd.DataFrame({'index': ['총 학점'],
                               'required credits': [126],
                               'current credits': [np.sum(df['학점'])],
                               'remaining credits': [126 - np.sum(df['학점'])]
                               })

        st.dataframe(sum_df.set_index('index'), width=1000)
        sum_df.reset_index()


        if major_second == 'None':
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                final_df = pd.concat([create_blank_df('학부 요건'),
                                      extra_df,
                                      blank_df,
                                      create_blank_df('전공', major_by_types(major_main)),
                                      final_df,
                                      blank_df,
                                      sum_df])

                final_df = final_df.T
                final_df.columns = final_df.iloc[0]
                final_df = final_df[1:]
                final_df.index = ['요건', '이수학점', '필요학점']

                final_df.to_excel(writer, sheet_name='Sheet1')

        else:
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                final_df = pd.concat([create_blank_df('학부 요건'),
                                      extra_df,
                                      blank_df,
                                      create_blank_df('전공1', major_by_types(major_main)),
                                      final_df_main,
                                      blank_df,
                                      create_blank_df('전공2', major_by_types(major_second)),
                                      final_df_second,
                                      blank_df,
                                      sum_df])

                final_df = final_df.T
                final_df.columns = final_df.iloc[0]
                final_df = final_df[1:]
                final_df.index = ['요건', '이수학점', '필요학점']

                final_df.to_excel(writer, sheet_name='Sheet1')

        download = st.download_button(
            label="Download Summary Data as Excel",
            data=buffer,
            file_name='your grade.xlsx',
            mime='application/vnd.ms-excel'
            )
