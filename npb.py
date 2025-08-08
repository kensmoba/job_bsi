from reportlab.lib.pagesizes import A3
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128

def generate_npb_labels(start=0, end=19, prefix="B09925", output_file="label_npb_fixed.pdf", header_img_path="static/header.png"):
    c = canvas.Canvas(output_file, pagesize=A3)
    width, height = A3

    label_width = 60 * mm
    label_height = 90 * mm

    cols = 5
    rows = 4

    margin_x = 10 * mm
    margin_y = 10 * mm

    total_width = cols * label_width
    total_height = rows * label_height

    start_x = (width - total_width) / 2
    start_y = height - margin_y - label_height

    # Nomor halaman
    c.setFillColorRGB(1, 0, 0)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(margin_x, height - margin_y + 2 * mm, "1")

    i = 0
    for num in range(start, end + 1):
        row = (i // cols) % rows
        col = i % cols

        x = start_x + col * label_width
        y = start_y - row * label_height

        barcode_value = f"{prefix}{num:04d}"

        # Bingkai label
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(0.5)
        c.rect(x, y, label_width, label_height)

        # Header/logo
        img_width = 52 * mm
        img_height = 16 * mm
        img_x = x + (label_width - img_width) / 2
        img_y = y + label_height - img_height - 6 * mm
        c.drawImage(header_img_path, img_x, img_y, width=img_width, height=img_height, preserveAspectRatio=True)

        # Teks "NPB"
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(x + label_width / 2, y + 52 * mm, "NPB")

        # Barcode
        barcode = code128.Code128(barcode_value, barHeight=26 * mm, barWidth=0.35 * mm)
        barcode_x = x + (label_width - barcode.width) / 2
        barcode_y = y + 22 * mm
        barcode.drawOn(c, barcode_x, barcode_y)

        # Teks barcode
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(x + label_width / 2, y + 14 * mm, barcode_value)

        i += 1

        # Ganti halaman jika penuh
        if i % (cols * rows) == 0 and num != end:
            c.showPage()
            c.setFillColorRGB(1, 0, 0)
            c.setFont("Helvetica-Bold", 17)
            c.drawString(margin_x, height - margin_y + 2 * mm, str(1 + i // (cols * rows)))

    c.save()
    print(f"✅ PDF NPB berhasil dibuat: {output_file}")
