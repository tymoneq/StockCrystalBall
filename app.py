import pandas as pd
import numpy as np 
import streamlit as st
import webcolors as wc


st.set_page_config("🔮Tymon's Crystal Ball🔮", "📈", layout="wide", initial_sidebar_state="collapsed")

stockData = pd.read_excel("stockData.xlsx",index_col="Unnamed: 0")


st.title("📊 Porownywarka Danych Finansowych Firm 📊")


col1, col2 = st.columns(2)

with col1:
    options = str(st.selectbox("Jakie dane chcesz porownac?",["Przychody ze sprzedaży","Techniczny koszt wytworzenia produkcji sprzedanej",
                   "Koszty sprzedaży","Zysk ze sprzedaży","Zysk operacyjny (EBIT)","Zysk przed opodatkowaniem","Zysk netto",
                   "Zysk netto akcjonariuszy jednostki dominującej"]))
    
with col2:
    dynamics = st.number_input("Jaka ma byc dynamika zmian w %?",value=10.00,step = 0.5)

df_reversed = stockData.iloc[::-1]
diff = df_reversed.diff().iloc[::-1]


#highlights the diffrence between two datas
def highlightChange(s):
    color = 'black'
    name = s.name
    # st.write(name)
    if s[options] > 1000000:
        color  = "green"
    return ['background-color: {}'.format(color)]* len(s)

#highlight every cell in diffrence data frame
def highlightedChanges(val):
    color = 'green' if val > 0 else 'red'
    return f'background-color: {color}'
   

st.dataframe(stockData.style.apply(highlightChange,axis=1).format(thousands='.'),width=1800)
st.dataframe(diff.style.format(thousands='.').applymap(highlightedChanges,subset = list(stockData.columns)),width=1800)

