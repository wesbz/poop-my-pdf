import argparse
from io import BytesIO

from tqdm import tqdm

from PyPDF4 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import *
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

poop_unicode = "\U0001F4A9"

def create_poop(text: str, x: int, y: int, pagesize: str, fontname: str, fontsize: int, color: str = COLOR):
    output_buffer = BytesIO()
    canva = canvas.Canvas(output_buffer, pagesize=pagesize)
    canva.setFont(fontname, fontsize)
    canva.setFillColor(color)
    
    style = ParagraphStyle(
        "Normal",
        fontName=fontname,
        fontSize=fontsize,
        leading=fontsize,
        alignment=1,
        textColor=color
    )
    p = Paragraph(text, style)
    p.wrap(x, y)
    p.drawOn(canva, 0, 0)
    
    canva.save()
    return output_buffer


def poop_it(input_file: str, output_file:str, text:str, fontname:str, fontsize:int):
    pdf_reader = PdfFileReader(open(input_file, 'rb'), strict=False)
    pdf_writer = PdfFileWriter()
    
    for page in tqdm(range(pdf_reader.getNumPages())):
        page = pdf_reader.getPage(page)
        _, _, x_max, y_max = page.mediaBox
        
        poop = create_poop(text, pagesize=page.mediaBox, x=int(x_max), y=int(y_max), fontname=fontname, fontsize=fontsize)
        poop_reader = PdfFileReader(poop)
        
        page.mergePage(poop_reader.getPage(0))
        
        pdf_writer.addPage(page)
    
    with open(output_file, 'wb') as pdf_output:
        pdf_writer.write(pdf_output)
        
    
    return pdf_reader, pdf_writer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to randomly watermark your pdf files.")
    parser.add_argument("-i", "--input", help="The input file to watermark.", required=True)
    parser.add_argument("-o", "--output", help="The output file to save the watermarked file.", required=True)
    parser.add_argument("-t", "--text", help="The text to watermark the file with.")
    parser.add_argument("-f", "--font", help="The font to use for the watermark.", default="Helvetica-Bold")
    parser.add_argument("-s", "--size", help="The size of the watermark.", default=40)
    parser.add_argument("-c", "--color", help=f"The color of the watermark: {sorted(list(getAllNamedColors().keys()))}", default=lightgrey)
    args = parser.parse_args()
    
    poop_it(args.input, args.output, args.text, args.font, args.size)
    print(f"{poop_unicode} Done {poop_unicode}")