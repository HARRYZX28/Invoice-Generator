# Invoice Generator

A professional invoice generation system with both web and CLI interfaces, built for LIFTHUB PTY LTD. The application generates standardized invoices for transactions with key suppliers.

## Features

- **Dual Interface**: Web-based (Streamlit) and Command Line (CLI) options
- **Supplier Management**: Pre-configured with major suppliers:
  - Platinum Elevators Pty Ltd
  - Direct Lifts Australia
  - Savaria (Australia) Pty Ltd
- **Automated Calculations**:
  - 5% invoice amount calculation
  - 10% GST calculation
  - Automatic due date (6 days from invoice date)
- **Professional PDF Generation**:
  - Company logo integration
  - Standardized layout
  - Complete supplier details
  - Banking information
  - Project reference numbers

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd Invoice-Generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface
Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

### CLI Interface
Run the Python script directly:
```bash
python generate_invoice.py
```

## Project Structure

- `streamlit_app.py`: Web interface implementation
- `generate_invoice.py`: CLI implementation
- `logo/`: Directory containing company logos
- `invoices/`: Directory where generated invoices are saved

## Configuration

The application comes pre-configured with:
- Company details (LIFTHUB PTY LTD)
- Banking information
- Supplier details and addresses
- Standard calculation rates

## Dependencies

- Streamlit
- ReportLab
- Python 3.x

## Output

Generated invoices include:
- Company header with logo
- Complete supplier details
- Project information
- Itemized charges
- GST calculations
- Banking details
- Professional PDF formatting

## Deployment

This application can be deployed on:
- Streamlit Cloud (recommended)
- Any Python-compatible hosting service
- Local server

## License

Proprietary - All rights reserved 