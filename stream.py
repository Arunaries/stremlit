"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import openpyxl
st.set_page_config(page_title='Fuel expenditure', layout = 'wide', initial_sidebar_state = 'auto')
import pandas as pd
from io import StringIO
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.title('Fuel amount spend')
#st.info('This is a purely informational message', icon="ℹ️")


uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:

    #bytes_data = uploaded_file.getvalue()
    #st.write(bytes_data)

    # To convert to a string based IO:
    #stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #st.write(stringio)

    # To read file as string:
    #string_data = stringio.read()
    #st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_excel(uploaded_file)
    #st.write(df)

#df = pd.read_excel('BPCL - Sale Transaction history report for Oct-22.xlsx', index_col=0)

    df2 = df.copy() 

    space_remove_1 = df2.columns = df2.columns.str.replace(' ', '',regex=True)
    space_remove_2 = df2.columns = df2.columns.str.replace('[/,.,(]', '',regex=True)
    space_remove_3 = df2.columns = df2.columns.str.replace('[)]', '',regex=True)

    print(space_remove_3)

#group_by = df2.groupby(['VehicleNumber']).agg('sum')

    group_by = df2.groupby(['VehicleNumber'])[['ProductVolumeQuantityLitres','TransactionAmountRs']].sum()


    df3 = group_by.copy()

#fuel_price = float(input('Fuel_price:'))
#liters_allowed = float(input('Liters_allowed:'))
#amount_allowed = float(input('Amount_allowed:'))
    
    fuel_price = st.number_input('Enter Fuel price in INR')

    #fuel_price = st.slider('Select Fuel', 0, 130, 25)

    #fuel_price = 95

    liters_allowed = st.slider('Liters allowed', 0, 300, 190)

    amount_allowed = st.slider('Amount allowed', 0,50000,16000)

    #liters_allowed = 190
    #amount_allowed = 16000

    df4 = cal_fuel_unused = df3.assign(Unconsumed_fuel_in_ltrs = liters_allowed - df3.ProductVolumeQuantityLitres)

    df5 = amount_for_unconsumed_fuel =  df4.assign(price_unconsumed_fuel = df4.Unconsumed_fuel_in_ltrs * fuel_price)

    amount_to_be_credited = df5.assign(amount_to_be_credited = df5.price_unconsumed_fuel + amount_allowed)

    st.dataframe(amount_to_be_credited)

    amount_to_be_credited.to_excel("amount_to_be_credited.xlsx")
    print(amount_to_be_credited)



    

    #final_out = amount_to_be_credited
   
    #st.download_button(label="Download data as excel",
    #data=final_out,
    #file_name='amount_to_be_credited.xlsx',
    #mime='text/vnd.ms-excel',
#)


