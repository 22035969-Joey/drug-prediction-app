import streamlit as st
import pandas as pd

# Placeholder DataFrame to store the entries
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Barcode", "Drug Name", 
                                                  "Weight Box", "Weight Strip", 
                                                  "Weight Tablet", "Bulk Quantity"])

# Functions to handle data logic
def clear_inputs():
    st.session_state.barcode = ""
    st.session_state.drug_name = ""
    st.session_state.weight_box = 0.0
    st.session_state.weight_strip = 0.0
    st.session_state.weight_tablet = 0.0
    st.session_state.bulk_quantity = 0

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

# Sidebar for instructions
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

# Data entry form
with st.form(key="data_entry_form", clear_on_submit=False):
    st.text_input("Scan Barcode", key="barcode")
    st.text_input("Drug Name", key="drug_name")

    # Weight readings with "Record" and "Add" buttons
    st.markdown("#### Weight Reading Inputs")
    weight_box = st.number_input("Weight Reading/Unit Box (g)", value=0.0, step=0.01, key="weight_box_input")
    weight_strip = st.number_input("Weight Reading/Unit Strip (g)", value=0.0, step=0.01, key="weight_strip_input")
    weight_tablet = st.number_input("Weight Reading/Unit Tablet/Capsule (g)", value=0.0, step=0.01, key="weight_tablet_input")
    bulk_quantity = st.number_input("Bulk Quantity/No. of Units", value=0, step=1, key="bulk_quantity_input")

    # Buttons to "record" or "add" weights
    record_action = st.radio("Action", options=["Record", "Add"], key="record_action")

    # Submit button
    confirm = st.form_submit_button("Confirm")

    # Logic for Record/Add actions
    if confirm:
        if st.session_state.barcode and st.session_state.drug_name:
            if record_action == "Record":
                # Set weight values directly
                st.session_state.weight_box = weight_box
                st.session_state.weight_strip = weight_strip
                st.session_state.weight_tablet = weight_tablet
                st.session_state.bulk_quantity = bulk_quantity
            elif record_action == "Add":
                # Add to the existing values
                st.session_state.weight_box += weight_box
                st.session_state.weight_strip += weight_strip
                st.session_state.weight_tablet += weight_tablet
                st.session_state.bulk_quantity += bulk_quantity
            # Add row to DataFrame
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
