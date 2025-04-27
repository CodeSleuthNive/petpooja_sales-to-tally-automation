
# Petpooja to Tally Converter

## Overview
The **Petpooja to Tally Converter** is a Streamlit-based web application that allows users to upload Petpooja sales CSV files and download Tally-compatible Excel sheets.  
This tool simplifies the accounting process for restaurants by formatting raw Petpooja data to match Tally’s import structure.

---

## Features

- **CSV Upload**: Upload Petpooja sales `.csv` files.
- **Automated Formatting**: Convert Petpooja data into a Tally-friendly Excel format.
- **Error Handling**: Validate file structure and alert for missing or incorrect data.
- **Multi-Order Type Support**: Handles Dine In, Pick Up, Online orders.
- **Downloadable Excel Output**: Generate and download a clean, ready-to-import `.xlsx` file.

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/petpooja-tally-converter.git
   cd petpooja-tally-converter
   ```

2. **Set Up Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. Open the app in your browser (usually [http://localhost:8501](http://localhost:8501)).
2. Upload your Petpooja `.csv` sales report.
3. The app will validate the CSV structure.
4. Download the processed Tally-formatted Excel file.

---

## Input CSV Format

The uploaded CSV must contain the following columns:

| Column Name         | Description |
|---------------------|-------------|
| `date`              | Order date (e.g., 25-04-2025) |
| `restaurant_name`    | Restaurant branch name |
| `invoice_no`         | Invoice number |
| `order_type`         | Order type (Dine In, Pick Up, Online) |
| `payment_type`       | Payment method (Cash, Card, UPI, etc.) |
| `item_name`          | Name of the item sold |
| `item_quantity`      | Quantity sold |
| `item_price`         | Selling price (if not mapped) |
| `discount`           | Discount amount |
| `container_charge`   | Packing/container charge |
| `service_charge`     | Service charge (if any) |
| `additional_charge`  | Other additional charges |
| `delivery_charge`    | Delivery fee |
| `status`             | Order status (Success/Cancelled) |
| `customer_name`      | Customer name (for Due/Part Payment orders) |

---

## Output Excel Format

The generated Excel file will include:

| Column | Description |
|--------|-------------|
| Voucher Date | Sale date |
| Voucher Type Name | "Dine In" or "Online Sales" |
| Voucher Number | Modified invoice number |
| Buyer/Supplier - Address | Restaurant name |
| Buyer/Supplier - Country | India |
| Buyer/Supplier - State | Tamil Nadu, Karnataka, etc. |
| Buyer/Supplier - GST Registration Type | Unregistered/Consumer |
| Buyer/Supplier - Place of Supply | State |
| Consignee - Address | Restaurant name |
| Consignee - Country | India |
| Consignee - State | State |
| Ledger Name | Cash, Card Sales, Swiggy, Zomato, etc. |
| Ledger Amount | Total invoice amount |
| Ledger Amount Dr/Cr | Dr for Sales |
| Item Name | Name of item sold |
| Billed Quantity | Quantity sold |
| Item Rate | Unit price |
| Item Rate per | Nos |
| Item Amount | Line total |
| Change Mode | Item Invoice / Cancelled |
| Cost Centre/Classes | Restaurant name |

---

## File Structure

```plaintext
petpooja-tally-converter/
├── app.py                  # Main Streamlit app
├── processor.py            # Core logic for CSV to Excel conversion (optional if separated)
├── requirements.txt        # Python dependencies
├── README.md                # Project documentation
└── sample_input.csv         # Sample Petpooja CSV (optional for users)
```

---

## Dependencies

- **Streamlit**: For building the web interface.
- **Pandas**: For CSV data processing.
- **XlsxWriter**: For creating formatted Excel files.

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Troubleshooting

1. **Incorrect Columns Error**
   - Ensure your uploaded CSV matches the expected column names exactly.

2. **Excel Download Issues**
   - Try re-uploading the file or checking if mandatory fields are missing.

3. **Streamlit App Not Loading**
   - Ensure all libraries are installed.
   - Check your Python version (recommended Python 3.8+).

---

## Future Enhancements

- Add multi-branch handling for large restaurant chains.
- Allow partial uploads (skip cancelled orders automatically).
- Add GST calculation modules.
- Enable customization of Tally voucher templates.

---

## Contributing

Contributions are welcome!  
If you'd like to improve this tool, fork the repository and submit a pull request.  
Please ensure your changes are well-documented.

---

## Acknowledgments

- [Streamlit](https://streamlit.io/) for providing an awesome tool to build quick web apps.
- [Petpooja](https://www.petpooja.com/) for their POS ecosystem.
- Open-source libraries and contributors.
