import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def isportfoy():
    is_portfoy_fund_list = ['IAG', 'IYG', 'ISZ']
    url = 'https://www.isportfoy.com.tr/tr/yatirim-fonlari'
    html = requests.get(url).content
    df_list = pd.read_html(html, encoding='utf-8', decimal=',', thousands='.')
    df = df_list[0]
    new_df = df[df[('Fon Kodu', 'Fon Kodu')].isin(is_portfoy_fund_list)]
    new_df = new_df[[('Fon Kodu', 'Fon Kodu'), ('Birim Pay Fiyatı', 'Birim Pay Fiyatı')]]
    new_df.columns = ['FUND', 'PRICE']
    return new_df


def fund_price(fund_code, start_date, end_date, type="YAT"):
    url = "https://www.tefas.gov.tr/api/DB/BindHistoryInfo"
    data = {
        "fontip": type,
        "sfontur": "",
        "fonkod": fund_code,
        "fongrup": "",
        "bastarih": start_date,
        "bittarih": end_date,
        "fonturkod": "",
        "fonunvantip": "",
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        dataframe = pd.DataFrame(response.json()["data"])
        return dataframe
    else:
        return None

def main():
   
    if st.button("Start"):
        current_date = datetime.now().date()
        formatted_date_1 = current_date.strftime("%d/%m/%Y")
        formatted_date_2 = current_date.strftime("%d.%m.%Y")
        formatted_date_3 = current_date.strftime("%Y%m%d")
        fund_list = ['GPA', 'TPL', 'IJT', 'TGE', 'AFA', 'AFS', 'AFT', 'KLU', 'TCA',
                     'AES', 'TPC', 'DLY', 'DCB', 'DTL', 'DBH', 'TUA', 'DPK',
                     'TCF', 'TJI', 'TRR', 'PUR', 'FSK', 'PPZ', 'NRG', 'TE4', 'TE3',
                     'DYN', 'DVT', 'DLD']

        kontrol = pd.DataFrame()
        for fund in fund_list:
            price = fund_price(fund, formatted_date_2, formatted_date_2)
            kontrol = pd.concat([kontrol, price])

        kontrol = kontrol[["FONKODU", "FIYAT"]]
        kontrol.columns = ['FUND', 'PRICE']

        new_df = isportfoy()
        result = pd.concat([kontrol, new_df]).reset_index(drop=True)

        export = pd.DataFrame({"date": formatted_date_1,
                               "fund": result["FUND"],
                               "price1": result["PRICE"],
                               "price2": result["PRICE"],
                               "price3": result["PRICE"]})

        export_filename = f'{formatted_date_3}.csv'

        export.to_csv(f'{export_filename}', index=False, header=False)

        st.success("Ready.")
       
        st.download_button(
            label="Download",
            data=export.to_csv(index=False, header=False, sep=";").encode('utf-8'),
            file_name=export_filename,
            mime='text/csv',
        )

if __name__ == "__main__":
    main()
