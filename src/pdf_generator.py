# src/pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import tempfile
import textwrap
import os

# Register basic clean font (optional)
#pdfmetrics.registerFont(TTFont('Helvetica', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
FONT_PATH = os.path.join(os.path.dirname(__file__), "../fonts/DejaVuSans.ttf")
pdfmetrics.registerFont(TTFont("DejaVu", FONT_PATH))

def generate_resume_pdf(text: str):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    filename = temp.name
    temp.close()

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Clean Typography Settings
    left_margin = 40
    top_margin = height - 60
    line_height = 16
    max_chars_per_line = 95

    y = top_margin

    # Detect section headings (simple rule)
    def is_heading(line):
        return line.strip().endswith(":") or line.strip().upper() == line.strip()

    wrapped_lines = []
    for raw_line in text.split("\n"):
        line = raw_line.strip()

        if not line:
            wrapped_lines.append("")
            continue

        # Wrap long lines
        if len(line) > max_chars_per_line:
            lines = textwrap.wrap(line, width=max_chars_per_line)
            wrapped_lines.extend(lines)
        else:
            wrapped_lines.append(line)

    # Draw lines properly
    for line in wrapped_lines:
        if y < 60:
            c.showPage()
            y = top_margin
            c.setFont("Helvetica", 11)

        # Heading styling
        if is_heading(line):
            c.setFont("Helvetica-Bold", 12)
        else:
            c.setFont("Helvetica", 11)

        c.drawString(left_margin, y, line)
        y -= line_height

    c.save()
    return filename
