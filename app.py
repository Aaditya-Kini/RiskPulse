import streamlit as st
import sqlite3
import pandas as pd

# Function to fetch data using complex SQL
@st.cache_data # Caches the data so the DB isn't hit on every button press
def get_analytics_data():
    conn = sqlite3.connect('risk_database.db')
    
    # We can run our complex CTE query directly into a pandas dataframe
    query = """
        WITH RiskBuckets AS (
            SELECT 
                c.home_ownership,
                COUNT(l.loan_id) as total_loans,
                SUM(CASE WHEN l.status = 1 THEN 1 ELSE 0 END) as default_count
            FROM Customers c
            JOIN Loans l ON c.customer_id = l.customer_id
            GROUP BY c.home_ownership
        )
        SELECT 
            home_ownership,
            total_loans,
            default_count,
            ROUND(CAST(default_count AS FLOAT) / total_loans * 100, 2) as default_rate_pct
        FROM RiskBuckets
        ORDER BY default_rate_pct DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("Credit Risk Analytics")

# Display the SQL-driven data
st.subheader("Default Rates by Home Ownership")
analytics_df = get_analytics_data()

# Show the raw data from the query
st.dataframe(analytics_df)

# Plot it using Streamlit's native charts
st.bar_chart(data=analytics_df, x='home_ownership', y='default_rate_pct')