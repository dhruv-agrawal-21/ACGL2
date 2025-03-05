# This is a sample PDF generator module that you should adapt to your specific needs
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_vendor_pdf(rfq_response, output_path):
    """
    Generate a PDF document for a vendor based on RFQ response data.
    
    Args:
        rfq_response: The RFQResponse object containing data
        output_path: Path where the PDF will be saved
    """
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=18
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Sample styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    normal_style = styles['Normal']
    
    # Add title
    title = Paragraph(f"RFQ {rfq_response.rfq_number} Documentation", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Add vendor information
    elements.append(Paragraph(f"Vendor Code: {rfq_response.vendor_code}", normal_style))
    elements.append(Spacer(1, 12))
    
    # Add RFQ details
    elements.append(Paragraph("RFQ Details:", styles['Heading2']))
    elements.append(Spacer(1, 6))
    
    # Create table data - Customize this based on your actual RFQResponse model fields
    data = [
        ["Field", "Value"],
        ["RFQ Number", rfq_response.rfq_number],
        ["Vendor Code", rfq_response.vendor_code],
    ]
    
    # Add any additional fields from your RFQResponse model
    # These are example fields - replace with your actual model fields
    if hasattr(rfq_response, 'date'):
        data.append(["Date", rfq_response.date])
    if hasattr(rfq_response, 'status'):
        data.append(["Status", rfq_response.status])
    if hasattr(rfq_response, 'amount'):
        data.append(["Amount", f"${rfq_response.amount:.2f}"])
    if hasattr(rfq_response, 'description'):
        data.append(["Description", rfq_response.description])
    if hasattr(rfq_response, 'delivery_date'):
        data.append(["Delivery Date", rfq_response.delivery_date])
    
    # Create table
    table = Table(data, colWidths=[200, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 12))
    
    # Add terms and conditions or other information
    elements.append(Paragraph("Terms and Conditions:", styles['Heading2']))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("This document contains confidential information related to the RFQ. "
                              "Please review all details and respond accordingly.", normal_style))
    
    # Build the PDF
    doc.build(elements)