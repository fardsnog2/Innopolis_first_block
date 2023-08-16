import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import numpy as np
import scipy.stats as stats
import random



def visualization(df,is_num):
    if is_num:
        val = df.value_counts()
        lab = df.unique().tolist()
        fig = go.Figure(
            px.bar(
            df,
            x=lab,
            y=val,
            labels={'x': 'Значение', 'y':'Кол-во'},
            width=800, height=400
            # hoverinfo = "label+percent",
            # textinfo = "label+value",
        ))
        st.plotly_chart(fig)
    else:
        val = df.value_counts()[:20]
        lab = df.unique().tolist()
        fig = go.Figure(
            go.Pie(
            labels = lab,
            values = val,
            hoverinfo = "label+percent",
            textinfo = "label+value",
        ))
        st.plotly_chart(fig)
        st.write('Были выбранны первые 20 значений для понятной визуализации, чтоб было удобно смотреть' )

def check_hypothesis(hyp,df,alpha,df1):
    if hyp == 'Случайная величина в первом столбце распределена нормально':
        res = stats.shapiro(df)
        st.write(f'p-value = {res.statistic}, alpha = {alpha}')
        if res.statistic < alpha:
            st.write('Значение p-value меньше чем альфа следовательно можно отвергнуть что случайная величина распределена нормально' )
        else:
            st.write('Значение p-value больше чем альфа следовательно нельзя отвергнуть что случайная величина распределена нормально')
    elif 'Среднее значение во втором столбце равно ' in hyp:
        p_value = stats.ttest_1samp (a=df1.tolist(), popmean= rand_mean )[1]
        st.write(f'p-value = {p_value}, alpha = {alpha}')
        if p_value < alpha:
            st.write(f'Значение p-value меньше чем альфа следовательно можно отвергнуть что среднее значение во втором столбце равно {rand_mean}' )
        else:
            st.write(f'Значение p-value больше чем альфа следовательно нельзя отвергнуть что среднее значение во втором столбце равно {rand_mean}')
    



def preprocessing(df,is_num):
    if is_num:
        return df.fillna(df.mean())# если количественный признак то заменяю пропуски на среднее кол-во, чтобы кол-во строк было таким же
    return df.fillna(df.mode())# если не количетсвенный, то пропуски заменяю на моду



def run():
    st.title('TEST')
    uploaded_file = st.file_uploader("Выбиерите CSV файл")
    if uploaded_file is not None:
        # To read file as bytes:
        if uploaded_file.name.split('.')[-1]!='csv':
            st.write('Файл не csv загрузите другой файл')
        else:
            try:
                df = pd.read_csv(uploaded_file)
                col = tuple(df.columns)
                num_cols = df._get_numeric_data().columns
                st.dataframe(df)
                first_col = st.selectbox('Выберите первую колонку',
                                        col)
                first_num = first_col in num_cols
                
                first_col_df = preprocessing(df[first_col],first_num)
                st.write('Вы выбрали:', first_col, ', он количественный' if first_num else ', он не количественный')
                second_col = st.selectbox('Выберите вторую колонку',
                                        col)
                second_num = second_col in num_cols
                second_col_df = preprocessing(df[second_col],second_num)
                global rand_mean
                rand_mean = second_col_df.tolist()[len(second_col_df.tolist())//2]
                st.write('Вы выбрали:', ', он количественный' if  second_num else', он не количественный')
                visualization(first_col_df,first_num)
                visualization(second_col_df,second_num)
                alpha = 0.05
                is_can_hyp=True
                if first_num and second_col:
                    lst_hypothesis=tuple(['Случайная величина в первом столбце распределена нормально',f'Среднее значение во втором столбце равно = {rand_mean}'])
                elif first_num:
                    lst_hypothesis=tuple(['Случайная величина в первом столбце распределена нормально'])
                elif second_num:
                    lst_hypothesis=tuple([f'Среднее значение во втором столбце равно = {rand_mean}'])
                else:
                    is_can_hyp=False
                    st.write('Для двух не количественных переменных гипотез к сожалению нет :(')
                if is_can_hyp:
                    hypothesis = st.selectbox('Выберите одну из гипотез',
                                            lst_hypothesis)
                    check_hypothesis(hypothesis,first_col_df,alpha,second_col_df)
            except UnicodeDecodeError:
                st.write('Ошибка с кодировкой в файле попробуйте поменять или загрузить другой')
            except:
                st.write("К сожалению я не знаю что с вашим файлом и почему нельзя его загрузить...")
            
if __name__=='__main__':
    run()