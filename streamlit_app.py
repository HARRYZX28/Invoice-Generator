import streamlit as st
import os
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import base64

# Company details
COMPANY_NAME = "LIFTHUB PTY LTD"
COMPANY_ACN = "ACN: 667592800"
COMPANY_ADDRESS = "120 Spencer Street, Melbourne, 3000"
COMPANY_EMAIL = "Email: info@lifthub.com.au"
COMPANY_PHONE = "Tel: +61422 099 979"

# Banking details
BANK_DETAILS = {
    "ACC Name": "LIFTHUB PTY LTD",
    "BSB": "033 - 002",
    "Account": "143 - 276"
}

# Define suppliers with full details
SUPPLIERS = {
    1: {
        "name": "Platinum Elevators Pty Ltd",
        "address": "Suite 19/2 Kirkham Rd W,\nKeysborough,\nVIC, 3173"
    },
    2: {
        "name": "Direct Lifts Australia",
        "address": "17 Military Road,\nBroadmeadows,\nVIC, 3047"
    },
    3: {
        "name": "Savaria (Australia) Pty Ltd",
        "address": "79 Crockford Street,\nNorthgate,\nQLD, 4013"
    }
}

def generate_invoice(supplier_details, project_number, project_address, contract_value):
    # Calculate values
    invoice_amount = contract_value * 0.05
    gst = invoice_amount * 0.10
    total = invoice_amount + gst

    # Get dates
    invoice_date = datetime.now()
    due_date = invoice_date + timedelta(days=6)

    # Create output directory if it doesn't exist
    os.makedirs('invoices', exist_ok=True)

    # Use project number for invoice number and filename
    invoice_number = project_number
    output_file = f"invoices/invoice_{invoice_number}.pdf"

    # Create PDF document
    doc = SimpleDocTemplate(output_file, pagesize=A4, 
                          rightMargin=25*mm, leftMargin=25*mm,
                          topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    story = []

    # Company Header
    company_style = ParagraphStyle(
        'Company',
        parent=styles['Normal'],
        fontSize=10,
        alignment=2  # Right alignment
    )
    
    # Add logo and company details in a table
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "logo", "Black logo.png")
    st.write(f"Debug - Looking for logo at: {logo_path}")
    
    if os.path.exists(logo_path):
        st.write("Debug - Logo file found!")
        try:
            img = Image(logo_path, width=2*inch, height=1*inch)
            company_details = Paragraph(f"{COMPANY_NAME}<br/>{COMPANY_ACN}<br/>{COMPANY_ADDRESS}<br/>{COMPANY_EMAIL}<br/>{COMPANY_PHONE}", company_style)
            header_data = [[img, company_details]]
            header_table = Table(header_data, colWidths=[doc.width/2]*2)
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (0, 0), 0),
                ('RIGHTPADDING', (1, 0), (1, 0), 0),
            ]))
            story.append(header_table)
            story.append(Spacer(1, 20))
            st.write("Debug - Header table added to PDF")
        except Exception as e:
            st.error(f"Error adding logo to PDF: {str(e)}")
    else:
        st.write(f"Debug - Logo file not found at: {logo_path}")
        # Add company details without logo as fallback
        company_details = Paragraph(f"{COMPANY_NAME}<br/>{COMPANY_ACN}<br/>{COMPANY_ADDRESS}<br/>{COMPANY_EMAIL}<br/>{COMPANY_PHONE}", company_style)
        header_table = Table([[company_details]], colWidths=[doc.width])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 20))

    # Add "INVOICE" title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=40,
        textColor=colors.salmon,
        spaceAfter=30
    )
    story.append(Paragraph("INVOICE", title_style))
    story.append(Spacer(1, 20))

    # Create a style for the address with line breaks
    address_style = ParagraphStyle(
        'Address',
        parent=styles['Normal'],
        fontSize=10,
        leading=12  # Adjust line spacing for the address
    )

    # Invoice details section with formatted address
    invoice_details = [
        ['Invoice No:', invoice_number, 'Invoice Date:', invoice_date.strftime('%d %b, %Y').upper()],
        ['Bill to:', Paragraph(f"{supplier_details['name']}<br/>{supplier_details['address']}", address_style), 'Due Date:', due_date.strftime('%d %b, %Y').upper()]
    ]
    
    t = Table(invoice_details, colWidths=[doc.width/6, doc.width/3, doc.width/6, doc.width/3])
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    # Items table
    items_data = [
        ['Item', 'Description', 'Tax', 'Amount'],
        ['1.', 'Sales & Marketing Activities', 'Total without GST', f'${invoice_amount:.2f}'],
        ['', f'Job Reference: {invoice_number}', 'GST', f'${gst:.2f}'],
        ['', '', 'Total with GST', f'${total:.2f}'],
        ['', f'Project Address: {project_address}', '', '']
    ]

    items_table = Table(items_data, colWidths=[doc.width/8, doc.width/2, doc.width/6, doc.width/6])
    items_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ('ALIGN', (-2, -1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 20))

    # Invoice Total
    total_table = Table([['Invoice Total', f'${total:.2f}']], 
                       colWidths=[doc.width*0.8, doc.width*0.2])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
    ]))
    story.append(total_table)
    story.append(Spacer(1, 20))

    # Add "Pay To:" title
    pay_to_style = ParagraphStyle(
        'PayTo',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Helvetica-Bold'
    )
    story.append(Paragraph("Pay To:", pay_to_style))
    story.append(Spacer(1, 5))

    # Banking details
    banking_data = [[f"{k}:", v] for k, v in BANK_DETAILS.items()]
    banking_data.append(['Reference:', invoice_number])  # Add Reference as last item
    banking_table = Table(banking_data, colWidths=[doc.width/6, doc.width*5/6])
    banking_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(banking_table)

    # Build PDF
    doc.build(story)
    
    return output_file

def get_pdf_download_link(file_path):
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except Exception as e:
        st.error(f"Error reading PDF file: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="Invoice Generator",
        layout="centered",
        menu_items={
            'About': "LIFTHUB PTY LTD Invoice Generator"
        }
    )
    
    # Add Open Graph meta tags for better social sharing
    st.markdown("""
        <head>
            <meta property="og:title" content="LIFTHUB Invoice Generator">
            <meta property="og:description" content="Generate professional invoices for LIFTHUB PTY LTD">
            <meta property="og:type" content="website">
        </head>
    """, unsafe_allow_html=True)
    
    # Create two columns for logo and company details
    col1, col2 = st.columns(2)
    
    # Column 1: Logo
    with col1:
        if os.path.exists("logo/White Logo.png"):
            st.image("logo/White Logo.png", width=200)
    
    # Column 2: Company Details
    with col2:
        st.markdown(f"""
        ### {COMPANY_NAME}
        {COMPANY_ACN}  
        {COMPANY_ADDRESS}  
        {COMPANY_EMAIL}  
        {COMPANY_PHONE}
        """)
    
    st.title("Invoice Generator")
    
    # Form for input
    with st.form("invoice_form"):
        # Current date information
        current_date = datetime.now()
        due_date = current_date + timedelta(days=6)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Invoice Date:**", current_date.strftime('%d %b, %Y').upper())
        with col2:
            st.write("**Due Date:**", due_date.strftime('%d %b, %Y').upper())
        
        # Supplier selection - show only names
        supplier_names = [supplier["name"] for supplier in SUPPLIERS.values()]
        selected_supplier_name = st.selectbox(
            "Select Supplier",
            options=supplier_names,
            index=0
        )
        
        # Find the selected supplier details (but don't display them)
        selected_supplier = next(
            supplier for supplier in SUPPLIERS.values() 
            if supplier["name"] == selected_supplier_name
        )

        # Project number input
        project_number = st.text_input(
            "Project Number",
            placeholder="Enter project number (This will be used as the Invoice No.)"
        )

        # Project address input
        project_address = st.text_input(
            "Project Address",
            placeholder="Enter project address"
        )
        
        # Contract value input
        contract_value = st.number_input(
            "Contract Value ($)",
            min_value=0.01,
            value=1000.00,
            step=100.00,
            format="%.2f"
        )
        
        # Submit button
        submitted = st.form_submit_button("Generate Invoice")

    # Handle form submission outside the form
    if submitted:
        if not project_number:
            st.error("Please enter a project number.")
        elif not project_address:
            st.error("Please enter a project address.")
        else:
            try:
                # Generate invoice
                output_file = generate_invoice(selected_supplier, project_number, project_address, contract_value)
                
                # Show success message
                st.success(f"Invoice {project_number} generated successfully!")
                
                # Display calculations
                st.write("### Invoice Summary")
                invoice_amount = contract_value * 0.05
                gst = invoice_amount * 0.10
                total = invoice_amount + gst
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Total without GST:")
                    st.write("GST (10%):")
                    st.write("**Total with GST:**")
                with col2:
                    st.write(f"${invoice_amount:.2f}")
                    st.write(f"${gst:.2f}")
                    st.write(f"**${total:.2f}**")
                
                # Add download button outside the form
                pdf_data = get_pdf_download_link(output_file)
                if pdf_data is not None:
                    st.download_button(
                        label="Download PDF",
                        data=pdf_data,
                        file_name=os.path.basename(output_file),
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error generating invoice: {str(e)}")

if __name__ == "__main__":
    main() 