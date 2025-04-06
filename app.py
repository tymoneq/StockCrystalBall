import pandas as pd
import numpy as np 
import streamlit as st
from scaner import IncomeStatment

st.set_page_config("🔮Tymon's Crystal Ball🔮", "📈", layout="wide", initial_sidebar_state="collapsed")

stockData = pd.read_excel("stockData.xlsx",index_col="Unnamed: 0")


st.title("📊 Porownywarka Danych Finansowych Firm 📊")

img_col1,img_col2,img_col3 = st.columns(3)

with img_col1:
    st.image("img/pepe.png")

with img_col2:
    st.image("img/pepe1.jpeg")
    
with img_col3:
    st.image("img/winnerscompound.png")
    
st.header("Kwartalna Dynamika:")

col1, col2 = st.columns(2)

with col1:
    options = str(st.selectbox("Jakie dane chcesz porownac?",["Przychody ze sprzedaży","Techniczny koszt wytworzenia produkcji sprzedanej",
                   "Koszty sprzedaży","Zysk ze sprzedaży","Zysk operacyjny (EBIT)","Zysk przed opodatkowaniem","Zysk netto",
                   "Zysk netto akcjonariuszy jednostki dominującej"]))
    
with col2:
    dynamics = float(st.number_input("Jaka ma byc dynamika zmian w %?",value=10.00,step = 0.5))

df_reversed = stockData.iloc[::-1]
diff = df_reversed.diff().iloc[::-1]

#highlights the diffrence between two datas
def highlightChange(s):
    color = 'black'
    name = str(s.name)
    row_index = stockData.index.get_loc(name)
    prev_row_index = row_index+1
    try:
        prev_row_data = stockData.iloc[prev_row_index]
        change = prev_row_data[options] * (1 + (dynamics/100))
        if s[options] >= change:
            color  = "green"
    except:
        color='black'
   
    return ['background-color: {}'.format(color)]* len(s)

#highlight every cell in diffrence data frame
def highlightedChanges(val):
    color = 'green' if val > 0 else 'red'
    return f'background-color: {color}'

for stock in IncomeStatment:
    with st.container():
        st.header("Dane Finansowe {}".format(stock))
        st.dataframe(stockData.style.apply(highlightChange,axis=1).format(thousands='.'),width=1800)
        st.header("Kwartalne Zmiany w Danych Finansowych CDR")
        st.dataframe(diff.style.format(thousands='.',precision=2).applymap(highlightedChanges,subset = list(stockData.columns)),width=1800)

