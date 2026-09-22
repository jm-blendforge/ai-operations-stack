"""Generates the one-page printable 'where the footage goes' wall sheet (reportlab).
Demonstrates: programmatic PDF layout, brand palette as constants, text wrapping, card grid."""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit

PAPER, INK, TERRA, SAGE, SAND, GREY = (HexColor(c) for c in
    ["#FAF7F2", "#2B2622", "#B5563A", "#4E654E", "#EFE7DA", "#7A7166"])
W, H = letter

def txt(c, x, y, s, size=10, bold=False, color=INK, maxw=None, lead=None):
    f = "Helvetica-Bold" if bold else "Helvetica"
    c.setFillColor(color); c.setFont(f, size); lead = lead or size * 1.25
    for ln in (simpleSplit(s, f, size, maxw) if maxw else [s]):
        c.drawString(x, y, ln); y -= lead
    return y

def build(path, cards):
    c = canvas.Canvas(path, pagesize=letter)
    c.setFillColor(PAPER); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(INK); c.rect(0, H-92, W, 92, fill=1, stroke=0)
    txt(c, 36, H-40, "BLACKFORGE CONTENT", 22, True, PAPER)
    cw, ch, x0, y0 = (W-72-16)/2, 112, 36, H-92-24-112
    for i, (name, head, body, when, accent) in enumerate(cards):
        x, y = x0 + (i % 2)*(cw+16), y0 - (i//2)*(ch+12)
        c.setFillColor(HexColor("#FFFFFF")); c.roundRect(x, y, cw, ch, 8, fill=1, stroke=1)
        c.setFillColor(accent); c.setFont("Courier-Bold", 19); c.drawString(x+14, y+ch-30, name)
        txt(c, x+14, y+ch-46, head, 10, True)
        txt(c, x+14, y+ch-62, body, 9.2, False, GREY, maxw=cw-28, lead=11.5)
        c.setFillColor(SAND); c.roundRect(x+10, y+9, cw-20, 18, 4, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 8.6); c.drawString(x+16, y+14.5, when)
    c.save()
