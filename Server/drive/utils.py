import requests
from io import BytesIO
from docx import Document
import pytesseract
from PIL import Image
import PyPDF2
import pdfplumber

def read_docx_from_file(file):
    document = Document(file)
    text = "\n".join([paragraph.text for paragraph in document.paragraphs])
    return text

# def read_docx_from_url(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         return read_docx_from_buffer(response.content)
#     else:
#         print("Failed to download DOCX file from the URL")
#         return None
    
# def read_pdf_from_buff(file):
#     with open("./tttx.pdf", 'wb') as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)
#     with pdfplumber.open('./tttx.pdf') as pdf:
#         text = ""
#         for page in pdf.pages:
#             text += page.extract_text()
#             break
#     return text

def read_pdf_from_file(file):
    text_content = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text_content += page.extract_text()
    except Exception as e:
        text_content = f"Unable to read PDF file: {e}"
    return text_content


# def read_pdf_from_url(url):
#     response = requests.get(url)
#     print(response.headers)
#     if response.status_code == 200:
#         return read_pdf_from_buffer(response.content)
#     else:
#         print("Failed to download PDF file from the URL")
#         return None
    
# def read_text_from_url(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         text = response.text
#         return text
#     else:
#         print("Failed to download text file from the URL")
#         return None
    
# def read_text_from_image_url(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         image = Image.open(BytesIO(response.content))
#         try:
#             raise Exception
#             text = pytesseract.image_to_string(image)
#         except:
#             return "Reading text from images not currently supported!"
#         return text
#     else:
#         print("Failed to download image file from the URL")
#         return None