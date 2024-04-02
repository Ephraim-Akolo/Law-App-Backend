import requests
from io import BytesIO
from docx import Document
import pytesseract
from PIL import Image
import PyPDF2
import pdfplumber


def read_docx_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        docx_bytes = BytesIO(response.content)
        document = Document(docx_bytes)
        text = "\n".join([paragraph.text for paragraph in document.paragraphs])
        return text
    else:
        print("Failed to download DOCX file from the URL")
        return None

def read_pdf_from_url(url):
    response = requests.get(url)
    print(response.headers)
    if response.status_code == 200:
        pdf_bytes = BytesIO(response.content)
        with pdfplumber.open(pdf_bytes) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
                break
        return text
    else:
        print("Failed to download PDF file from the URL")
        return None
    
def read_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        return text
    else:
        print("Failed to download text file from the URL")
        return None
    
def read_text_from_image_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        try:
            raise Exception
            text = pytesseract.image_to_string(image)
        except:
            return "Reading text from images not currently supported!"
        return text
    else:
        print("Failed to download image file from the URL")
        return None