# petpooja_sales-to-tally-automation

This Streamlit app converts Petpooja restaurant sales data (CSV) into a Tally-compatible Excel file for easy accounting and GST filing.

🚀 Features
Rename and standardize restaurant names.

Modify invoice numbers to avoid duplication.

Auto-map item prices (based on menu mapping).

Calculate taxes, discounts, service charges, container charges, and delivery fees.

Separate handling of "Success" and "Cancelled" orders.

Generate a ready-to-import Excel sheet for Tally.

## 📂 Input CSV Format
Your CSV must have these columns:


Column Name	Description
date	Order date (e.g., 25-04-2025)
restaurant_name	Restaurant branch name
invoice_no	Invoice number
order_type	Order type (Dine In, Pick Up, Online)
payment_type	Payment method (Cash, Card, UPI, etc.)
item_name	Name of the item sold
item_quantity	Quantity sold
item_price	Selling price (if price not mapped)
discount	Discount amount
container_charge	Packing/container charge
service_charge	Service charge (if any)
additional_charge	Other charges
delivery_charge	Delivery fee
status	Order status (Success/Cancelled)
customer_name	Customer name (for Due/Part Payment)


## 📄 Output Excel Format
The generated Excel file contains:


Column	Description
Voucher Date	Sale date
Voucher Type Name	"Dine In" or "Online Sales"
Voucher Number	Modified invoice number
Buyer/Supplier - Address	Restaurant name
Buyer/Supplier - Country	India
Buyer/Supplier - State	Tamil Nadu, Karnataka, etc.
Buyer/Supplier - GST Registration Type	Unregistered/Consumer
Buyer/Supplier - Place of Supply	State
Consignee - Address	Restaurant name
Consignee - Country	India
Consignee - State	State
Ledger Name	Cash, Card Sales, Swiggy, Zomato, etc.
Ledger Amount	Total invoice amount
Ledger Amount Dr/Cr	Dr for Sales
Item Name	Name of item sold
Billed Quantity	Quantity sold
Item Rate	Unit price
Item Rate per	Nos
Item Amount	Line total
Change Mode	Item Invoice / Cancelled
Cost Centre/Classes	Restaurant name
🛠️ How to Run Locally
Clone this repository:

bash
Copy
Edit
git clone https://github.com/your-username/petpooja-tally-converter.git
cd petpooja-tally-converter
Install dependencies:

bash
Copy
Edit
pip install streamlit pandas xlsxwriter
Run the app:

bash
Copy
Edit
streamlit run app.py
Upload your Petpooja CSV and download the processed Tally Excel file!

## ✨ Notes
Price Mapping: If the item_name is in predefined mapping (like Egg Puff, Pani Puri), it uses fixed prices.

Taxes: For Dine In orders, 2.5% CGST + 2.5% SGST are calculated.

Cancelled Orders: Marked clearly with "Cancelled" mode in output.

Error Handling: Unexpected restaurant names will trigger a warning.

📧 Contact
For improvements, issues, or queries, feel free to open an issue or contribute!
