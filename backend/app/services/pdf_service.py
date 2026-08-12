import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from app.models.invoice import Invoice

class PdfService:
    @staticmethod
    def generate_invoice_pdf(invoice: Invoice) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30,
        )

        elements = []
        styles = getSampleStyleSheet()
        
        # Header
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=16,
            alignment=1, # Center
            spaceAfter=20
        )
        
        doc_title = "TAX INVOICE"
        if invoice.invoice_status == "DRAFT":
            doc_title = "PROFORMA INVOICE / DRAFT"
        elif invoice.invoice_status == "CANCELLED":
            doc_title = "CANCELLED INVOICE"
            
        elements.append(Paragraph(doc_title, title_style))
        
        # Company & Customer Details
        header_data = [
            [
                Paragraph(f"<b>{invoice.seller_name_snapshot}</b><br/>"
                         f"{invoice.seller_address_snapshot}<br/>"
                         f"GSTIN: {invoice.seller_gstin_snapshot or 'N/A'}<br/>"
                         f"State: {invoice.seller_state_snapshot} ({invoice.seller_state_code_snapshot})", styles['Normal']),
                Paragraph(f"<b>Billed To:</b><br/>"
                         f"<b>{invoice.customer_name_snapshot}</b><br/>"
                         f"{invoice.customer_address_snapshot or ''}<br/>"
                         f"GSTIN: {invoice.customer_gstin_snapshot or 'N/A'}<br/>"
                         f"State: {invoice.customer_state_snapshot} ({invoice.customer_state_code_snapshot})<br/>"
                         f"Place of Supply: {invoice.place_of_supply}", styles['Normal'])
            ],
            [
                Paragraph(f"<b>Invoice Number:</b> {invoice.invoice_number}<br/>"
                         f"<b>Invoice Date:</b> {invoice.invoice_date.strftime('%d-%b-%Y')}", styles['Normal']),
                ""
            ]
        ]
        
        header_table = Table(header_data, colWidths=[270, 270])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('SPAN', (0, 1), (1, 1)),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 20))
        
        # Items Table
        items_data = [
            ['S.No', 'Description', 'HSN/SAC', 'Qty', 'Unit', 'Rate', 'GST %', 'Amount']
        ]
        
        for idx, line in enumerate(invoice.lines, 1):
            items_data.append([
                str(idx),
                Paragraph(line.item_name_snapshot, styles['Normal']),
                line.hsn_sac_snapshot or '-',
                str(line.quantity.normalize()),
                line.unit_symbol_snapshot or '-',
                f"{line.rate:.2f}",
                f"{line.gst_rate}%",
                f"{line.line_total:.2f}"
            ])
            
        items_table = Table(items_data, colWidths=[30, 150, 60, 50, 40, 60, 50, 90])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        
        elements.append(items_table)
        
        # Totals
        totals_data = [
            ['Subtotal:', f"{invoice.subtotal:.2f}"],
            ['Discount:', f"{invoice.discount_total:.2f}"],
            ['Taxable Value:', f"{invoice.taxable_total:.2f}"],
        ]
        
        if invoice.igst_total > 0:
            totals_data.append(['IGST:', f"{invoice.igst_total:.2f}"])
        else:
            totals_data.append(['CGST:', f"{invoice.cgst_total:.2f}"])
            totals_data.append(['SGST:', f"{invoice.sgst_total:.2f}"])
            
        totals_data.append(['Grand Total:', f"{invoice.grand_total:.2f}"])
        
        totals_table = Table(totals_data, colWidths=[400, 130])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('LINEBELOW', (0, -2), (-1, -2), 0.5, colors.grey),
            ('LINEABOVE', (0, -1), (-1, -1), 0.5, colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
            ('PADDING', (0, 0), (-1, -1), 4)
        ]))
        
        elements.append(totals_table)
        elements.append(Spacer(1, 20))
        
        # Amount in Words
        if invoice.amount_in_words:
            elements.append(Paragraph(f"<b>Amount in Words:</b> Rupees {invoice.amount_in_words}", styles['Normal']))
            
        if invoice.notes or invoice.terms:
            elements.append(Spacer(1, 20))
            if invoice.notes:
                elements.append(Paragraph(f"<b>Notes:</b><br/>{invoice.notes}", styles['Normal']))
                elements.append(Spacer(1, 10))
            if invoice.terms:
                elements.append(Paragraph(f"<b>Terms & Conditions:</b><br/>{invoice.terms}", styles['Normal']))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
