import os
import datetime
from typing import Dict, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from app.config import REPORTS_DIR

class PDFReportService:
    """
    Generates official Government of India style Legal Metrology Inspection Reports in PDF format.
    """

    @classmethod
    def generate_inspection_pdf(cls, inspection_data: Dict[str, Any]) -> str:
        inspection_num = inspection_data.get("inspection_number", "INSP-0000")
        pdf_filename = f"Inspection_Report_{inspection_num}.pdf"
        pdf_path = REPORTS_DIR / pdf_filename

        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Custom styles
        header_style = ParagraphStyle(
            'GovHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            alignment=1, # Center
            textColor=colors.HexColor('#0F172A')
        )
        
        sub_header_style = ParagraphStyle(
            'GovSubHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            alignment=1,
            textColor=colors.HexColor('#1E3A8A')
        )
        
        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=colors.HexColor('#1E3A8A'),
            spaceBefore=10,
            spaceAfter=6
        )
        
        body_style = ParagraphStyle(
            'GovBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#334155')
        )

        table_header_style = ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            textColor=colors.white
        )

        table_cell_style = ParagraphStyle(
            'TableCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor('#1E293B')
        )

        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor('#64748B'),
            alignment=1
        )

        story = []

        # 1. Government Department Header
        story.append(Paragraph("GOVERNMENT OF INDIA", header_style))
        story.append(Paragraph("MINISTRY OF CONSUMER AFFAIRS, FOOD & PUBLIC DISTRIBUTION", sub_header_style))
        story.append(Paragraph("DEPARTMENT OF CONSUMER AFFAIRS — LEGAL METROLOGY DIVISION", ParagraphStyle(
            'DeptTitle', parent=sub_header_style, fontSize=10, leading=14, textColor=colors.HexColor('#475569')
        )))
        story.append(Spacer(1, 4))
        story.append(Paragraph("LEGAL METROLOGY (PACKAGED COMMODITIES) RULES, 2011 — COMPLIANCE INSPECTION REPORT", ParagraphStyle(
            'ReportTitle', parent=header_style, fontSize=11, leading=15, textColor=colors.HexColor('#0F766E')
        )))
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceBefore=2, spaceAfter=8))

        # 2. Meta Information & Status Badge Table
        status = inspection_data.get("compliance_status", "PENDING")
        score = inspection_data.get("compliance_score", 0.0)
        
        status_color = colors.HexColor('#059669') if status == "COMPLIANT" else (colors.HexColor('#DC2626') if status == "NON-COMPLIANT" else colors.HexColor('#D97706'))

        meta_table_data = [
            [
                Paragraph(f"<b>Inspection ID:</b> {inspection_num}", body_style),
                Paragraph(f"<b>Inspection Date:</b> {inspection_data.get('inspection_date', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}", body_style),
            ],
            [
                Paragraph(f"<b>Inspecting Officer ID:</b> {inspection_data.get('officer_id', 'LMO001')}", body_style),
                Paragraph(f"<b>Officer Name:</b> {inspection_data.get('officer_name', 'Inspector R. Sharma')}", body_style),
            ],
            [
                Paragraph(f"<b>Product Name:</b> {inspection_data.get('product_name', 'Packaged Commodity')}", body_style),
                Paragraph(f"<b>Category:</b> {inspection_data.get('category', 'Food & Grocery')}", body_style),
            ],
            [
                Paragraph(f"<b>Manufacturer / Packer:</b> {inspection_data.get('manufacturer', 'Declared on Package')}", body_style),
                Paragraph(f"<b>Overall Compliance Score:</b> <b><font color='{status_color.hexval()}'>{score}/100 ({status})</font></b>", body_style),
            ]
        ]
        
        meta_table = Table(meta_table_data, colWidths=[260, 260])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 10))

        # 3. Score Breakdown
        breakdown = inspection_data.get("score_breakdown", {})
        if breakdown:
            breakdown_data = [
                [
                    Paragraph(f"<b>Mandatory Declarations:</b> {breakdown.get('mandatory_declarations', 100)}%", body_style),
                    Paragraph(f"<b>Quantity Unit Compliance:</b> {breakdown.get('quantity_declaration', 100)}%", body_style),
                    Paragraph(f"<b>MRP Declaration:</b> {breakdown.get('mrp_compliance', 100)}%", body_style),
                ],
                [
                    Paragraph(f"<b>Consumer Care Cell:</b> {breakdown.get('consumer_care', 100)}%", body_style),
                    Paragraph(f"<b>Readability / Formatting:</b> {breakdown.get('readability_formatting', 100)}%", body_style),
                    Paragraph(f"<b>Status:</b> <b>{status}</b>", body_style),
                ]
            ]
            breakdown_table = Table(breakdown_data, colWidths=[173, 173, 174])
            breakdown_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EFF6FF')),
                ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#BFDBFE')),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DBEAFE')),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(breakdown_table)
            story.append(Spacer(1, 10))

        # 4. Mandatory Declarations Extraction Table
        story.append(Paragraph("1. Extracted Package Declarations (Rule 6 Analysis)", section_title_style))
        declarations = inspection_data.get("declarations", [])
        
        dec_table_rows = [
            [
                Paragraph("<b>Mandatory Declaration</b>", table_header_style),
                Paragraph("<b>Detected Package Value</b>", table_header_style),
                Paragraph("<b>Status</b>", table_header_style),
                Paragraph("<b>Confidence</b>", table_header_style),
                Paragraph("<b>Est. Font / Readability</b>", table_header_style),
            ]
        ]

        for d in declarations:
            val = d.get("detected_value") or "Not Detected / Missing"
            is_pres = d.get("is_present", True) and "missing" not in val.lower()
            dec_status = "Compliant" if is_pres else "Violation"
            st_color = "#059669" if is_pres else "#DC2626"
            conf = f"{d.get('confidence', 0.95)*100:.0f}%"
            font_est = f"{d.get('estimated_font_size_px', 14):.0f}px ({d.get('readability_status', 'PASS')})"

            dec_table_rows.append([
                Paragraph(f"<b>{d.get('field_name', '').replace('_', ' ').title()}</b>", table_cell_style),
                Paragraph(val, table_cell_style),
                Paragraph(f"<font color='{st_color}'><b>{dec_status}</b></font>", table_cell_style),
                Paragraph(conf, table_cell_style),
                Paragraph(font_est, table_cell_style),
            ])

        dec_table = Table(dec_table_rows, colWidths=[120, 190, 70, 60, 80])
        dec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(dec_table)
        story.append(Spacer(1, 10))

        # 5. Detected Violations Table
        story.append(Paragraph("2. Detected Violations & Non-Compliance Findings", section_title_style))
        violations = inspection_data.get("violations", [])

        if not violations:
            story.append(Paragraph("<b>No violations detected. Product meets all scanned Legal Metrology mandatory declarations.</b>", ParagraphStyle(
                'NoViol', parent=body_style, textColor=colors.HexColor('#059669'), fontName='Helvetica-Bold'
            )))
        else:
            viol_rows = [
                [
                    Paragraph("<b>Rule Reference</b>", table_header_style),
                    Paragraph("<b>Category</b>", table_header_style),
                    Paragraph("<b>Issue & Detected Observation</b>", table_header_style),
                    Paragraph("<b>Severity</b>", table_header_style),
                    Paragraph("<b>Expected Legal Requirement</b>", table_header_style),
                ]
            ]
            for v in violations:
                sev = v.get("severity", "HIGH")
                sev_color = "#DC2626" if sev in ["CRITICAL", "HIGH"] else "#D97706"
                viol_rows.append([
                    Paragraph(f"<b>{v.get('rule_code', 'LM-PC')}</b><br/><font size='7' color='#475569'>{v.get('legal_reference', 'Legal Metrology Rules 2011')}</font>", table_cell_style),
                    Paragraph(v.get("category", "General"), table_cell_style),
                    Paragraph(f"<b>Issue:</b> {v.get('issue', '')}<br/><b>Detected:</b> {v.get('detected_value', 'N/A')}", table_cell_style),
                    Paragraph(f"<font color='{sev_color}'><b>{sev}</b></font>", table_cell_style),
                    Paragraph(v.get("expected_requirement", ""), table_cell_style),
                ])

            viol_table = Table(viol_rows, colWidths=[100, 95, 145, 60, 120])
            viol_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#991B1B')),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FEF2F2')]),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ]))
            story.append(viol_table)

        story.append(Spacer(1, 12))

        # 6. Officer Remarks & Signature Block
        story.append(KeepTogether([
            Paragraph("3. Officer Verification & Remarks", section_title_style),
            Paragraph(f"<b>Officer Notes:</b> {inspection_data.get('remarks') or 'Inspection conducted as per Legal Metrology (Packaged Commodities) Rules, 2011. Evidence verified.'}", body_style),
            Spacer(1, 15),
            Table([
                [
                    Paragraph("<b>Digitally Verified By:</b><br/>Legal Metrology Inspection Cell<br/>Government of India", body_style),
                    Paragraph("<b>Officer Seal & Signature:</b><br/>__________________________<br/>Authorised Enforcement Officer", body_style)
                ]
            ], colWidths=[260, 260]),
            Spacer(1, 10),
            HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#94A3B8'), spaceBefore=4, spaceAfter=6),
            Paragraph(
                "DISCLAIMER: This document is generated by an AI-assisted Legal Metrology compliance screening prototype for SIH 2026 (SIH26034). "
                "The findings are advisory and intended to assist authorized enforcement officers. Final legal determination and compounding/prosecution rests solely with the competent authority under the Legal Metrology Act, 2009.",
                disclaimer_style
            )
        ]))

        doc.build(story)
        return str(pdf_path)
