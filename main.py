import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Function to analyze sales data
def analyze_sales_data(data):
    total_sales_by_month = data.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
    average_sales = data['Sales'].mean()
    total_sales_by_year = data.groupby(['Year'])['Sales'].sum().reset_index()
    return total_sales_by_month, average_sales, total_sales_by_year

# Function to plot sales data using Plotly
def plot_sales_data(total_sales_by_month):
    # Ensure the 'Month' column is treated as a categorical variable for better plotting
    total_sales_by_month['Month'] = total_sales_by_month['Month'].astype(str)
    fig = px.line(total_sales_by_month, x='Month', y='Sales', title='Sales Trend by Month', markers=True)
    st.plotly_chart(fig)

# Streamlit app layout
st.image("logo.png", use_column_width=True)
# Add custom CSS for logo styling
st.markdown("""
    <style>
    .logo {
        width: 60px;  /* Adjust width */
        height: 60px; /* Adjust height */
        border-radius: 50%;  /* Makes the logo round */
        object-fit: cover;  /* Ensures the image fits */
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("Upload Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Required columns for analysis
required_columns = ['Year', 'Month', 'Sales']

if uploaded_file is not None:
    try:
        sales_data = pd.read_csv(uploaded_file)
        st.write("Uploaded Sales Data:")
        st.dataframe(sales_data)

        # Check if the required columns are present
        if all(col in sales_data.columns for col in required_columns):
            # Use the spinner during the analysis process
            with st.spinner("Analyzing data..."):
                total_sales_by_month, average_sales, total_sales_by_year = analyze_sales_data(sales_data)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader('Total Sales by Month and Year')
                st.dataframe(total_sales_by_month)

            with col2:
                st.subheader('Sales Trend by Month')
                plot_sales_data(total_sales_by_month)

            st.subheader("💡 Suggestions for Business Growth")
            if average_sales > 500:
                st.write("Your business is performing well! 🎉 Consider expanding to new markets or introducing complementary products.")
            else:
                st.write("There’s room for growth. 📈 Focus on improving marketing strategies or identifying underperforming products.")

            with st.expander("See Raw Data"):
                st.dataframe(sales_data)

            st.success("Analysis complete!")
        else:
            # Display a warning if the required columns are missing
            missing_cols = [col for col in required_columns if col not in sales_data.columns]
            st.warning(f"The uploaded CSV file is missing the following required columns: {', '.join(missing_cols)}. Please upload a CSV file with the correct format.")
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.warning('Please upload a CSV file to proceed!')
