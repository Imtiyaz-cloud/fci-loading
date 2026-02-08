import streamlit as st 
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Google Sheet se connect karne ke liye
conn = st.connection("gsheets", type=GSheetsConnection, credentials="google_keys.json")

# Aapki sheet ka link
url = ""

# sheet se data uthane ke liye
df = conn.read(spreadsheet=url)

#Screen par dikhane ke liye
st.title("FCI Online Data") st.dataframe(df)

# Data save karne ke liye (Sample button)
if st.button("Data Update Karein"): conn.update(spreadsheet=url, data=df) st.success("Data safalta purvak save ho gaya!")


