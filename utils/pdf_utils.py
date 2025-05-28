# utils/pdf_utils.py

def is_pdf(file_content):
    """
    Detect if the content is PDF.
    This checks for the standard PDF file header.
    """
    if isinstance(file_content, bytes):
        return file_content.startswith(b'%PDF')
    if isinstance(file_content, str):
        return file_content.strip().startswith('%PDF')
    return False
