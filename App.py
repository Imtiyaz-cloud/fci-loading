import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="FCI Cloud Loading App", layout="wide")
st.title("🌾 FCI Rake Loading (Cloud System)")

# 1. Google Sheets se Connect karein
# Note: Iske liye aapko .streamlit/secrets.toml mein link dalna hoga ya niche direct use karein
url = "APNI_GOOGhttps://docs.google.com/spreadsheets/d/1vjWHkuL-EDj_6A6X-eaWNuFASwMfxX_rIYwu6nlw6bU/edit?gid=0#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Data Read karein
try:
    data = conn.read(spreadsheet=url)
except:
    data = pd.DataFrame(columns=['wagon_no', 'gate_pass', 'truck_no', 'bags', 'weight', 'entry_time'])

# Sidebar Summary
st.sidebar.header("Rake Live Stats")
if not data.empty:
    st.sidebar.metric("Total Weight (Qtls)", f"{pd.to_numeric(data['weight']).sum():.2f}")
    st.sidebar.metric("Total Bags", int(pd.to_numeric(data['bags']).sum()))

# 3. Entry Form
with st.expander("➕ Mobile Entry Form", expanded=True):
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            wagon = st.text_input("Wagon No.")
            gp_no = st.text_input("Gate Pass No.")
        with col2:
            truck = st.text_input("Truck No.")
            bags = st.number_input("Bags", min_value=0, step=1)
            weight = st.number_input("Weight (Qtls)", min_value=0.0, step=0.1)
        
        submit = st.form_submit_button("Submit to Cloud")

        if submit:
            # Capacity Check (640 Qtls)
            wagon_wt = pd.to_numeric(data[data['wagon_no'] == wagon]['weight']).sum()
            
            if wagon_wt + weight > 640:
                st.error(f"❌ Limit Exceeded! Wagon {wagon} mein pehle se {wagon_wt} Qtls hai.")
            else:
                # Naya data prepare karein
                new_entry = pd.DataFrame([{
                    "wagon_no": wagon,
                    "gate_pass": gp_no,
                    "truck_no": truck,
                    "bags": bags,
                    "weight": weight,
                    "entry_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                
                # Sheet update karein
                updated_df = pd.concat([data, new_entry], ignore_index=True)
                conn.update(spreadsheet=url, data=updated_df)
                st.success("✅ Cloud par data save ho gaya!")
                st.rerun()

# 4. Dashboard
st.divider()
tab1, tab2 = st.tabs(["Wagon Summary", "Full Rake Log"])

with tab1:
    if not data.empty:
        summary = data.groupby('wagon_no').agg({'bags':'sum', 'weight':'sum'}).reset_index()
        st.table(summary)

with tab2:
    st.dataframe(data)
