import qrcode
import barcode
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from reportlab.lib.units import mm
from reportlab.lib import colors
import os
import tempfile

def generate_labels(start=1, end=10, prefix="D", output_file="static/output.pdf"):
    with tempfile.TemporaryDirectory() as temp_dir:
        c = canvas.Canvas(output_file, pagesize=A3)
        page_width, page_height = A3

        cols = 8
        rows = 10
        label_w = (page_width - 2 * 10 * mm) / cols
        label_h = (page_height - 2 * 10 * mm) / rows
        margin_x = 10 * mm
        margin_y = 10 * mm

        i = 0
        page_num = 1

        c.setFillColor(colors.red)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(10 * mm, page_height - 5 * mm, f"HALAMAN {page_num}")
        c.setFillColor(colors.black)

        for num in range(start, end + 1):
            code = f"{prefix}{num:06d}"

            qr = qrcode.make(code)
            qr_path = os.path.join(temp_dir, f"qr_{code}.png")
            qr.save(qr_path)

            CODE128 = barcode.get_barcode_class('code128')
            bc = CODE128(code, writer=ImageWriter())
            bc_path = os.path.join(temp_dir, f"bc_{code}.png")
            with open(bc_path, "wb") as f:
                bc.write(f, {"write_text": False, "dpi": 300})

            if i != 0 and i % (cols * rows) == 0:
                page_num += 1
                c.showPage()
                c.setFillColor(colors.red)
                c.setFont("Helvetica-Bold", 14)
                c.drawString(10 * mm, page_height - 5 * mm, f"HALAMAN {page_num}")
                c.setFillColor(colors.black)

            col = i % cols
            row = (i // cols) % rows

            label_x = margin_x + col * label_w
            label_y = page_height - margin_y - (row + 1) * label_h

            qr_size = label_h * 0.62
            barcode_h = label_h / 5
            barcode_w = label_w * 0.8
            spacing = 0.5 * mm
            total_height = barcode_h + spacing + qr_size
            center_y = label_y + (label_h - total_height) / 2
            barcode_x = label_x + (label_w - barcode_w) / 2
            barcode_y = center_y + qr_size + spacing
            qr_x = label_x + (label_w - qr_size) / 1.5
            qr_y = center_y

            frame_margin = 1 * mm
            corner_radius = 2 * mm
            c.setLineWidth(0.6)
            c.roundRect(
                label_x + frame_margin,
                label_y + frame_margin,
                label_w - 2 * frame_margin,
                label_h - 2 * frame_margin,
                corner_radius)

            c.drawImage(bc_path, barcode_x, barcode_y, width=barcode_w, height=barcode_h, preserveAspectRatio=False, mask='auto')
            c.drawImage(qr_path, qr_x, qr_y, width=qr_size, height=qr_size, preserveAspectRatio=True, mask='auto')

            text_x = qr_x + qr_size / 10.75
            text_y = qr_y + qr_size / 2
            c.saveState()
            c.translate(text_x, text_y)
            c.rotate(90)
            c.setFont("Helvetica-Bold", 13)
            c.drawCentredString(0, 0, code)
            c.restoreState()

            i += 1

        c.save()
