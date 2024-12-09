import streamlit as st
import pandas as pd

# Placeholder DataFrame to store the entries
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Barcode", "Drug Name", 
                                                  "Weight Box", "Weight Strip", 
                                                  "Weight Tablet", "Bulk Quantity"])

# Function to add a row to the DataFrame
def add_row():
    new_row = {
        "Barcode": st.session_state.barcode,
        "Drug Name": st.session_state.drug_name,
        "Weight Box": st.session_state.weight_box,
        "Weight Strip": st.session_state.weight_strip,
        "Weight Tablet": st.session_state.weight_tablet,
        "Bulk Quantity": st.session_state.bulk_quantity
    }
    st.session_state.data = st.session_state.data.append(new_row, ignore_index=True)
    clear_inputs()

# Function to clear input fields
def clear_inputs():
    st.session_state.barcode = ""
    st.session_state.drug_name = ""
    st.session_state.weight_box = 0.0
    st.session_state.weight_strip = 0.0
    st.session_state.weight_tablet = 0.0
    st.session_state.bulk_quantity = 0

# Sidebar Instructions
with st.sidebar:
    st.markdown("### How to Record Weight Information?")
    st.markdown("""
    1. **Scan barcode** and drug name information will be retrieved from the database.
    2. **Click on the appropriate field box**, click 'Record' to enter the weight captured from the weighing scale.
    3. If there is a second batch for the same field, **click 'Add'** to add more weight captured.
    4. **Click 'Confirm'** to enter data into the datasheet and clear the form for the next entry.
    """)

# App Layout
st.title("Data Entry Interface")

# Input fields with Record/Add Buttons
with st.form(key="data_entry_form", clear_on_submit=False):
    # Barcode and Drug Name
    st.text_input("Scan Barcode", key="barcode")
    st.text_input("Drug Name", key="drug_name")
    
    # Weight readings with Record and Add buttons
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.number_input("Weight Reading/Unit Box (g)", value=0.0, step=0.01, key="weight_box")
    with col2:
        if st.button("Record Box", key="record_box"):
            st.session_state.weight_box += st.session_state.weight_box
    with col3:
        if st.button("Add Box", key="add_box"):
            st.session_state.weight_box += st.session_state.weight_box

    col4, col5, col6 = st.columns([3, 1, 1])
    with col4:
        st.number_input("Weight Reading/Unit Strip (g)", value=0.0, step=0.01, key="weight_strip")
    with col5:
        if st.button("Record Strip", key="record_strip"):
            st.session_state.weight_strip += st.session_state.weight_strip
    with col6:
        if st.button("Add Strip", key="add_strip"):
            st.session_state.weight_strip += st.session_state.weight_strip

    col7, col8, col9 = st.columns([3, 1, 1])
    with col7:
        st.number_input("Weight Reading/Unit Tablet/Capsule (g)", value=0.0, step=0.01, key="weight_tablet")
    with col8:
        if st.button("Record Tablet", key="record_tablet"):
            st.session_state.weight_tablet += st.session_state.weight_tablet
    with col9:
        if st.button("Add Tablet", key="add_tablet"):
            st.session_state.weight_tablet += st.session_state.weight_tablet

    # Bulk Quantity
    st.number_input("Bulk Quantity/No. of Units", value=0, step=1, key="bulk_quantity")

    # Confirm Button
    if st.form_submit_button("Confirm"):
        if st.session_state.barcode and st.session_state.drug_name:
            add_row()
            st.success("Entry confirmed and added to the datasheet!")
        else:
            st.error("Please fill in Barcode and Drug Name.")

# Display the updated table
st.markdown("### Data Table")
st.dataframe(st.session_state.data)

# Option to download the data
csv = st.session_state.data.to_csv(index=False).encode("utf-8")
st.download_button(label="Download Table", data=csv, file_name="data_entry_table.csv", mime="text/csv")
