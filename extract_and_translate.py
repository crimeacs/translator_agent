import argparse
import fitz  # PyMuPDF
import logging
from openai import OpenAI
from PyPDF2 import PdfMerger
import textwrap
from fpdf import FPDF
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    logging.info('Extracting text from PDF.')
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def save_text_to_file(text, file_path):
    """
    Saves text to a file.

    :param text: Text to save.
    :param file_path: Path to the file where the text will be saved.
    """
    logging.info('Saving text to file.')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

def translate_text_with_openai(client, text, language_1, language_2):
    """
    Translates text using OpenAI's GPT model.

    :param client: OpenAI client instance.
    :param text: Text to translate.
    :return: Translated text as a string.
    """
    logging.info('Translating text with OpenAI.')
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": f'You are a helpful assistant. You are expert in translating from {language_1} to {language_2}. Please translate the article text verbatim, excluding any website navigation, ads, footers, or other non-article elements. Translate header. You are tasked with outputting the translation of the whole article. Please output nothing but the translation'},
            {"role": "user", "content": text}
        ]
    )
    # Filter out non UTF-8 characters from the response
    translated_text = response.choices[0].message.content.encode('utf-8', 'ignore').decode('utf-8')
    return translated_text

def produce_certificate(name, address, language_1, language_2, filename):
    """
    Produces a certificate of translation in PDF format.

    :param name: Name of the person certifying the translation.
    :param address: Address of the person certifying the translation.
    :param language_1: Source language of the translation.
    :param language_2: Target language of the translation.
    :param filename: Path to the output PDF file.
    """
    logging.info('Producing certificate of translation.')
    letter_width_mm = 215.9  # Width of American letter size paper in mm
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = int(letter_width_mm / character_width_mm)

    text = f'I, {name} hereby certify that I am fluent in the {language_1} and {language_2} languages and that the attached translation is a faithful and accurate translation of the enclosed document in the Russian language.'
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    
    # Apply bold style for the title
    pdf.set_font(family='Arial', size=fontsize_pt, style='B')
    
    # Add the title (centered and bold)
    pdf.multi_cell(0, fontsize_mm * 2, 'Certificate of Translation', align='C')
    pdf.ln(fontsize_mm)  # Extra space after the title

    # Reset font style to regular for the body text
    pdf.set_font(family='Arial', size=fontsize_pt, style='')

    for line in text.split('\n'):
        lines = textwrap.wrap(line, width_text)
        for wrap in lines:
            try:
                pdf.cell(0, fontsize_mm, wrap.encode('latin-1', 'replace').decode('latin-1'), ln=1)
            except UnicodeEncodeError as e:
                logging.error(f'UnicodeEncodeError: {e}')
                wrap = wrap.encode('latin-1', 'replace').decode('latin-1')
                pdf.cell(0, fontsize_mm, wrap, ln=1)
        if not lines:
            pdf.ln()
    
    pdf.ln()
    pdf.ln()
    # Add the name in bold
    pdf.set_font(family='Arial', size=fontsize_pt, style='B')
    pdf.multi_cell(0, fontsize_mm, name)
    pdf.ln(fontsize_mm * 0.5)

    # Reset font style to regular and add the address
    pdf.set_font(family='Arial', size=fontsize_pt, style='')
    pdf.multi_cell(0, fontsize_mm, address)
    pdf.ln(fontsize_mm * 0.5)
    
    # Add the date, which uses today's date in Python
    today_date = datetime.today().strftime('%m/%d/%Y')
    pdf.multi_cell(0, fontsize_mm, today_date)
    try:
        pdf.output(filename, 'F')
    except Exception as e:
        logging.error(f'Failed to convert text to PDF: {e}')
        raise

def text_to_pdf(text, filename):
    """
    Converts text to a PDF file.

    :param text: Text to convert.
    :param filename: Path to the output PDF file.
    """
    logging.info('Converting text to PDF.')
    letter_width_mm = 215.9  # Width of American letter size paper in mm
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = int(letter_width_mm / character_width_mm)

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Arial', size=fontsize_pt)

    for line in text.split('\n'):
        lines = textwrap.wrap(line, width_text)
        for wrap in lines:
            try:
                pdf.cell(0, fontsize_mm, wrap.encode('latin-1', 'replace').decode('latin-1'), ln=1)
            except UnicodeEncodeError as e:
                logging.error(f'UnicodeEncodeError: {e}')
                wrap = wrap.encode('latin-1', 'replace').decode('latin-1')
                pdf.cell(0, fontsize_mm, wrap, ln=1)
        if not lines:
            pdf.ln()

    try:
        pdf.output(filename, 'F')
    except Exception as e:
        logging.error(f'Failed to convert text to PDF: {e}')
        raise

def merge_pdfs(pdfs, output):
    """
    Merges multiple PDF files into a single PDF file.

    :param pdfs: List of paths to the PDF files to merge.
    :param output: Path to the output merged PDF file.
    """
    logging.info('Merging PDFs.')
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(output)
    merger.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract, translate and merge PDF documents.")
    parser.add_argument("--pdf_path", help="Path to the PDF file to be processed")
    parser.add_argument("--output", help="Output file name for the merged PDF")
    parser.add_argument("--api_key", help="API key for OpenAI")
    parser.add_argument("--name", help="Name for the certificate of translation")
    parser.add_argument("--address", help="Address for the certificate of translation")
    parser.add_argument("--language_1", help="Source language for the translation")
    parser.add_argument("--language_2", help="Target language for the translation")
    parser.add_argument("--certificate_output", help="Output path for the certificate of translation")
    args = parser.parse_args()

    client = OpenAI(api_key=args.api_key)
    text = extract_text_from_pdf(args.pdf_path)
    produce_certificate(name=args.name, address=args.address, language_1=args.language_1, language_2=args.language_2, filename=args.certificate_output)
    save_text_to_file(text, 'extracted_text.txt')
    translated_text = translate_text_with_openai(client, text, args.language_1, args.language_2)
    save_text_to_file(translated_text, 'translated_extracted_text.txt')
    text_to_pdf(translated_text, 'translated_extracted_text.pdf')
    pdfs_to_merge = [
        args.certificate_output,
        'translated_extracted_text.pdf',
        args.pdf_path
    ]
    merge_pdfs(pdfs_to_merge, args.output)
    logging.info('Process completed successfully.')
