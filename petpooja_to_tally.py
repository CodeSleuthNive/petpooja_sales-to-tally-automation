# app.py
import streamlit as st
import pandas as pd
import io

def rename_restaurant(name):
    mapping = {
        'Snacks Hub Chennai': 'Chennai',
        'Snacks Hub Banglore': 'Banglore',
        'Snacks Hub Mumbai': 'Mumbai',
        'Snacks Hub Kerala': 'Kerala',
    }
    new_name = mapping.get(name.strip())  
    if new_name:
        return new_name
    else:
        st.warning(f"Unexpected restaurant name found: {name}")
        return name  

def process_data(df):
    df['date'] = df['date'].str[:10]
    df['date'] = pd.to_datetime(df['date'], dayfirst=True).dt.date
    df['restaurant_name'] = df['restaurant_name'].apply(rename_restaurant)

    price_mapping = {
        "Egg Puff": 27.62,
        "Pani Puri": 18.10,
        "Veg Sandwich": 28.10,
        "Chicken Sandwich":48.10,
        "Dahi Puri":38.10,
        "Samosa": 23.81,
        "Vada Paav": 38.10,
    }

    def modify_invoice_no(row):
        abbrev = ''.join(word[0].upper() for word in row['restaurant_name'].split())  
        return f"{abbrev}{str(row['invoice_no']).capitalize()}"

    df['modified_invoice_no'] = df.apply(modify_invoice_no, axis=1)
    df['modified_invoice_no'] = pd.Categorical(df['modified_invoice_no'], categories=df['modified_invoice_no'].unique(), ordered=True)

    grouped = df.groupby('modified_invoice_no')

    data = []
    for invoice_no, group in grouped:
        first_row = group.iloc[0]
        date = first_row['date']
        restaurant_name = first_row['restaurant_name']
        order_type = first_row['order_type']
        payment_type = first_row['payment_type']
        discount = first_row['discount']
        container_charge = first_row['container_charge']
        service_charge = first_row['service_charge']
        additional_charge = first_row['additional_charge']
        delivery_charge = first_row['delivery_charge']
        status = first_row['status']
        customer_name = first_row['customer_name']

        voucher_type = "Dine In" if order_type in ["Dine In", "Pick Up"] else "Online Sales"

        if voucher_type in ["Dine In", "Pick Up"]:
            if payment_type == "Cash":
                first_row_ledger_name = "Cash"
            elif payment_type == "CARD":
                first_row_ledger_name = "Card Sales"
            elif payment_type == "Other [UPI]":
                first_row_ledger_name = "UPI Sales"
            elif payment_type == "Due Payment":
                first_row_ledger_name = customer_name if customer_name else "Due Payment"
            elif payment_type == "Part Payment":
                first_row_ledger_name = customer_name if customer_name else "Part Payment"
            else:
                first_row_ledger_name = payment_type
        else:
            if payment_type in ["Zomato", "Swiggy"]:
                first_row_ledger_name = payment_type
            else:
                first_row_ledger_name = payment_type

        ledger_name = "Online Sales" if voucher_type == "Online Sales" else "Sales"

        # Set state according to restaurant
        state_mapping = {
            'Chennai': 'Tamil Nadu',
            'Banglore': 'Karnataka',
            'Mumbai': 'Maharashtra',
            'Kerala': 'Kerala'
        }
        state = state_mapping.get(restaurant_name, 'Tamil Nadu')  # Default to Tamil Nadu

        item_total_sum = sum(row['item_quantity'] * price_mapping.get(row['item_name'], row['item_price']) for _, row in group.iterrows())

        if voucher_type == "Dine In":
            tax_amount = round((item_total_sum * 0.025), 2)
            total_amount = item_total_sum + (2 * tax_amount) + additional_charge + service_charge + container_charge + delivery_charge - discount
        else:
            tax_amount = 0
            total_amount = item_total_sum + additional_charge + service_charge + container_charge + delivery_charge - discount

        change_mode = "Item Invoice" if status == "Success" else "Cancelled"

        data.append([
            date, voucher_type, invoice_no, restaurant_name, 'India', state, 'Unregistered/Consumer',
            state, restaurant_name, 'India', state, first_row_ledger_name,
            total_amount if status == "Success" else '', 'Dr' if status == "Success" else '', '', '', '', '', '', change_mode, restaurant_name
        ])

        if status == "Success":
            first_item = True
            sales_total = item_total_sum
            for index, row in group.iterrows():
                item_name = row['item_name']
                item_quantity = row['item_quantity']

                mapped_price = price_mapping.get(item_name, row['item_price'])

                item_total = item_quantity * mapped_price

                if first_item:
                    data.append(['', '', '', '', '', '', '', '', '', '', '', ledger_name, sales_total, 'Cr',
                                 item_name, item_quantity, mapped_price, 'Nos', item_total, '', ''])
                    first_item = False
                else:
                    data.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '',
                                 item_name, item_quantity, mapped_price, 'Nos', item_total, '', ''])

            if voucher_type == "Dine In":
                data.append(['', '', '', '', '', '', '', '', '', '', '', 'CGST', tax_amount, 'Cr', '', '', '', '', '', '', ''])
                data.append(['', '', '', '', '', '', '', '', '', '', '', 'SGST', tax_amount, 'Cr', '', '', '', '', '', '', ''])

            if discount > 0:
                data.append(['', '', '', '', '', '', '', '', '', '', '', 'Discount on Sales', discount, 'Cr', '', '', '', '', '', '', ''])
            if container_charge > 0:
                data.append(['', '', '', '', '', '', '', '', '', '', '', 'Packing Charges', container_charge, 'Cr', '', '', '', '', '', '', ''])
            if service_charge > 0:
                data.append(['', '', '', '', '', '', '', '', '', '', '', 'Service Charge', service_charge, 'Cr', '', '', '', '', '', '', ''])
            if additional_charge > 0:
                data.append(['', '', '', '', '', '', '', '', '', '', '', 'Additional Charge', additional_charge, 'Cr', '', '', '', '', '', '', ''])
            if delivery_charge > 0:
                data.append(['', '', '', '', '', '', '', '', '', '', '', 'Delivery Charge', delivery_charge, 'Cr', '', '', '', '', '', '', ''])

    columns = [
        'Voucher Date', 'Voucher Type Name', 'Voucher Number', 'Buyer/Supplier - Address', 'Buyer/Supplier - Country', 
        'Buyer/Supplier - State', 'Buyer/Supplier - GST Registration Type', 'Buyer/Supplier - Place of Supply', 
        'Consignee - Address', 'Consignee - Country', 'Consignee - State', 
        'Ledger Name', 'Ledger Amount', 'Ledger Amount Dr/Cr',
        'Item Name', 'Billed Quantity', 'Item Rate', 'Item Rate per', 'Item Amount', 'Change Mode', 'Cost Centre/Classes'
    ]

    result_df = pd.DataFrame(data, columns=columns)
    return result_df

st.title("Petpooja data to tally converter file (Sales)")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    result_df = process_data(df)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        result_df.to_excel(writer, index=False)
    st.download_button(
        label="Download Excel file",
        data=buffer,
        file_name="processed_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
