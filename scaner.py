import pandas as pd
import numpy as np
import yfinance as yf

pd.set_option('future.no_silent_downcasting', True)
writer = pd.ExcelWriter('stockData.xlsx', engine='xlsxwriter')

newColumnsNamesIncomeStmt = ["Przychody ze sprzedaży","Techniczny koszt wytworzenia produkcji sprzedanej",
                   "Koszty sprzedaży","Zysk ze sprzedaży","Zysk operacyjny (EBIT)","Zysk przed opodatkowaniem","Zysk netto",
                   "Zysk netto akcjonariuszy jednostki dominującej"]

newColumnsNamesBalanceSheet = ["Aktywa trwałe","Wartości niematerialne i prawne","Wartość firmy","Rzeczowe składniki majątku trwałego",
                               "Inwestycje długoterminowe", "Pozostałe aktywa trwałe","Aktywa obrotowe","Zapasy",
                               "Inwestycje krótkoterminowe", "Środki pieniężne i inne aktywa pieniężne",
                               "Pozostałe aktywa obrotowe", "Kapitał własny akcjonariuszy jednostki dominującej",
                               "Kapitał (fundusz) podstawowy", "Zobowiązania długoterminowe",
                               "Zobowiązania krótkoterminowe","Pasywa razem"]

newColumnsNamesCashFlow = ["Przepływy pieniężne z działalności operacyjnej", "Przepływy pieniężne z działalności inwestycyjnej",
                           "Przepływy pieniężne z działalności finansowej", "Emisja akcji", "Dywidenda",
                           "Przepływy pieniężne razem", "Free Cash Flow"]


def GetStockData(stock):
    StockData = yf.Ticker(stock)
    #Downloading Data
    cashFlow = StockData.quarterly_cash_flow.fillna(0)
    balanceSheet = StockData.quarterly_balance_sheet.fillna(0)
    incomeStmt = StockData.quarterly_income_stmt.fillna(0)
    
    #Transposing Data
    cashFlow = cashFlow.T
    balanceSheet = balanceSheet.T
    incomeStmt = incomeStmt.T
    
    
    NewIncomeStmt = pd.DataFrame(columns=newColumnsNamesIncomeStmt)
    NewIncomeStmt["Przychody ze sprzedaży"] = incomeStmt["Total Revenue"]
    NewIncomeStmt["Techniczny koszt wytworzenia produkcji sprzedanej"] = incomeStmt["Cost Of Revenue"]
    NewIncomeStmt["Koszty sprzedaży"] = incomeStmt["Operating Expense"]
    NewIncomeStmt["Zysk ze sprzedaży"] = incomeStmt["Total Revenue"] - incomeStmt["Cost Of Revenue"] - incomeStmt["Operating Expense"]
    NewIncomeStmt["Zysk operacyjny (EBIT)"] = incomeStmt["Total Operating Income As Reported"]
    NewIncomeStmt["Zysk przed opodatkowaniem"] = incomeStmt["Pretax Income"]
    NewIncomeStmt["Zysk netto"] = incomeStmt["Net Income"]
    NewIncomeStmt["Zysk netto akcjonariuszy jednostki dominującej"] = incomeStmt["Net Income Common Stockholders"]
    
    
    NewBalanceSheet = pd.DataFrame(columns=newColumnsNamesBalanceSheet)
    NewBalanceSheet["Aktywa razem"] = balanceSheet["Total Assets"]
    NewBalanceSheet["Aktywa obrotowe"] = balanceSheet["Current Assets"]
    NewBalanceSheet["Aktywa trwałe"] = balanceSheet["Total Non Current Assets"]
    NewBalanceSheet["Inwestycje krótkoterminowe"] = balanceSheet["Cash Cash Equivalents And Short Term Investments"]
    NewBalanceSheet["Środki pieniężne i inne aktywa pieniężne"] = balanceSheet["Cash And Cash Equivalents"]
    NewBalanceSheet["Zapasy"] = balanceSheet["Inventory"]
    NewBalanceSheet["Pozostałe aktywa obrotowe"] = balanceSheet["Prepaid Assets"]
    NewBalanceSheet["Rzeczowe składniki majątku trwałego"] = balanceSheet["Net PPE"]
    NewBalanceSheet["Wartości niematerialne i prawne"] = balanceSheet["Goodwill And Other Intangible Assets"]
    NewBalanceSheet["Pozostałe aktywa trwałe"] = balanceSheet["Non Current Prepaid Assets"] + balanceSheet["Non Current Deferred Taxes Assets"]
    NewBalanceSheet["Inwestycje długoterminowe"] = balanceSheet["Total Non Current Assets"] - balanceSheet["Net PPE"] - balanceSheet["Goodwill And Other Intangible Assets"] - balanceSheet["Non Current Deferred Taxes Assets"] - balanceSheet["Non Current Prepaid Assets"]
    NewBalanceSheet["Kapitał własny akcjonariuszy jednostki dominującej"] = balanceSheet["Stockholders Equity"]
    NewBalanceSheet["Kapitał (fundusz) podstawowy"] = balanceSheet["Capital Stock"]
    NewBalanceSheet["Zobowiązania krótkoterminowe"] = balanceSheet["Current Liabilities"]
    NewBalanceSheet["Zobowiązania długoterminowe"] = balanceSheet["Total Non Current Liabilities Net Minority Interest"]
    NewBalanceSheet["Pasywa razem"] = balanceSheet["Total Assets"]
    
   
    NewCashFlow = pd.DataFrame(columns=newColumnsNamesCashFlow)
    NewCashFlow["Przepływy pieniężne z działalności operacyjnej"] = cashFlow["Operating Cash Flow"]
    NewCashFlow["Przepływy pieniężne z działalności inwestycyjnej"] = cashFlow["Investing Cash Flow"]
    NewCashFlow["Przepływy pieniężne z działalności finansowej"] = cashFlow["Financing Cash Flow"]
    NewCashFlow["Emisja akcji"] = cashFlow["Issuance Of Capital Stock"]
    NewCashFlow["Przepływy pieniężne razem"] = cashFlow["Changes In Cash"]
    NewCashFlow["Free Cash Flow"] = cashFlow["Free Cash Flow"]
    NewCashFlow["Dywidenda"] = cashFlow["Cash Dividends Paid"]
    
    
    # NewCashFlow = NewCashFlow.T
    # NewBalanceSheet = NewBalanceSheet.T
    # NewIncomeStmt = NewIncomeStmt.T
    
    NewIncomeStmt.to_excel(writer,sheet_name=str(stock)+"IncomeStmt")
    NewBalanceSheet.to_excel(writer,sheet_name=str(stock)+"BalanceSheet")
    NewCashFlow.to_excel(writer,sheet_name=str(stock)+"CashFlow")
    

listOfStocks = ["CDR"]

for i in range(len(listOfStocks)):
    listOfStocks[i] = listOfStocks[i] +".WA"

for stock in listOfStocks:
    GetStockData(stock)
    
    
writer.close()