
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import binom_test
from scipy.stats import shapiro
from scipy.stats import levene
from scipy.stats import ttest_ind


st.title('**Больничные дни сотрудников**')
st.sidebar.title("Параметры")

@st.cache_data (experimental_allow_widgets=True)

#Загрузка csv файла

def load_data():
    uploaded_file = st.file_uploader(label='**Выберите файл csv**', type= '.csv')
    if uploaded_file is not None:
        csv_data = pd.read_csv(uploaded_file,sep=',', encoding = 'cp1251', quoting=3)
        csv_data = csv_data.rename(columns= lambda x: x.replace('"',''))\
                             .rename(columns= {'Количество больничных дней': 'work_days','Возраст': 'age','Пол':'sex'})
        
        csv_data['work_days'] = csv_data['work_days'].str.replace('"', '')
        csv_data['sex'] =csv_data['sex'].str.replace('"', '')
        csv_data['work_days'] = csv_data['work_days'].astype (str).astype (int)              
        return csv_data
    
    else:
        return None
    
csv_data = load_data()

#Просмотр откорректированного файла

show_data = st.button('Показать данные')
if show_data == True:
    st.subheader('Загруженные данные')
    st.write(csv_data)

#Сайтбар с параметрами для выбора
#Количество дней

show_work_days = st.sidebar.checkbox('Выбрать количество дней')

if show_work_days:
    min_work_days = csv_data['work_days'].min()
    max_work_days = csv_data['work_days'].max()
    min_work_days, max_work_day = st.sidebar.slider("Больничные дни", min_value=min_work_days, max_value=max_work_days, value=[min_work_days, max_work_days])
    csv_data = csv_data[(csv_data['work_days'] >= min_work_days) & (csv_data['work_days']  <= max_work_days)]

#Возраст

choose_age = st.sidebar.checkbox('Выбрать возраст')
if choose_age:
    min_age= csv_data['age'].min()
    max_age= csv_data['age'].max()
    min_age, max_age = st.sidebar.slider("Возраст", min_value=min_age, max_value=max_age, value=[min_age, max_age])
    csv_data = csv_data[(csv_data['age'] >= min_age) & (csv_data['age']  <= max_age)]

#Графики


show_age = st.sidebar.checkbox('Визуализировать данные по возрастным группам младше и старше 35')

if show_age == True:
    st.subheader('Возраст')
    sns.distplot(csv_data.query('age >= 35').work_days, color = '#8B4513')
    sns.distplot(csv_data.query('age < 35').work_days, color = '#4B0082')
    sns.despine()
    st.pyplot()

show_sex = st.sidebar.checkbox('Визуализировать распределение по гендерному признаку')

if show_sex == True:
   st.subheader('Пол')
   sns.distplot(csv_data.query('sex == "Ж"').work_days, color = '#CD853F' )
   sns.distplot(csv_data.query('sex == "М"').work_days, color = '#BA55D3')  

   st.pyplot()



#Тест Левене

show_levene_sex = st.button('Тест Левене ("sex")')

if show_levene_sex:
    st.subheader('Значение P-value')
    
    m_work_days =csv_data[csv_data['sex'] == "М"].sample(30)['work_days']
    w_work_days =csv_data[csv_data['sex'] == "Ж"].sample(30)['work_days']

    st.write(levene(m_work_days, w_work_days, center = 'mean'))

show_levene_age= st.button('Тест Левене ("age")')

if show_levene_age:
    st.subheader('Значение P-value')

    older_work_days =csv_data[csv_data['age'] >= 35].sample(20)['work_days'] 
    younger_work_days =csv_data[csv_data['age'] < 35].sample(20)['work_days']

    st.write(levene(older_work_days, younger_work_days , center = 'mean'))
