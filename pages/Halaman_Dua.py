# membuat drop down pages tambahan yaitu dengan cara membuat folder baru bernama "pages" dan di dalamnya diisi dengan file .py
# list pages yang ditampilkan pada berdasarkan abjad penamaan file .py
# untuk mengurutkan dapat menggunakan format pada penamaan file .py >> "1_(nama file)" yang mana "1_" tidak muncul saat ditampilkan
# referensi https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app

import streamlit as st
import pandas as pd
import plotly_express as px

st.set_page_config(
    page_title="Demo Dashboard", # nama page pada tab browser
    page_icon="💡", # klik tombol Windows & "." (titik) untuk memilih emoji
    layout='wide' # layout tampilan dashboard lebar
)

loan = pd.read_pickle('data_input/loan_clean')
loan['purpose'] = loan['purpose'].str.replace("_", " ") # menghilangkan underscore pada nilai dalam kolom purpose

with st.container(border=True):

    condition = st.selectbox("Select Loan Condition", ["Good Loan", "Bad Loan"])

    loan_condition = loan[loan['loan_condition'] == condition]

    tab4, tab5 = st.tabs(['Loan Amount Distribution Condition', 'Loan Amount Distribution by Purpose'])

    with tab4:
        # Loans Amount Distribution
        histo_term = px.histogram(
            loan,
            x = 'loan_amount',
            nbins=30,
            template='seaborn',
            color='term',
            title='Loan Amount Distribution by Condition',
            labels={
                'loan_amount':'Loan Amount',
                'term':'Loan Term'
            }
        )

        st.plotly_chart(histo_term)

    with tab5:
        # Loan Amount Distribution by Purpose
        box_term = px.box(
            loan,
            x = 'purpose',
            y = 'loan_amount',
            color = 'term',
            title="Loan Amount Distribution by Purpose",
            template='seaborn',
            labels={
                'purpose':'Loan Purpose',
                'loan_amount':'Loan Amount',
                'term':'Loan Term'
            }
        )
        
        st.plotly_chart(box_term)