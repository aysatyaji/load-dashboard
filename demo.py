import streamlit as st
import pandas as pd
import plotly_express as px

st.set_page_config(
    page_title="Demo Dashboard", # nama page pada tab browser
    page_icon="💡", # klik tombol Windows & "." (titik) untuk memilih emoji
    layout='wide' # layout tampilan dashboard lebar
)

st.title("Financial Insights Dashboard: Loan Performance & Trends")
st.markdown("---") # Menambahkan garis

st.sidebar.header("Dashboard Filters and Features")
st.sidebar.subheader("Features")
st.sidebar.markdown(
'''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
'''
)

loan = pd.read_pickle('data_input/loan_clean')
loan['purpose'] = loan['purpose'].str.replace("_", " ") # menghilangkan underscore pada nilai dalam kolom purpose

# Container dapat digunakan untuk mengelompokan fitur jika diperlukan
with st.container(border=True): # Gunakan parameter border untuk memberikan garis
    col1, col2 = st.columns(2) # Mendefinisikan nama kolom

    with col1: # Isi dari kolom pertama
        st.metric("Total Loans", f"{loan['id'].count():,.0f}", help="Total Number of Loans")
        st.metric("Total Loan Amount", f"${loan['loan_amount'].sum():,.0f}", help="Sum of All Loan Amounts")

    with col2: # Isi dari kolom kedua
        st.metric("Average Interest Rate", f"{loan['interest_rate'].mean():,.2f}%", help="Percentage of the loan amount that the borrower has to pay")
        st.metric("Average Loan Amount", f"${loan['loan_amount'].mean():,.0f}", help="Average interest rate across all loans")

with st.container(border=True):
    tab1, tab2, tab3 = st.tabs(['Loans Issued Over Time', 'Loan Amount Over Time', 'Issue Date Analysis'])

    with tab1:   
        # Loans Issued Over Time
        loan_date_count = loan.groupby('issue_date')['loan_amount'].count()
    
        line_count = px.line(
            loan_date_count,
            markers = True,
            labels={
                'value':'Number of Loans',
                'issue_date':'Issue Date'
            },
            template='seaborn',
            title='Number of Loans Issued Over Time'
        ).update_layout(showlegend = False)

        st.plotly_chart(line_count)

    with tab2:
        # Loan Amount Over Time
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()

        line_sum = px.line(
            loan_date_sum,
            markers = True,
            labels={
                'value':'Number of Loans',
                'issue_date':'Issue Date'
            },
            template='seaborn',
            title='Total Loan Amount Issued Over Time'
        ).update_layout(showlegend = False)
        
        st.plotly_chart(line_sum)

    with tab3:
        # Issue Date Analysis
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()

        bar_count = px.bar(
        loan_day_count,
            category_orders={ # Mengatur urutan categori (hari)
                'issue_weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            },
            title='Distribution of Loans by Day of the Week',
            labels={
                'value':'Number of Loans',
                'issue_weekday':'Day of the Week'
            },
            template='seaborn'
        ).update_layout(showlegend=False)

        st.plotly_chart(bar_count)

st.subheader("Loan Performance")

with st.expander("Click here to expand visualization"):
    with st.container(border=True):
        col3, col4 = st.columns(2)

        with col3:
            # Loan Condition Analysis
            pie = px.pie(
                loan,
                names = 'loan_condition',
                hole = 0.5,
                title = 'Distribution of Loans by Condition',
                template='seaborn'
            ).update_traces(textinfo='percent + value')
            
            st.plotly_chart(pie)

        with col4:
            # Grade Distribution
            grade = loan['grade'].value_counts().sort_index()

            bar = px.bar(
                grade,
                title='Distribution of Loans by Grade',
                labels={
                    'grade':'Grade',
                    'value':'Number of Loans'
                },
            template='seaborn'
            ).update_layout(showlegend=False)
            
            st.plotly_chart(bar)

st.subheader("Financial Analysis")

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

