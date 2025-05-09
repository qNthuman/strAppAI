```python
import streamlit as st
import pandas as pd
from utils import get_db_connection

st.title("📈 Dashboard")

conn = get_db_connection()

st.subheader("DPP Performance")
dpp_df = pd.read_sql_query("SELECT * FROM dpp_logs", conn)
st.dataframe(dpp_df)

st.subheader("Mock Test Trends")
mock_df = pd.read_sql_query("SELECT * FROM mock_tests", conn)
st.dataframe(mock_df)
```
