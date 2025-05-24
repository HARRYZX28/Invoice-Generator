#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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

def get_supplier_choice():
    while True:
        print("\nAvailable suppliers:")
        for key, supplier in SUPPLIERS.items():
            print(f"{key}. {supplier['name']}")
        
        try:
            choice = int(input("\nChoose a supplier (1-3): "))
            if choice in SUPPLIERS:
                return SUPPLIERS[choice]
            print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_project_number():
    return input("\nEnter project number: ")

def get_project_address():
    return input("\nEnter project address: ")

def get_contract_value():
    while True:
        try:
            value = float(input("\nEnter total contract value: $"))
            if value > 0:
                return value
            print("Please enter a positive value.")
        except ValueError:
            print("Invalid input. Please enter a number.")

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
    logo_path = "logo/Black logo.png"
    if os.path.exists(logo_path):
        img = Image(logo_path, width=2*inch, height=1*inch)
        header_data = [[img, Paragraph(f"{COMPANY_NAME}<br/>{COMPANY_ACN}<br/>{COMPANY_ADDRESS}<br/>{COMPANY_EMAIL}<br/>{COMPANY_PHONE}", company_style)]]
        header_table = Table(header_data, colWidths=[doc.width/2]*2)
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
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

def main():
    print("Welcome to the Invoice Generator!")
    
    supplier_details = get_supplier_choice()
    project_number = get_project_number()
    project_address = get_project_address()
    contract_value = get_contract_value()
    
    output_file = generate_invoice(supplier_details, project_number, project_address, contract_value)
    print(f"\nInvoice generated successfully: {output_file}")

if __name__ == "__main__":
    main() 