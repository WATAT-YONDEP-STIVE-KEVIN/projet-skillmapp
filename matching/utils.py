import re
import string
import tempfile
#from PIL import Image
#import pytesseract
import io
#import docx2txt
#from PyPDF2 import PdfReader
#from pdf2image import convert_from_path


def clean_text(text):
    text = text.lower()
    patterHeadF = r"minist[eè]re|coll[eè]ge|d[eé]partemen|ghbs|evaluation|r[eé]publique|cameroun|region|paix|travail|patrie|d[ée]l[eé]gation|r[eé]gionale|lyc[eé]e|ann[eé]e scolaire|bilingue|s[eé]quence|examinateur"
    patterHeadE = r"ministry|minesec|republic|cameroon|region|peace|work|fatherland|delegation|regional|divisional|gbs|secondary|education"

    text = re.sub(r"\n", " ", text)
    text = re.sub(r"-", " ", text)
    text = re.sub(r"[\.]+", "", text)
    text = re.sub(patterHeadF, '', text)
    text = re.sub(patterHeadE, '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = " ".join(text.split())
    return text


def ocr_image_pil(image):
    return pytesseract.image_to_string(image, lang='eng+fra')


def extract_text_and_images_from_file(django_file):
    name = django_file.name.lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf" if name.endswith('.pdf') else ".docx") as tmp:
        for chunk in django_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    images = []
    ocr_texts = []

    if name.endswith(".pdf"):
        # Extraction du texte avec PyPDF2
        reader = PdfReader(tmp_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        # OCR sur les pages converties en images
        pil_images = convert_from_path(tmp_path, dpi=200)
        for idx, img in enumerate(pil_images):
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            image_data = buf.getvalue()

            images.append({
                "page": idx + 1,
                "image_data": image_data,
                "ext": "png"
            })

            ocr_text = ocr_image_pil(img)
            ocr_texts.append(ocr_text)

        full_text = text + " " + " ".join(ocr_texts)
        return clean_text(full_text), images

    elif name.endswith(".docx"):
        text = docx2txt.process(tmp_path)
        return clean_text(text), []

    return "", []
