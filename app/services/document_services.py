from pypdf import PdfReader

from app.services.document_classifier import classify_document
from app.llm.qwen import extract_medical_information


def extract_text(file_path: str) -> str:

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def process_document(file_path: str):

    text = extract_text(file_path)

    document_type = classify_document(text)

    result = {
        "document_type": document_type,
        "text": text
    }

    if document_type == "MEDICAL":

        medical_data = extract_medical_information(text)

        result["extracted_data"] = medical_data.model_dump()

    return result